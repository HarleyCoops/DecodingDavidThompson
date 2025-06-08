import cv2
import yaml
from pathlib import Path

class LineSegmenter:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)["segmentation"]

    def segment_lines(self, original_img, binary_img, output_dir):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Find contours (lines)
        contours, _ = cv2.findContours(
            binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        line_num = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if (
                h >= self.config["min_line_height"]
                and h <= self.config["max_line_height"]
            ):
                margin = self.config["horizontal_margin"]
                line_img = original_img[
                    max(0, y - margin) : y + h + margin, max(0, x - margin) : x + w + margin
                ]
                line_path = output_dir / f"line_{line_num:03d}.png"
                cv2.imwrite(str(line_path), line_img)
                line_num += 1
        return line_num
