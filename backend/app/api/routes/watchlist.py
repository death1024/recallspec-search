from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from ...services.watchlist import WatchlistService
from ...db.postgres import get_db

router = APIRouter(prefix="/api/v1/watchlist", tags=["watchlist"])

class WatchlistItem(BaseModel):
    identity_spec_id: UUID
    item_name: str
    category: str

@router.post("/")
async def add_to_watchlist(item: WatchlistItem, db: Session = Depends(get_db)):
    """Add item to watchlist"""
    service = WatchlistService()
    user_id = uuid4()  # TODO: Get from auth
    result = service.add_item(db, user_id, item.identity_spec_id, item.item_name, item.category)
    return {"id": str(result.id), "message": "Item added to watchlist"}

@router.get("/")
async def get_watchlist(db: Session = Depends(get_db)):
    """Get all watchlist items"""
    service = WatchlistService()
    user_id = uuid4()  # TODO: Get from auth
    items = service.get_items(db, user_id)
    return {"items": [{"id": str(i.id), "name": i.item_name, "category": i.category} for i in items]}

@router.delete("/{item_id}")
async def remove_from_watchlist(item_id: UUID, db: Session = Depends(get_db)):
    """Remove item from watchlist"""
    service = WatchlistService()
    service.remove_item(db, item_id)
    return {"message": "Item removed"}
