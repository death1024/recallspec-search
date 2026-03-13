from sqlalchemy import Column, String, DateTime, Integer, JSON, Date, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from ..db.postgres import Base

class RecallDB(Base):
    __tablename__ = "recalls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    authority = Column(String(20), nullable=False)
    authority_record_id = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    product_name = Column(Text, nullable=False)
    brand = Column(String(255))
    manufacturer = Column(String(255))
    model = Column(String(255))
    identifiers = Column(JSON, default={})
    hazard = Column(Text, nullable=False)
    risk_level = Column(String(20), nullable=False)
    recall_date = Column(Date, nullable=False)
    remedy = Column(Text, nullable=False)
    distribution = Column(Text)
    source_url = Column(Text, nullable=False)
    full_text = Column(Text, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow)
    version = Column(Integer, default=1)

class IdentitySpecDB(Base):
    __tablename__ = "identity_specs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    status = Column(String(20), nullable=False)
    category = Column(String(50))
    brand = Column(String(255))
    model = Column(String(255))
    identifiers = Column(JSON, default={})
    confidence_scores = Column(JSON, default={})
    missing_fields = Column(JSON, default=[])
    source_artifacts = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ResolutionSpecDB(Base):
    __tablename__ = "resolution_specs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identity_spec_id = Column(UUID(as_uuid=True), nullable=False)
    match_status = Column(String(20), nullable=False)
    candidate_records = Column(JSON, default=[])
    evidence = Column(JSON, default=[])
    action_card = Column(JSON)
    risk_level = Column(String(20), nullable=False)
    uncertainties = Column(JSON, default=[])
    last_verified_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
