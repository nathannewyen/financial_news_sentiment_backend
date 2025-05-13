from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String(500))
    url = Column(String(500))
    source = Column(String(100))
    published_at = Column(DateTime, default=datetime.utcnow)
    ticker = Column(String(10), index=True)  # Stock ticker symbol
    content = Column(Text, nullable=True)
    
    # Relationships
    sentiment_analysis = relationship("SentimentAnalysis", back_populates="article", cascade="all, delete-orphan")

class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("news_articles.id"))
    score = Column(Float)  # Sentiment score between -1 and 1
    label = Column(String(20))  # Positive, Negative, or Neutral
    confidence = Column(Float)  # Confidence score of the analysis
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    article = relationship("NewsArticle", back_populates="sentiment_analysis")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    watchlist = relationship("Watchlist", back_populates="user", cascade="all, delete-orphan")

class Watchlist(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=True)
    change = Column(Float, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="watchlist")
