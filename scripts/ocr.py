import pytesseract
from PIL import Image
import json
from pathlib import Path
import yaml
import os

class OCRProcessor:
    def __init__(self, config_path="config/config.yaml"):
        # Set the Tesseract path if it's not in your system PATH
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Load config if exists
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                self.config = yaml.safe_load(f).get("ocr", {})
        else:
            self.config = {}

    def process_line(self, image_path):
        """Process a single line image with Tesseract OCR."""
        try:
            img = Image.open(image_path)
            # Use Tesseract to do OCR on the image
            text = pytesseract.image_to_string(img, config='--psm 7')
            return [{"text": text.strip(), "confidence": 1.0}]
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            return [{"text": "", "confidence": 0.0}]

    def process_directory(self, input_dir, output_file):
        """Process all images in a directory and save results to a file."""
        input_dir = Path(input_dir)
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        results = {}
        for img_path in input_dir.glob("*.png"):
            line_results = self.process_line(img_path)
            results[img_path.name] = line_results[0] if line_results else {"text": "", "confidence": 0.0}
        
        # Save results as JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return results

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
