import finnhub
from app.config import settings
from typing import Dict, Any

class StockService:
    def __init__(self):
        self.client = finnhub.Client(api_key=settings.FINNHUB_API_KEY)

    async def get_stock_info(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch stock information for a given ticker.
        
        Args:
            ticker (str): Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Dict[str, Any]: Stock information including price and price change
        """
        try:
            # Get quote data from Finnhub
            quote = self.client.quote(ticker)
            
            return {
                "price": quote['c'],  # Current price
                "priceChange": quote['dp']  # Daily percentage change
            }
            
        except Exception as e:
            print(f"Error fetching stock info for {ticker}: {str(e)}")
            raise

# Create a singleton instance
stock_service = StockService() 