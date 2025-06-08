#!/usr/bin/env python3
import subprocess
import argparse
from pathlib import Path


def train_model(ground_truth_file, output_name, epochs=10):
    output_path = Path(f"models/{output_name}.mlmodel")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "kraken",
        "train",
        "-f",
        str(ground_truth_file),
        "-o",
        str(output_path),
        "--epochs",
        str(epochs),
        "--aug",
        "--workers",
        "4",
    ]
    print(f"Training model: {output_name}")
    print("Command:", " ".join(cmd))
    subprocess.run(cmd)
    print(f"Model saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train custom OCR model")
    parser.add_argument("ground_truth", help="Ground truth TSV file")
    parser.add_argument("-n", "--name", required=True, help="Model name")
    parser.add_argument("-e", "--epochs", type=int, default=10, help="Training epochs")
    args = parser.parse_args()
    train_model(args.ground_truth, args.name, args.epochs)
