from typing import List, Dict, Optional
from ..models.specs import RecallResolutionSpec, ActionCard, ProductIdentitySpec

class ResolutionSpecEngine:
    """Generate Recall Resolution Spec with action cards"""

    def generate_resolution(
        self,
        identity_spec: ProductIdentitySpec,
        scored_matches: List[Dict]
    ) -> RecallResolutionSpec:
        """Create resolution spec from scored matches"""

        if not scored_matches:
            return self._create_no_match_resolution(identity_spec)

        top_match = scored_matches[0]
        match_status = top_match["match_status"]

        return RecallResolutionSpec(
            identity_spec_id=identity_spec.id,
            match_status=match_status,
            primary_authority=top_match["recall"].get("authority"),
            candidate_records=[
                {
                    "recall_id": m["recall"].get("authority_record_id"),
                    "score": m["score"],
                    "match_reasons": m["match_reasons"]
                }
                for m in scored_matches[:5]
            ],
            evidence=self._build_evidence(scored_matches[:3]),
            action_card=self._generate_action_card(match_status, top_match["recall"], identity_spec),
            risk_level=top_match["recall"].get("risk_level", "unknown"),
            uncertainties=self._identify_uncertainties(match_status, identity_spec)
        )

    def _create_no_match_resolution(self, identity_spec: ProductIdentitySpec) -> RecallResolutionSpec:
        """Create resolution for no matches found"""
        return RecallResolutionSpec(
            identity_spec_id=identity_spec.id,
            match_status="no_match",
            risk_level="unknown",
            action_card=ActionCard(
                immediate_action="No recalls found in current database",
                next_steps=["Verify product information", "Check official recall websites directly"],
                official_source="https://www.recalls.gov",
                risk_level="unknown"
            ),
            uncertainties=["No matching recalls found as of search time"]
        )

    def _build_evidence(self, matches: List[Dict]) -> List[Dict]:
        """Build evidence chain from matches"""
        return [
            {
                "authority": m["recall"].get("authority"),
                "record_ref": m["recall"].get("authority_record_id"),
                "matched_fields": m["match_reasons"]
            }
            for m in matches
        ]

    def _generate_action_card(
        self,
        match_status: str,
        recall: Dict,
        identity_spec: ProductIdentitySpec
    ) -> ActionCard:
        """Generate action card from official remedy"""

        if match_status == "exact_match":
            immediate = "STOP USING THIS PRODUCT IMMEDIATELY" if recall.get("risk_level") == "high" else "Check recall details"
            steps = [recall.get("remedy", "Contact manufacturer")]
        elif match_status == "probable_match":
            immediate = "Verify product details before taking action"
            steps = [
                f"Check product for: {', '.join(identity_spec.missing_fields)}",
                "Compare with recall details",
                recall.get("remedy", "Contact manufacturer if match confirmed")
            ]
        else:
            immediate = "Unable to confirm match"
            steps = [f"Please provide: {', '.join(identity_spec.missing_fields)}"]

        return ActionCard(
            immediate_action=immediate,
            next_steps=steps,
            official_source=recall.get("source_url", "https://www.recalls.gov"),
            risk_level=recall.get("risk_level", "unknown")
        )

    def _identify_uncertainties(self, match_status: str, identity_spec: ProductIdentitySpec) -> List[str]:
        """Identify what's uncertain about the match"""
        uncertainties = []

        if match_status in ["probable_match", "unresolved"]:
            if identity_spec.missing_fields:
                uncertainties.append(f"Missing fields: {', '.join(identity_spec.missing_fields)}")

        return uncertainties
