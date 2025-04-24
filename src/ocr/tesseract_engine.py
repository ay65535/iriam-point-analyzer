"""
Tesseractを使用したOCRエンジンの実装
"""

import os
import subprocess
from typing import List
from .base import OCREngine
from src.config.config_loader import load_config


class TesseractEngine(OCREngine):
    """Tesseractを使用したOCR実装"""

    def __init__(self, tessdata_prefix: str = None, psm: int = 6):
        """
        初期化

        Args:
            tessdata_prefix: tessdataディレクトリのパス
            psm: Page Segmentation Mode (デフォルト: 6)
        """
        # 設定ファイルから設定を読み込む
        config = load_config()

        # tessdata_prefixの設定: 引数 > 設定ファイル の順で優先
        self.tessdata_prefix = tessdata_prefix
        if self.tessdata_prefix is None:
            try:
                self.tessdata_prefix = config["ocr"]["tessdata_prefix"]
            except (KeyError, TypeError):
                raise ValueError(
                    "設定ファイルに 'ocr.tessdata_prefix' が定義されていません。"
                    "設定ファイルに 'ocr' セクションを作成し、'tessdata_prefix' に"
                    "tessdataディレクトリのパスを設定してください。"
                )

        self.psm = psm

    def extract_text(self, image_path: str, preprocessed_path: str = None) -> List[str]:
        """
        画像からテキストを抽出する

        Args:
            image_path: 入力画像のパス
            preprocessed_path: 前処理済み画像の保存パス（オプション）

        Returns:
            抽出されたテキスト行のリスト

        Raises:
            RuntimeError: テキスト抽出に失敗した場合
        """
        # 使用する画像のパスを決定
        image_to_process = preprocessed_path if preprocessed_path else image_path

        try:
            # Tesseractを実行
            result = subprocess.run(
                [
                    "tesseract",
                    image_to_process,
                    "stdout",
                    "-l",
                    "jpn",
                    f"--psm",
                    str(self.psm),
                ],
                capture_output=True,
                text=True,
                env={"TESSDATA_PREFIX": self.tessdata_prefix},
            )

            if result.returncode != 0:
                raise RuntimeError(f"Tesseract error: {result.stderr}")

            # 空行を除去して結果を返す
            lines = [
                line.strip() for line in result.stdout.splitlines() if line.strip()
            ]
            return lines

        except subprocess.SubprocessError as e:
            raise RuntimeError(f"Failed to execute Tesseract: {str(e)}")

        finally:
            # 一時ファイルの削除（前処理済み画像が指定されている場合）
            if preprocessed_path and os.path.exists(preprocessed_path):
                os.remove(preprocessed_path)
