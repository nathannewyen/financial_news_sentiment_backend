from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.services.stock_service import stock_service

router = APIRouter()

@router.get("/{ticker}", response_model=Dict[str, Any])
async def get_stock_info(ticker: str) -> Dict[str, Any]:
    """
    Fetch stock information for a given ticker.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL')
        
    Returns:
        Dict[str, Any]: Stock information with status
    """
    try:
        stock_info = await stock_service.get_stock_info(ticker)
        return {
            "status": "success",
            "data": stock_info
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching stock info for {ticker}: {str(e)}"
        ) 