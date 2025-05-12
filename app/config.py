from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:your_password@localhost:5432/financial_news")
    
    # API Keys
    FINNHUB_API_KEY: str = os.getenv("FINNHUB_API_KEY", "")
    
    # Model settings
    MODEL_PATH: str = "app/ml/models/sentiment_model.pkl"
    
    class Config:
        env_file = ".env"

settings = Settings()