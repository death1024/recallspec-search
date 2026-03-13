from sqlalchemy.orm import Session
from uuid import UUID
import secrets
from datetime import datetime, timedelta
from ..models.share import ShareTokenDB

class ShareService:
    """Manage shareable result links"""

    def create_share_token(self, db: Session, resolution_spec_id: UUID, resolution_data: dict) -> str:
        """Create shareable token for resolution spec"""
        token = secrets.token_urlsafe(32)
        share = ShareTokenDB(
            token=token,
            resolution_spec_id=resolution_spec_id,
            resolution_data=resolution_data,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.add(share)
        db.commit()
        return token

    def get_by_token(self, db: Session, token: str):
        """Retrieve resolution spec by share token"""
        share = db.query(ShareTokenDB).filter(ShareTokenDB.token == token).first()
        if share and (not share.expires_at or share.expires_at > datetime.utcnow()):
            return share.resolution_data
        return None
