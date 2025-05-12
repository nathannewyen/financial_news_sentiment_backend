from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.ml.trend_analyzer import trend_analyzer
from app.services.news_service import news_service

router = APIRouter()

@router.get("/trends/{ticker}")
async def get_sentiment_trends(ticker: str) -> Dict[str, Any]:
    """
    Get sentiment trend analysis for a ticker.
    """
    try:
        # Get news data
        news = await news_service.get_news(ticker)
        
        # Extract sentiment data
        sentiment_data = [
            {
                "score": article["sentiment"]["score"],
                "label": article["sentiment"]["label"],
                "datetime": article["datetime"]
            }
            for article in news
        ]
        
        # Analyze trends
        trends = trend_analyzer.analyze_sentiment_trends(sentiment_data)
        
        return {
            "status": "success",
            "data": trends
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing trends for {ticker}: {str(e)}"
        ) 