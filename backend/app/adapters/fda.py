import httpx
from typing import List, Dict
from datetime import datetime, timedelta
from ..models.recalls import Recall

class FDAAdapter:
    BASE_URL = "https://api.fda.gov"

    async def fetch_drug_recalls(self, days_back: int = 730) -> List[Recall]:
        """Fetch drug enforcement reports from FDA"""
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/drug/enforcement.json",
                params={"search": f"report_date:[{start_date} TO 99991231]", "limit": 100}
            )
            response.raise_for_status()
            data = response.json()

        recalls = []
        for item in data.get("results", []):
            recall = self._normalize_recall(item, "drug")
            if recall:
                recalls.append(recall)
        return recalls

    async def fetch_device_recalls(self, days_back: int = 730) -> List[Recall]:
        """Fetch device enforcement reports from FDA"""
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/device/enforcement.json",
                params={"search": f"report_date:[{start_date} TO 99991231]", "limit": 100}
            )
            response.raise_for_status()
            data = response.json()

        recalls = []
        for item in data.get("results", []):
            recall = self._normalize_recall(item, "device")
            if recall:
                recalls.append(recall)
        return recalls

    def _normalize_recall(self, raw: Dict, category: str) -> Recall:
        """Convert FDA format to unified Recall model"""
        try:
            return Recall(
                authority="FDA",
                authority_record_id=raw.get("recall_number", ""),
                category=category,
                product_name=raw.get("product_description", ""),
                brand="",
                manufacturer=raw.get("recalling_firm", ""),
                model="",
                identifiers={"code_info": raw.get("code_info", "")},
                hazard=raw.get("reason_for_recall", ""),
                risk_level=self._assess_risk(raw.get("classification", "")),
                recall_date=datetime.strptime(raw.get("report_date", ""), "%Y%m%d").date(),
                remedy=raw.get("product_quantity", ""),
                distribution=raw.get("distribution_pattern", ""),
                source_url=f"https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts",
                full_text=f"{raw.get('product_description', '')} {raw.get('reason_for_recall', '')}"
            )
        except Exception:
            return None

    def _assess_risk(self, classification: str) -> str:
        """Risk assessment based on FDA classification"""
        if classification == "Class I":
            return "high"
        elif classification == "Class II":
            return "medium"
        return "low"
