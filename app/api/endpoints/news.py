from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.services.news_service import news_service

router = APIRouter()

@router.get("/{ticker}", response_model=Dict[str, Any])
async def fetch_news(ticker: str) -> Dict[str, Any]:
    """
    Fetch news for a given ticker symbol.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL')
        
    Returns:
        Dict[str, Any]: News data with status
        
    Raises:
        HTTPException: If there's an error fetching news
    """
    try:
        news = await news_service.get_news(ticker)
        return {
            "status": "success",
            "data": news
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching news for {ticker}: {str(e)}"
        ) 