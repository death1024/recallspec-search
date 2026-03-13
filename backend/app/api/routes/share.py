from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from uuid import UUID
from sqlalchemy.orm import Session
from ...services.share import ShareService
from ...db.postgres import get_db

router = APIRouter(prefix="/api/v1/share", tags=["share"])

class ShareRequest(BaseModel):
    resolution_spec_id: UUID
    resolution_data: dict

@router.post("/")
async def create_share(request: ShareRequest, db: Session = Depends(get_db)):
    """Create shareable link for resolution spec"""
    service = ShareService()
    token = service.create_share_token(db, request.resolution_spec_id, request.resolution_data)
    return {"share_url": f"/share/{token}", "token": token}

@router.get("/{token}")
async def get_shared_result(token: str, db: Session = Depends(get_db)):
    """Get shared resolution spec by token"""
    service = ShareService()
    data = service.get_by_token(db, token)
    if not data:
        raise HTTPException(status_code=404, detail="Share link not found or expired")
    return data
