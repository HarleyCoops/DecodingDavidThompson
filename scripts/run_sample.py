#!/usr/bin/env python3
"""Run the transcription pipeline on the bundled sample image.

This script demonstrates running the preprocessing, line segmentation, and OCR
steps on the `docs/DavidThompsonSample.jpg` image included in the repository.
The results are written to `output/sample_run/`.
"""
from pathlib import Path
from pipeline import run_pipeline


def main():
    repo_root = Path(__file__).resolve().parent.parent
    sample = repo_root / "docs" / "DavidThompsonSample.jpg"
    output = repo_root / "output" / "sample_run"
    run_pipeline(sample, output)


if __name__ == "__main__":
    main()
