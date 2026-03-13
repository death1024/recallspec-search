from pydantic import BaseModel, Field
from typing import Optional, Dict, Literal
from datetime import datetime, date
from uuid import UUID, uuid4

class Recall(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    authority: Literal["CPSC", "NHTSA", "FDA"]
    authority_record_id: str
    category: Literal["consumer_product", "vehicle", "food", "drug", "device"]
    product_name: str
    brand: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    identifiers: Dict = Field(default_factory=dict)  # upc, vin_pattern, lot, ndc
    hazard: str
    risk_level: Literal["high", "medium", "low"]
    recall_date: date
    remedy: str
    distribution: Optional[str] = None
    source_url: str
    full_text: str  # For search indexing
    ingested_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1
