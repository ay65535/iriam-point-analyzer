"""
EasyOCRを使用したOCRエンジンの実装
"""

import os
import easyocr
from typing import List
from .base import OCREngine


class EasyOCREngine(OCREngine):
    """EasyOCRを使用したOCR実装"""

    def __init__(self, languages: List[str] = None):
        """
        初期化

        Args:
            languages: 認識する言語のリスト（デフォルト: ['ja', 'en']）
        """
        if languages is None:
            languages = ["ja", "en"]
        self.reader = easyocr.Reader(languages)

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
        # 前処理済み画像があれば、それを使用
        image_to_process = preprocessed_path if preprocessed_path else image_path

        try:
            # テキスト認識を実行
            results = self.reader.readtext(image_to_process)

            # 結果を行のリストに変換（確信度が低いものを除外）
            lines = []
            for bbox, text, prob in results:
                if prob > 0.2:  # 確信度が0.2以上のものを採用
                    lines.append(text)

            return lines

        except Exception as e:
            raise RuntimeError(f"EasyOCR error: {str(e)}")

        finally:
            # 一時ファイルの削除（前処理済み画像が指定されている場合）
            if preprocessed_path and os.path.exists(preprocessed_path):
                os.remove(preprocessed_path)
