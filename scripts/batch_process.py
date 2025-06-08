#!/usr/bin/env python3
import argparse
from pathlib import Path
from pipeline import run_pipeline
from tqdm import tqdm


def batch_process(input_dir, output_dir, config_path="config/config.yaml"):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    image_files = list(input_dir.glob("*.png")) + list(input_dir.glob("*.jpg"))
    print(f"Found {len(image_files)} images to process")

    for img_file in tqdm(image_files):
        try:
            run_pipeline(img_file, output_dir, config_path)
        except Exception as e:
            print(f"Error processing {img_file.name}: {e}")
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch process images")
    parser.add_argument("input_dir", help="Directory containing images")
    parser.add_argument("-o", "--output", default="output", help="Output directory")
    parser.add_argument("-c", "--config", default="config/config.yaml", help="Config file")
    args = parser.parse_args()
    batch_process(args.input_dir, args.output, args.config)
