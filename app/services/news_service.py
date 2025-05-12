from datetime import datetime
from typing import List, Dict, Any

import finnhub
from sqlalchemy.orm import Session

from app.config import settings
from app.database.database import SessionLocal
from app.database.models import NewsArticle, SentimentAnalysis
from app.ml.sentiment_analyzer import sentiment_analyzer

class NewsService:
    def __init__(self):
        self.client = finnhub.Client(api_key=settings.FINNHUB_API_KEY)

    async def get_news(self, ticker: str) -> List[Dict[str, Any]]:
        """
        Fetch news for a given ticker from Finnhub and store in database
        """
        try:
            # Fetch news from Finnhub
            news = self.client.company_news(ticker, _from="2024-01-01", to=datetime.now().strftime("%Y-%m-%d"))
            
            # Transform and analyze sentiment
            transformed_news = []
            for article in news:
                # Analyze sentiment
                sentiment = sentiment_analyzer.analyze_text(article['headline'])
                
                transformed_article = {
                    "headline": article['headline'],
                    "url": article['url'],
                    "datetime": article['datetime'],
                    "source": article['source'],
                    "content": article.get('summary', ''),
                    "sentiment": sentiment
                }
                transformed_news.append(transformed_article)
            
            # Store in database
            with SessionLocal() as db:
                self._store_news(db, transformed_news, ticker)
            
            return transformed_news
            
        except Exception as e:
            print(f"Error fetching news for {ticker}: {str(e)}")
            raise

    def _store_news(self, db: Session, news: List[Dict[str, Any]], ticker: str) -> None:
        """Store news articles in the database."""
        for article in news:
            if not self._article_exists(db, article['url']):
                new_article = self._create_article(db, article, ticker)
                self._create_sentiment(db, new_article.id)

    def _article_exists(self, db: Session, url: str) -> bool:
        """Check if an article already exists in the database."""
        return db.query(NewsArticle).filter(NewsArticle.url == url).first() is not None

    def _create_article(self, db: Session, article: Dict[str, Any], ticker: str) -> NewsArticle:
        """Create a new article in the database."""
        new_article = NewsArticle(
            headline=article['headline'],
            url=article['url'],
            source=article['source'],
            published_at=datetime.fromtimestamp(article['datetime']),
            ticker=ticker,
            content=article.get('content', '')
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        return new_article

    def _create_sentiment(self, db: Session, article_id: int) -> None:
        """Create a placeholder sentiment analysis for an article."""
        sentiment = SentimentAnalysis(
            article_id=article_id,
            score=0.0,
            label="neutral",
            confidence=0.0
        )
        db.add(sentiment)
        db.commit()

# Create a singleton instance
news_service = NewsService()
