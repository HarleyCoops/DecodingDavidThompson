#!/usr/bin/env python3
import argparse
from pathlib import Path
from preprocess import ImagePreprocessor
from segment import LineSegmenter
from ocr import OCRProcessor

def run_pipeline(input_image, output_dir, config_path="config/config.yaml"):
    input_path = Path(input_image)
    output_dir = Path(output_dir)

    preprocessor = ImagePreprocessor(config_path)
    segmenter = LineSegmenter(config_path)
    ocr = OCRProcessor(config_path)

    print(f"Processing {input_path.name}...")
    preprocessed_path = output_dir / "preprocessed" / f"{input_path.stem}_processed.png"
    original_img, binary_img = preprocessor.process(input_path, preprocessed_path)

    print("Segmenting lines...")
    lines_dir = output_dir / "lines" / input_path.stem
    segmenter.segment_lines(original_img, binary_img, lines_dir)

    print("Running OCR...")
    ocr_output = output_dir / "ocr" / f"{input_path.stem}.txt"
    ocr.process_directory(lines_dir, ocr_output)

    print(f"Pipeline complete! Results saved to {ocr_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="David Thompson Transcription Pipeline")
    parser.add_argument("input", help="Input image file")
    parser.add_argument("-o", "--output", default="output", help="Output directory")
    parser.add_argument("-c", "--config", default="config/config.yaml", help="Config file")
    args = parser.parse_args()
    run_pipeline(args.input, args.output, args.config)
