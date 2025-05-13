import os
import finnhub
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinancialNewsCollector:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('FINNHUB_API_KEY')
        if not self.api_key:
            raise ValueError("FINNHUB_API_KEY not found in environment variables")
        
        logger.info("Initializing Finnhub client...")
        self.client = finnhub.Client(api_key=self.api_key)
        
    def collect_news(self, days_back: int = 30) -> pd.DataFrame:
        """
        Collect financial news articles from Finnhub.
        
        Args:
            days_back (int): Number of days to look back for news
            
        Returns:
            pd.DataFrame: DataFrame containing news articles and their metadata
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        logger.info(f"Collecting news from {start_date} to {end_date}")
        
        # Get news from major financial categories
        categories = [
            'general',
            'forex',
            'crypto',
            'merger'
        ]
        
        all_articles = []
        
        for category in categories:
            try:
                logger.info(f"Fetching news for category: {category}")
                # Get news for the category
                news = self.client.general_news(category, min_id=0)
                
                if not news:
                    logger.warning(f"No news found for category: {category}")
                    continue
                
                # Filter by date
                filtered_news = [
                    article for article in news
                    if datetime.fromtimestamp(article['datetime']) >= start_date
                ]
                
                logger.info(f"Found {len(filtered_news)} articles for category {category}")
                all_articles.extend(filtered_news)
                
            except Exception as e:
                logger.error(f"Error collecting news from category {category}: {str(e)}")
        
        if not all_articles:
            raise ValueError("No articles collected")
        
        logger.info(f"Total articles collected: {len(all_articles)}")
        
        # Convert to DataFrame
        df = pd.DataFrame(all_articles)
        
        # Keep only relevant columns and rename them
        df = df[['headline', 'summary', 'category', 'datetime']]
        df.columns = ['title', 'description', 'category', 'publishedAt']
        
        # Combine title and description for better context
        df['text'] = df['title'] + ' ' + df['description'].fillna('')
        
        # Add placeholder labels
        df['label'] = 'neutral'  # Default label
        
        # Save raw data
        self._save_raw_data(df)
        
        return df
    
    def _save_raw_data(self, df: pd.DataFrame):
        """Save raw collected data to a JSON file"""
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(data_dir, f"raw_news_{timestamp}.json")
        
        df.to_json(filepath, orient='records', indent=2)
        logger.info(f"Raw data saved to {filepath}")
    
    def label_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Label the collected data using a pre-trained model for initial labeling.
        This is a starting point - manual review and correction will be needed.
        """
        logger.info("Starting data labeling process...")
        from .sentiment_analyzer import sentiment_analyzer
        
        # Get initial sentiment predictions
        predictions = []
        total = len(df)
        
        for idx, text in enumerate(df['text'], 1):
            try:
                result = sentiment_analyzer.analyze_text(text)
                predictions.append(result['label'])
                if idx % 10 == 0:  # Log progress every 10 articles
                    logger.info(f"Labeled {idx}/{total} articles")
            except Exception as e:
                logger.error(f"Error labeling article {idx}: {str(e)}")
                predictions.append('neutral')  # Default to neutral on error
        
        df['label'] = predictions
        
        # Save labeled data
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(data_dir, f"labeled_news_{timestamp}.json")
        
        df.to_json(filepath, orient='records', indent=2)
        logger.info(f"Labeled data saved to {filepath}")
        
        return df

def main():
    collector = FinancialNewsCollector()
    
    try:
        # Collect news
        logger.info("Starting news collection...")
        df = collector.collect_news(days_back=30)
        
        # Label data
        logger.info("Starting data labeling...")
        labeled_df = collector.label_data(df)
        
        logger.info(f"Successfully collected and labeled {len(labeled_df)} articles")
        
    except Exception as e:
        logger.error(f"Error in data collection: {str(e)}")
        raise

if __name__ == "__main__":
    main() 