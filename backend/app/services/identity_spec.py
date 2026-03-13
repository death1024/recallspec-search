import re
from typing import Dict, List, Optional, Tuple
from ..models.specs import ProductIdentitySpec

class IdentitySpecEngine:
    """Parse user input into structured Product Identity Spec"""

    # Known brand aliases for high-confidence matching
    BRAND_ALIASES = {
        "gm": "General Motors", "vw": "Volkswagen", "bmw": "BMW",
        "honda": "Honda", "toyota": "Toyota", "ford": "Ford",
        "tesla": "Tesla", "nissan": "Nissan", "chevrolet": "Chevrolet",
        "chevy": "Chevrolet", "mercedes": "Mercedes-Benz", "benz": "Mercedes-Benz",
        "hyundai": "Hyundai", "kia": "Kia", "mazda": "Mazda",
        "subaru": "Subaru", "jeep": "Jeep", "dodge": "Dodge",
        "ram": "Ram", "gmc": "GMC", "cadillac": "Cadillac",
        "lexus": "Lexus", "acura": "Acura", "infiniti": "Infiniti",
        "volvo": "Volvo", "audi": "Audi", "porsche": "Porsche",
    }

    # Category keywords
    CATEGORY_KEYWORDS = {
        "vehicle": ["car", "truck", "suv", "vehicle", "auto", "van", "sedan", "coupe"],
        "consumer_product": ["stroller", "crib", "toy", "appliance", "fryer", "chair", "table"],
        "food": ["food", "snack", "beverage", "drink"],
        "drug": ["medicine", "drug", "prescription", "medication"],
        "device": ["medical device", "pacemaker", "implant"],
    }

    def parse_text(self, text: str, fields: Optional[Dict] = None) -> ProductIdentitySpec:
        """Parse text input into identity spec with flexible extraction"""
        spec_data = fields or {}
        spec_data["raw_query"] = text  # Preserve original query for fuzzy search

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

        # Extract brand with confidence score
        brand, brand_conf = self._extract_brand_smart(text)
        if brand:
            spec_data["brand"] = brand
            spec_data["brand_confidence"] = brand_conf

        # Extract model with confidence score
        model, model_conf = self._extract_model_smart(text)
        if model:
            spec_data["model"] = model
            spec_data["model_confidence"] = model_conf

        return self._build_spec(spec_data)

    def _detect_category(self, text: str) -> Optional[str]:
        """Detect product category from text"""
        text_lower = text.lower()
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return category
        return None

    def _extract_brand(self, text: str) -> Optional[str]:
        """Legacy method - use _extract_brand_smart instead"""
        brand, _ = self._extract_brand_smart(text)
        return brand

    def _extract_brand_smart(self, text: str) -> Tuple[Optional[str], float]:
        """Extract brand name with confidence score using multiple strategies"""
        text_lower = text.lower()

        # Strategy 1: Known brand aliases (high confidence)
        for alias, full_name in self.BRAND_ALIASES.items():
            if re.search(rf'\b{alias}\b', text_lower):
                return full_name, 0.95

        # Strategy 2: Capitalized words (medium confidence)
        # Look for capitalized words that might be brand names
        words = text.split()
        for i, word in enumerate(words):
            # Skip common words
            if word.lower() in ['the', 'a', 'an', 'my', 'recall', 'vin', 'upc']:
                continue
            # Check if word starts with capital and is 2+ chars
            if word[0].isupper() and len(word) >= 2 and word.isalpha():
                # Higher confidence if followed by another capitalized word (likely model)
                if i + 1 < len(words) and words[i + 1][0].isupper():
                    return word, 0.7
                return word, 0.6

        return None, 0.0

    def _extract_model(self, text: str) -> Optional[str]:
        """Legacy method - use _extract_model_smart instead"""
        model, _ = self._extract_model_smart(text)
        return model

    def _extract_model_smart(self, text: str) -> Tuple[Optional[str], float]:
        """Extract model name with confidence score using multiple strategies"""
        text_lower = text.lower()

        # Strategy 1: Model patterns (alphanumeric with dash/space)
        # Examples: "F-150", "Model S", "Accord 2023", "CX-5"
        model_patterns = [
            r'\b([A-Z][\w\-]+\s*\d{1,4})\b',  # F-150, Model 3, CX-5
            r'\b(model\s+[a-z0-9]+)\b',        # Model S, Model 3
            r'\b([A-Z]{2,}\-\d+)\b',           # CX-5, RX-350
        ]

        for pattern in model_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1), 0.8

        # Strategy 2: Look for capitalized word after known brand
        words = text.split()
        for i, word in enumerate(words):
            if word in self.BRAND_ALIASES.values() and i + 1 < len(words):
                next_word = words[i + 1]
                if next_word[0].isupper() or next_word[0].isdigit():
                    return next_word, 0.75

        # Strategy 3: Year followed by capitalized word (e.g., "2023 Accord")
        year_model = re.search(r'\b(20\d{2})\s+([A-Z][a-z]+)', text)
        if year_model:
            return year_model.group(2), 0.7

        return None, 0.0

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
            brand_confidence=data.get("brand_confidence", 0.0),
            model=data.get("model"),
            model_confidence=data.get("model_confidence", 0.0),
            upc=data.get("upc"),
            vin=data.get("vin"),
            lot=data.get("lot"),
            missing_fields=missing,
            disambiguation_questions=self._generate_questions(missing),
            source_artifacts=[{"type": "text", "content": data.get("raw_query", "")}]
        )

    def _generate_questions(self, missing: List[str]) -> List[str]:
        """Generate questions for missing fields"""
        questions = []
        if "brand" in missing:
            questions.append("What is the brand or manufacturer name?")
        if "model" in missing:
            questions.append("What is the model number or product code?")
        return questions
