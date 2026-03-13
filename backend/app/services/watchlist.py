from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime
from ..models.watchlist import WatchlistItemDB
from ..db.postgres import get_db

class WatchlistService:
    """Manage watchlist items with database persistence"""

    def add_item(self, db: Session, user_id: UUID, identity_spec_id: UUID, item_name: str, category: str):
        """Add item to watchlist"""
        item = WatchlistItemDB(
            user_id=user_id,
            identity_spec_id=identity_spec_id,
            item_name=item_name,
            category=category
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get_items(self, db: Session, user_id: UUID) -> List[WatchlistItemDB]:
        """Get all watchlist items for user"""
        return db.query(WatchlistItemDB).filter(
            WatchlistItemDB.user_id == user_id,
            WatchlistItemDB.monitoring_active == True
        ).all()

    def remove_item(self, db: Session, item_id: UUID):
        """Remove item from watchlist"""
        item = db.query(WatchlistItemDB).filter(WatchlistItemDB.id == item_id).first()
        if item:
            db.delete(item)
            db.commit()
        return item

    def update_check_time(self, db: Session, item_id: UUID):
        """Update last checked timestamp"""
        item = db.query(WatchlistItemDB).filter(WatchlistItemDB.id == item_id).first()
        if item:
            item.last_checked_at = datetime.utcnow()
            db.commit()
