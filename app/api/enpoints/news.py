from fastapi import APIRouter, HTTPException
from app.services.news_service import get_news

router = APIRouter()

@router.get("/{ticker}")
async def fetch_news(ticker: str):
    """
    Fetch news for a given ticker symbol
    """
    try:
        news = await get_news(ticker)
        return {"status": "success", "data": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))