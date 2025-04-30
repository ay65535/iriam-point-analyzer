"""OCRスクリプトのメインエントリーポイント"""

import os
import csv
import pytesseract
from ocr import check_tesseract, extract_data_from_image

# Tesseract OCRのパス設定
pytesseract.pytesseract.tesseract_cmd = (
    r"/opt/homebrew/bin/tesseract"  # macOS (Homebrew)
)


def main():
    """メイン処理を実行する"""
    img_dir = "img/"
    output_csv = "output.csv"
    all_data = []

    try:
        if not os.path.isdir(img_dir):
            print(f"エラー: 画像ディレクトリ '{img_dir}' が見つかりません。")
            return

        # PNG, JPG, JPEGファイルを列挙
        image_files = sorted(
            [
                f
                for f in os.listdir(img_dir)
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            ]
        )

        if not image_files:
            print(f"エラー: {img_dir} に画像ファイルが見つかりません。")
            return

        print(f"{len(image_files)} 個の画像を処理します...")

        for filename in image_files:
            image_path = os.path.join(img_dir, filename)
            print(f"処理中: {image_path}")
            extracted_data = extract_data_from_image(image_path)
            if extracted_data:
                all_data.extend(extracted_data)
            else:
                print(f"情報: {filename} から有効なデータを抽出できません。")

    except (FileNotFoundError, PermissionError) as e:
        print(f"ファイルアクセスエラー: {e}")
        return
    except ValueError as e:
        print(f"データ処理エラー: {e}")
        return
    except IOError as e:
        print(f"入出力エラー: {e}")
        return

    if not all_data:
        print(
            "エラー: どの画像からもデータが抽出できません。"
            "OCRの精度や画像内容を確認してください。"
        )
        return

    # 逆順に並べ替え
    all_data.reverse()

    # CSVに出力
    try:
        with open(output_csv, "w", newline="", encoding="utf-8-sig") as csvfile:
            fieldnames = ["date", "pt", "name", "namae"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)
        print(f"処理完了: 結果を {output_csv} に出力しました。")
    except IOError as e:
        print(f"CSV書き込み中にIOエラー: {e}")
    except (UnicodeError, ValueError) as e:
        print(f"CSV書き込み中にデータエラー: {e}")


if __name__ == "__main__":
    if check_tesseract():
        main()
