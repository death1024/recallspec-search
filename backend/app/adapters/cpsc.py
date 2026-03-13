import httpx
from typing import List, Dict
from datetime import datetime, timedelta
from ..models.recalls import Recall

class CPSCAdapter:
    BASE_URL = "https://www.saferproducts.gov/RestWebServices"

    async def fetch_recalls(self, days_back: int = 1825) -> List[Recall]:
        """Fetch recalls from CPSC API (default: last 5 years)"""
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/Recall",
                params={"RecallDateStart": start_date, "format": "json"}
            )
            response.raise_for_status()
            data = response.json()

        recalls = []
        for item in data:
            recall = self._normalize_recall(item)
            if recall:
                recalls.append(recall)

        return recalls

    def _normalize_recall(self, raw: Dict) -> Recall:
        """Convert CPSC format to unified Recall model"""
        try:
            return Recall(
                authority="CPSC",
                authority_record_id=raw.get("RecallNumber", ""),
                category="consumer_product",
                product_name=raw.get("ProductName", ""),
                brand=raw.get("Manufacturer", ""),
                manufacturer=raw.get("Manufacturer", ""),
                model=raw.get("ModelNumber", ""),
                identifiers={"upc": raw.get("UPC", [])},
                hazard=raw.get("Hazard", ""),
                risk_level=self._assess_risk(raw.get("Hazard", "")),
                recall_date=datetime.strptime(raw.get("RecallDate", ""), "%Y-%m-%d").date(),
                remedy=raw.get("Remedy", ""),
                distribution=raw.get("Distribution", ""),
                source_url=raw.get("URL", ""),
                full_text=f"{raw.get('ProductName', '')} {raw.get('Manufacturer', '')} {raw.get('Hazard', '')}"
            )
        except Exception:
            return None

    def _assess_risk(self, hazard: str) -> str:
        """Simple risk assessment based on hazard keywords"""
        hazard_lower = hazard.lower()
        if any(word in hazard_lower for word in ["death", "fatal", "serious injury", "fire", "choking"]):
            return "high"
        elif any(word in hazard_lower for word in ["injury", "burn", "cut", "shock"]):
            return "medium"
        return "low"