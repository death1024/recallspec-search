import re
from typing import Dict, List, Optional
from ..models.specs import ProductIdentitySpec

class IdentitySpecEngine:
    """Parse user input into structured Product Identity Spec"""

    # Common brand aliases
    BRAND_ALIASES = {
        "gm": "General Motors",
        "vw": "Volkswagen",
        "bmw": "BMW",
    }

    # Category keywords
    CATEGORY_KEYWORDS = {
        "vehicle": ["car", "truck", "suv", "vehicle", "auto"],
        "consumer_product": ["stroller", "crib", "toy", "appliance", "fryer"],
        "food": ["food", "snack", "beverage"],
        "drug": ["medicine", "drug", "prescription"],
        "device": ["medical device", "pacemaker"],
    }

    def parse_text(self, text: str, fields: Optional[Dict] = None) -> ProductIdentitySpec:
        """Parse text input into identity spec"""
        spec_data = fields or {}

        # Extract VIN (17 characters, alphanumeric)
        vin_match = re.search(r'\b[A-HJ-NPR-Z0-9]{17}\b', text.upper())
        if vin_match:
            spec_data["vin"] = vin_match.group()
            spec_data["category"] = "vehicle"

        # Extract UPC (12 digits)
        upc_match = re.search(r'\b\d{12}\b', text)
        if upc_match:
            spec_data["upc"] = upc_match.group()

        # Detect category
        if "category" not in spec_data:
            spec_data["category"] = self._detect_category(text)

        # Extract brand (simple keyword matching)
        spec_data["brand"] = self._extract_brand(text)

        return self._build_spec(spec_data)

    def _detect_category(self, text: str) -> Optional[str]:
        """Detect product category from text"""
        text_lower = text.lower()
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return category
        return None

    def _extract_brand(self, text: str) -> Optional[str]:
        """Extract brand name (simple keyword matching)"""
        text_lower = text.lower()
        for alias, full_name in self.BRAND_ALIASES.items():
            if alias in text_lower:
                return full_name
        return None

    def _build_spec(self, data: Dict) -> ProductIdentitySpec:
        """Build ProductIdentitySpec from extracted data"""
        missing = []
        if not data.get("brand"):
            missing.append("brand")
        if not data.get("model"):
            missing.append("model")

        status = "complete" if not missing else "partial" if data.get("brand") or data.get("vin") or data.get("upc") else "minimal"

        return ProductIdentitySpec(
            status=status,
            category=data.get("category"),
            brand=data.get("brand"),
            brand_confidence=0.9 if data.get("brand") else 0.0,
            model=data.get("model"),
            model_confidence=0.9 if data.get("model") else 0.0,
            upc=data.get("upc"),
            vin=data.get("vin"),
            lot=data.get("lot"),
            missing_fields=missing,
            disambiguation_questions=self._generate_questions(missing)
        )

    def _generate_questions(self, missing: List[str]) -> List[str]:
        """Generate questions for missing fields"""
        questions = []
        if "brand" in missing:
            questions.append("What is the brand or manufacturer name?")
        if "model" in missing:
            questions.append("What is the model number or product code?")
        return questions
