import sys
from pathlib import Path
import pytest

# Skip tests if OpenCV is not available
pytest.importorskip("cv2")

sys.path.append(str(Path(__file__).parent.parent))

from scripts.preprocess import ImagePreprocessor
from scripts.segment import LineSegmenter
from scripts.ocr import OCRProcessor
from scripts.pipeline import run_pipeline


def test_preprocessing():
    preprocessor = ImagePreprocessor()
    assert preprocessor is not None


def test_segmentation():
    segmenter = LineSegmenter()
    assert segmenter is not None


def test_ocr():
    ocr = OCRProcessor()
    assert ocr is not None


def test_sample_run(tmp_path):
    """Run the full pipeline on the bundled sample image."""
    pytest.importorskip("kraken")

    repo_root = Path(__file__).parent.parent
    sample = repo_root / "docs" / "DavidThompsonSample.jpg"
    output_dir = tmp_path
    run_pipeline(sample, output_dir)

    result_file = output_dir / "ocr" / f"{sample.stem}.txt"
    assert result_file.exists()
