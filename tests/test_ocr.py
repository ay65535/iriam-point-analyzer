import pytest
from pathlib import Path
from src.ocr.ocr_engine import OCREngine
from src.preprocessing.preprocessor import preprocess
from src.evaluation.metrics import TextEvaluator

TEST_IMAGE = "data/img/IMG_1527.PNG"


def test_ocr_engine_initialization():
    engine = OCREngine(engine="easyocr")
    assert engine.engine == "easyocr"
    assert engine.language == "ja"
    assert engine.psm == 3


def test_preprocessor():
    output = preprocess(TEST_IMAGE, "basic")
    assert Path(output).exists()
    assert str(output).endswith("_basic.PNG")


@pytest.mark.parametrize("method", ["none", "basic", "adaptive", "otsu"])
def test_ocr_workflow(method):
    engine = OCREngine()
    img_path = preprocess(TEST_IMAGE, method)
    results = engine.extract(img_path)

    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(text, str) for text in results)

    accuracy = TextEvaluator.compare_normalized(results, TextEvaluator.load_expected())
    assert accuracy > 0
