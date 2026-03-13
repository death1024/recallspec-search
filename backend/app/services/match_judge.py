from typing import Dict, Tuple, List, Literal
from ..models.specs import ProductIdentitySpec

class MatchJudge:
    """Score matches and classify into four states"""

    def judge_matches(
        self,
        identity_spec: ProductIdentitySpec,
        candidates: List[Dict]
    ) -> List[Dict]:
        """Score all candidates and return with match status"""
        scored = []
        for candidate in candidates:
            score, status = self._score_match(identity_spec, candidate)
            scored.append({
                "recall": candidate,
                "score": score,
                "match_status": status,
                "match_reasons": self._get_match_reasons(identity_spec, candidate)
            })

        # Sort by score descending
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored

    def _score_match(
        self,
        identity_spec: ProductIdentitySpec,
        recall: Dict
    ) -> Tuple[float, Literal["exact_match", "probable_match", "unresolved", "no_match"]]:
        """Calculate match score and determine status"""
        score = 0.0

        # Exact identifiers = instant exact_match
        if identity_spec.vin and recall.get("identifiers", {}).get("vin_pattern") == identity_spec.vin:
            return 1.0, "exact_match"

        if identity_spec.upc and identity_spec.upc in recall.get("identifiers", {}).get("upc", []):
            return 1.0, "exact_match"

        # Accumulate points for partial matches
        if identity_spec.brand and recall.get("brand"):
            if identity_spec.brand.lower() == recall["brand"].lower():
                score += 0.3

        if identity_spec.model and recall.get("model"):
            if identity_spec.model.lower() == recall["model"].lower():
                score += 0.4

        if identity_spec.category and recall.get("category"):
            if identity_spec.category == recall["category"]:
                score += 0.1

        if identity_spec.lot and recall.get("identifiers", {}).get("lot"):
            if identity_spec.lot == recall["identifiers"]["lot"]:
                score += 0.1

        # Classify based on score
        if score >= 0.9:
            return score, "exact_match"
        elif score >= 0.6:
            return score, "probable_match"
        elif score >= 0.3:
            return score, "unresolved"
        else:
            return score, "no_match"

    def _get_match_reasons(self, identity_spec: ProductIdentitySpec, recall: Dict) -> List[str]:
        """Explain why this recall matched"""
        reasons = []

        if identity_spec.vin and recall.get("identifiers", {}).get("vin_pattern"):
            reasons.append("VIN exact match")

        if identity_spec.upc and identity_spec.upc in recall.get("identifiers", {}).get("upc", []):
            reasons.append("UPC exact match")

        if identity_spec.brand and recall.get("brand"):
            if identity_spec.brand.lower() == recall["brand"].lower():
                reasons.append("Brand match")

        if identity_spec.model and recall.get("model"):
            if identity_spec.model.lower() == recall["model"].lower():
                reasons.append("Model match")

        if identity_spec.category and recall.get("category"):
            if identity_spec.category == recall["category"]:
                reasons.append("Category match")

        return reasons
