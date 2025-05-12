from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
import pandas as pd

# Load environment variables
load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load sentiment model
classifier = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

class HeadlineRequest(BaseModel):
    headline: str

class TickerRequest(BaseModel):
    ticker: str

@app.post("/analyze-headline")
async def analyze_headline(request: HeadlineRequest):
    try:
        result = classifier(request.headline)[0]
        return {
            "label": result['label'],
            "score": result['score']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stock-info")
async def get_stock_info(request: TickerRequest):
    try:
        stock = yf.Ticker(request.ticker)
        current_price = stock.info.get('regularMarketPrice', 'N/A')
        price_change = stock.info.get('regularMarketChangePercent', 0)
        
        return {
            "price": current_price,
            "priceChange": price_change
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/news")
async def get_news(request: TickerRequest):
    try:
        today = datetime.today().date()
        week_ago = today - timedelta(days=7)
        
        url = f"https://finnhub.io/api/v1/company-news?symbol={request.ticker.upper()}&from={week_ago}&to={today}&token={FINNHUB_API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            articles = response.json()
            if articles:
                processed_articles = []
                for article in articles[:5]:
                    sentiment = classifier(article['headline'])[0]
                    processed_articles.append({
                        "headline": article['headline'],
                        "url": article['url'],
                        "datetime": article['datetime'],
                        "sentiment": {
                            "label": sentiment['label'],
                            "score": sentiment['score']
                        }
                    })
                return processed_articles
            return []
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching news from Finnhub")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 