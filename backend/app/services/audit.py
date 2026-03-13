from sqlalchemy.orm import Session
from uuid import UUID
from ..models.share import AuditLogDB

class AuditService:
    """Audit logging for all operations"""

    def log(self, db: Session, user_id: UUID, action: str, entity_type: str, entity_id: UUID, details: dict = None):
        """Create audit log entry"""
        log = AuditLogDB(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details or {}
        )
        db.add(log)
        db.commit()
        return log
