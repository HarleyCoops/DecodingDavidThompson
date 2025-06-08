from kraken import rpred
from kraken.lib import models
from PIL import Image
import json
from pathlib import Path
import yaml

class OCRProcessor:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)["ocr"]
        self.model = None

    def load_model(self, model_path=None):
        if model_path is None:
            model_path = self.config["default_model"]
        self.model = models.load_any(model_path)

    def process_line(self, image_path):
        img = Image.open(image_path)
        pred_it = rpred.rpred(self.model, img, None, None)
        results = []
        for pred in pred_it:
            results.append({"text": pred.prediction, "confidence": pred.confidence})
        return results

    def process_directory(self, input_dir, output_file):
        input_dir = Path(input_dir)
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if self.model is None:
            self.load_model()

        all_results = []
        line_files = sorted(input_dir.glob("*.png"))
        for line_file in line_files:
            result = self.process_line(line_file)
            if result:
                all_results.append(
                    {
                        "file": line_file.name,
                        "text": result[0]["text"],
                        "confidence": result[0]["confidence"],
                    }
                )

        if output_file.suffix == ".json":
            with open(output_file, "w") as f:
                json.dump(all_results, f, indent=2)
        else:
            with open(output_file, "w") as f:
                for result in all_results:
                    if result["confidence"] >= self.config["confidence_threshold"]:
                        f.write(result["text"] + "\n")
        return all_results
