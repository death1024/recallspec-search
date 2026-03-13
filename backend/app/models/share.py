from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
from datetime import datetime
from ..db.postgres import Base

class ShareTokenDB(Base):
    __tablename__ = "share_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String(64), unique=True, nullable=False)
    resolution_spec_id = Column(UUID(as_uuid=True), nullable=False)
    resolution_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    action = Column(String(50), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True))
    details = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
