"""画像処理とOCR関連の関数を提供するモジュール"""

# 標準ライブラリインポート
import re
from typing import List, Dict, Any, cast

# サードパーティライブラリインポート
from PIL import Image, ImageEnhance
from PIL.Image import Image as PILImage
import pytesseract

# ローカルアプリケーション/ライブラリ固有のインポート
from .text_processing import get_name_from_table

# デバッグモードを有効にする
DEBUG = True


def check_tesseract() -> bool:
    """
    Tesseract OCRが利用可能か確認する

    Returns:
        bool: Tesseractが利用可能な場合True
    """
    try:
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract OCR バージョン {version} を検知しました。")
        return True
    except pytesseract.TesseractNotFoundError:
        print("エラー: Tesseract OCRがインストールされていません。")
        return False
    except (IOError, OSError) as e:
        print(f"OCR確認中のシステムエラー: {e}")
        return False
    except RuntimeError as e:
        print(f"OCR確認中の実行時エラー: {e}")
        return False


def enhance_image(image: PILImage) -> PILImage:
    """
    画像の品質を向上させる

    Args:
        image: 元の画像

    Returns:
        処理された画像
    """
    # コントラストを強調
    contrast_enhancer = ImageEnhance.Contrast(image)
    enhanced = cast(PILImage, contrast_enhancer.enhance(1.5))

    # シャープネスを強調
    sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
    enhanced = cast(PILImage, sharpness_enhancer.enhance(1.5))

    # 画像を拡大
    width, height = enhanced.size
    enhanced = cast(
        PILImage, enhanced.resize((width * 2, height * 2), Image.Resampling.LANCZOS)
    )

    return enhanced


def extract_data_from_image(image_path: str) -> List[Dict[str, Any]]:
    """
    画像からテキストを抽出し、データを解析する

    Args:
        image_path: 処理する画像のパス

    Returns:
        解析されたデータのリスト。各要素は辞書で、
        date, pt, name, namaeのキーを持つ
    """
    try:
        # OCRの設定
        custom_config = r"--oem 1 --psm 6 -l jpn+jpn_vert --dpi 300"

        # 画像を読み込み
        image = cast(PILImage, Image.open(image_path))

        # 画像の品質を向上
        enhanced_image = enhance_image(image)

        # OCR実行（より高い精度で）
        text = pytesseract.image_to_string(
            enhanced_image,
            config=custom_config,
        )

        if DEBUG:
            print(f"\n--- Extracted Text from {image_path} ---")
            print(text)
            print("---------------------------------------\n")

        lines = text.split("\n")
        data = []
        current_date_str = None

        # 日付パターン
        date_pattern = re.compile(
            r"(\d{4})\s*[年]\s*(\d{1,2})\s*[月]\s*(\d{1,2})\s*[日晶]"
        )

        # ポイントと名前のパターン
        pt_name_pattern = re.compile(r"([\d,\.]+)\s*[pPｐＰ]?[tTｔＴ]\s+(.*)")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 日付行の検出
            date_match = date_pattern.search(line)
            if date_match:
                year, month, day = map(int, date_match.groups())
                try:
                    current_date_str = f"{year:04}/{month:02}/{day:02}"
                    if DEBUG:
                        print(f"日付検出: {current_date_str} (元: {line})")
                except ValueError:
                    print(f"警告: 無効な日付形式: {line} in {image_path}")
                    current_date_str = None
                continue

            # ポイント/名前行の検出
            if current_date_str:
                pt_name_match = pt_name_pattern.search(line)
                if pt_name_match:
                    pt_str, raw_namae = pt_name_match.groups()
                    # カンマ・ドットをすべて除去し数値化
                    pt_val = re.sub(r"[,\.]", "", pt_str)
                    try:
                        pt = int(pt_val)
                    except ValueError:
                        if DEBUG:
                            print(f"ポイント解析失敗: {pt_str} -> {pt_val} in {line}")
                        continue

                    # 名前マッピング取得
                    name_eng, namae_jp = get_name_from_table(raw_namae)

                    # 空文字列でない場合のみデータを追加
                    if name_eng and namae_jp:
                        data.append(
                            {
                                "date": current_date_str,
                                "pt": str(pt),  # 文字列として保存
                                "name": name_eng,
                                "namae": namae_jp,
                            }
                        )
                        if DEBUG:
                            print(
                                f"データ検出: date={current_date_str}, "
                                f"pt={pt}, name={name_eng}, namae={namae_jp}"
                            )
                else:
                    if DEBUG:
                        print(f"スキップ行(ポイント形式不一致): {line}")

        return data

    except pytesseract.TesseractNotFoundError:
        print("エラー: Tesseract OCRが見つかりません。インストールを確認してください。")
        return []
    except (IOError, OSError) as e:
        print(f"エラー: {image_path} の読み込み中にファイルエラー: {e}")
        return []
    except (ValueError, TypeError) as e:
        print(f"エラー: {image_path} のデータ処理中に型エラー: {e}")
        return []
    except RuntimeError as e:
        print(f"エラー: {image_path} の処理中に実行時エラー: {e}")
        return []
