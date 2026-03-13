from PIL import Image
import pytesseract
import re
from typing import Dict, Optional

class OCREngine:
    """Extract text and fields from product images"""

    def extract_from_image(self, image_path: str) -> Dict:
        """Extract text from image using OCR"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return self._parse_ocr_text(text)
        except Exception as e:
            return {"error": str(e), "text": ""}

    def _parse_ocr_text(self, text: str) -> Dict:
        """Parse OCR text to extract structured fields"""
        fields = {}

        # Extract VIN (17 characters)
        vin_match = re.search(r'\b[A-HJ-NPR-Z0-9]{17}\b', text.upper())
        if vin_match:
            fields["vin"] = vin_match.group()

        # Extract UPC (12 digits)
        upc_match = re.search(r'\b\d{12}\b', text)
        if upc_match:
            fields["upc"] = upc_match.group()

        # Extract model numbers (common patterns)
        model_match = re.search(r'(?:Model|MOD|M/N)[:\s]+([A-Z0-9-]+)', text, re.IGNORECASE)
        if model_match:
            fields["model"] = model_match.group(1)

        # Extract lot/batch numbers
        lot_match = re.search(r'(?:Lot|Batch|LOT)[:\s]+([A-Z0-9-]+)', text, re.IGNORECASE)
        if lot_match:
            fields["lot"] = lot_match.group(1)

        fields["raw_text"] = text
        return fields
