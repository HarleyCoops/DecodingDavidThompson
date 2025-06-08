import cv2
from skimage import measure
from pathlib import Path
import yaml

class LineSegmenter:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def segment_lines(self, original_img, binary_img, output_dir):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        kernel_h = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            tuple(self.config["preprocessing"]["morphology"]["line_closing_kernel"]),
        )
        h_close = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel_h)

        labels = measure.label(h_close, connectivity=2)
        regions = measure.regionprops(labels)
        regions = sorted(regions, key=lambda r: r.bbox[0])

        lines = []
        seg_config = self.config["segmentation"]
        for idx, region in enumerate(regions):
            y0, x0, y1, x1 = region.bbox
            height = y1 - y0
            if seg_config["min_line_height"] <= height <= seg_config["max_line_height"]:
                margin = seg_config["horizontal_margin"]
                x0 = max(0, x0 - margin)
                x1 = min(original_img.shape[1], x1 + margin)

                line_img = original_img[y0:y1, x0:x1]
                line_path = output_dir / f"line_{idx+1:03d}.png"
                cv2.imwrite(str(line_path), line_img)
                lines.append(line_path)

        print(f"Extracted {len(lines)} lines to {output_dir}")
        return lines
