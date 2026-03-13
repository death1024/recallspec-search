from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from ..db.postgres import Base

class WatchlistItemDB(Base):
    __tablename__ = "watchlist_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    identity_spec_id = Column(UUID(as_uuid=True), nullable=False)
    item_name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    monitoring_active = Column(Boolean, default=True)
    last_checked_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
