import cv2
import yaml
from pathlib import Path

class ImagePreprocessor:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)["preprocessing"]

    def enhance_image(self, image_path):
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        clahe = cv2.createCLAHE(
            clipLimit=self.config["clahe"]["clip_limit"],
            tileGridSize=tuple(self.config["clahe"]["tile_grid_size"]),
        )
        return clahe.apply(img)

    def threshold_image(self, img):
        return cv2.ximgproc.niBlackThreshold(
            img,
            255,
            cv2.THRESH_BINARY_INV,
            blockSize=self.config["threshold"]["block_size"],
            k=self.config["threshold"]["k"],
        )

    def remove_guidelines(self, binary_img):
        kernel_v = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            tuple(self.config["morphology"]["guide_removal_kernel"]),
        )
        guides = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel_v)
        return cv2.bitwise_and(binary_img, binary_img, mask=cv2.bitwise_not(guides))

    def process(self, input_path, output_path):
        img = self.enhance_image(input_path)
        binary = self.threshold_image(img)
        clean = self.remove_guidelines(binary)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_path), clean)

        return img, clean
