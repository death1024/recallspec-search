import httpx
from typing import List, Dict, Optional
from datetime import datetime
from ..models.recalls import Recall

class NHTSAAdapter:
    BASE_URL = "https://api.nhtsa.gov/recalls/recallsByVehicle"

    async def fetch_recalls_by_vin(self, vin: str) -> List[Recall]:
        """Fetch recalls for specific VIN"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.BASE_URL}?vin={vin}")
            response.raise_for_status()
            data = response.json()

        recalls = []
        for item in data.get("results", []):
            recall = self._normalize_recall(item, vin)
            if recall:
                recalls.append(recall)
        return recalls

    async def fetch_recalls_by_make_model(self, make: str, model: str, year: int) -> List[Recall]:
        """Fetch recalls by vehicle make/model/year"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}?make={make}&model={model}&modelYear={year}"
            )
            response.raise_for_status()
            data = response.json()

        recalls = []
        for item in data.get("results", []):
            recall = self._normalize_recall(item)
            if recall:
                recalls.append(recall)
        return recalls

    def _normalize_recall(self, raw: Dict, vin: Optional[str] = None) -> Recall:
        """Convert NHTSA format to unified Recall model"""
        try:
            return Recall(
                authority="NHTSA",
                authority_record_id=raw.get("NHTSACampaignNumber", ""),
                category="vehicle",
                product_name=f"{raw.get('Make', '')} {raw.get('Model', '')} {raw.get('ModelYear', '')}",
                brand=raw.get("Make", ""),
                manufacturer=raw.get("Manufacturer", ""),
                model=raw.get("Model", ""),
                identifiers={"vin_pattern": vin} if vin else {},
                hazard=raw.get("Consequence", ""),
                risk_level=self._assess_risk(raw.get("Consequence", "")),
                recall_date=datetime.strptime(raw.get("ReportReceivedDate", ""), "%Y%m%d").date(),
                remedy=raw.get("Remedy", ""),
                distribution="",
                source_url=f"https://www.nhtsa.gov/recalls?nhtsaId={raw.get('NHTSACampaignNumber', '')}",
                full_text=f"{raw.get('Make', '')} {raw.get('Model', '')} {raw.get('Component', '')} {raw.get('Consequence', '')}"
            )
        except Exception:
            return None

    def _assess_risk(self, consequence: str) -> str:
        """Risk assessment based on consequence"""
        consequence_lower = consequence.lower()
        if any(word in consequence_lower for word in ["crash", "fire", "death", "injury"]):
            return "high"
        elif any(word in consequence_lower for word in ["fail", "malfunction", "loss of control"]):
            return "medium"
        return "low"
