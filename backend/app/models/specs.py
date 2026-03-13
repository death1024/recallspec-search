from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal
from datetime import datetime
from uuid import UUID, uuid4

class ProductIdentitySpec(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    status: Literal["complete", "partial", "minimal"]
    category: Optional[str] = None
    brand: Optional[str] = None
    brand_confidence: float = 0.0
    model: Optional[str] = None
    model_confidence: float = 0.0
    upc: Optional[str] = None
    vin: Optional[str] = None
    lot: Optional[str] = None
    batch: Optional[str] = None
    serial: Optional[str] = None
    purchase_date: Optional[str] = None
    source_artifacts: List[Dict] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)
    disambiguation_questions: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ActionCard(BaseModel):
    immediate_action: str
    next_steps: List[str]
    contact_info: Optional[Dict] = None
    required_info: List[str] = Field(default_factory=list)
    official_source: str
    risk_level: Literal["high", "medium", "low", "unknown"]

class RecallResolutionSpec(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    identity_spec_id: UUID
    match_status: Literal["exact_match", "probable_match", "unresolved", "no_match"]
    primary_authority: Optional[str] = None
    candidate_records: List[Dict] = Field(default_factory=list)
    evidence: List[Dict] = Field(default_factory=list)
    action_card: Optional[ActionCard] = None
    risk_level: Literal["high", "medium", "low", "unknown"]
    uncertainties: List[str] = Field(default_factory=list)
    last_verified_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
