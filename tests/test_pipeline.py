import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.preprocess import ImagePreprocessor
from scripts.segment import LineSegmenter
from scripts.ocr import OCRProcessor


def test_preprocessing():
    preprocessor = ImagePreprocessor()
    assert preprocessor is not None


def test_segmentation():
    segmenter = LineSegmenter()
    assert segmenter is not None


def test_ocr():
    ocr = OCRProcessor()
    assert ocr is not None
