from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.database.models import Watchlist
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class WatchlistCreate(BaseModel):
    symbol: str
    name: str
    price: float = None
    change: float = None
    user_id: int

@router.get("/watchlist")
def get_watchlist(user_id: int = Query(...), db: Session = Depends(get_db)):
    items = db.query(Watchlist).filter(Watchlist.user_id == user_id).all()
    return {
        "status": "success",
        "data": [
            {
                "symbol": item.symbol,
                "name": item.name,
                "price": item.price,
                "change": item.change,
            }
            for item in items
        ]
    }

@router.post("/watchlist")
def add_to_watchlist(watch: WatchlistCreate, db: Session = Depends(get_db)):
    # Check if already exists for this user
    existing = db.query(Watchlist).filter_by(symbol=watch.symbol, user_id=watch.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ticker already in watchlist for this user")
    item = Watchlist(
        symbol=watch.symbol,
        name=watch.name,
        price=watch.price,
        change=watch.change,
        user_id=watch.user_id
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"status": "success", "data": {
        "symbol": item.symbol,
        "name": item.name,
        "price": item.price,
        "change": item.change,
    }} 