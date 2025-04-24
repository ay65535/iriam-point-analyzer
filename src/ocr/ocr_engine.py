import os
from typing import List
from PIL import Image
import pytesseract
from easyocr import Reader


class OCREngine:
    """
    EasyOCR または Tesseract を用いた OCR エンジンラッパー
    """

    def __init__(self, engine: str = "easyocr", language: str = "ja", psm: int = 3):
        self.engine = engine.lower()
        self.language = language
        self.psm = psm
        if self.engine == "easyocr":
            self.reader = Reader([language], gpu=False)

    def extract(self, image_path: str) -> List[str]:
        """
        画像からテキストを抽出して行リストを返す。
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"画像が見つかりません: {image_path}")

        if self.engine == "easyocr":
            results = self.reader.readtext(image_path)
            return [text for (_, text, prob) in results if prob > 0.2]

        elif self.engine == "tesseract":
            config = f"--psm {self.psm}"
            raw = pytesseract.image_to_string(
                Image.open(image_path), lang=self.language, config=config
            )
            return [line.strip() for line in raw.splitlines() if line.strip()]

        else:
            raise ValueError(f"Unknown engine: {self.engine}")
