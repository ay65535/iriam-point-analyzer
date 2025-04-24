"""
OCRを使用して画像からテキストを抽出し、精度を評価するメインスクリプト
"""

import argparse
import os
from src.preprocessing.image_processor import ImageProcessor
from src.ocr.easyocr_engine import EasyOCREngine
from src.ocr.tesseract_engine import TesseractEngine
from src.evaluation.metrics import TextEvaluator


def main():
    parser = argparse.ArgumentParser(description="画像からのテキスト抽出と精度評価")
    parser.add_argument("image", help="入力画像ファイルのパス")
    parser.add_argument(
        "--engine",
        choices=["easyocr", "tesseract"],
        default="easyocr",
        help="使用するOCRエンジン",
    )
    parser.add_argument(
        "--preprocess",
        choices=["none", "basic", "adaptive", "otsu"],
        default="none",
        help="前処理方法",
    )
    args = parser.parse_args()

    # OCRエンジンの初期化
    if args.engine == "easyocr":
        ocr_engine = EasyOCREngine()
    else:  # tesseract
        ocr_engine = TesseractEngine()

    # 期待される結果の読み込み
    expected = TextEvaluator.load_expected()

    # 前処理の適用（指定された場合）
    preprocessed_path = None
    if args.preprocess != "none":
        print(f"\n前処理方法: {args.preprocess}")
        preprocessed_path = f"temp_preprocessed_{args.preprocess}.png"
        ImageProcessor.preprocess_image(args.image, preprocessed_path, args.preprocess)

    try:
        # テキスト抽出
        print(f"\nOCRエンジン: {args.engine}")
        extracted = ocr_engine.extract_text(args.image, preprocessed_path)

        print("\n=== 抽出されたテキスト ===")
        for line in extracted:
            print(line)

        # 精度評価
        standard_acc = TextEvaluator.compare(extracted, expected)
        normalized_acc = TextEvaluator.compare_normalized(extracted, expected)

        print(f"\n標準精度: {standard_acc:.2f}%")
        print(f"正規化精度: {normalized_acc:.2f}%")

    finally:
        # 一時ファイルの削除
        if preprocessed_path and os.path.exists(preprocessed_path):
            os.remove(preprocessed_path)


if __name__ == "__main__":
    main()
