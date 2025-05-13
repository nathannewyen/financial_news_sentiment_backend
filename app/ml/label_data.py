import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import os
from datetime import datetime

def get_db_connection():
    load_dotenv()
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def get_unlabeled_articles(limit=10):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT id, headline, content, published_at 
                FROM news_articles 
                WHERE id NOT IN (SELECT article_id FROM sentiment_analysis)
                ORDER BY published_at DESC
                LIMIT %s
            """, (limit,))
            return cur.fetchall()

def label_article(article_id, label, score, confidence):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sentiment_analysis 
                (article_id, label, score, confidence, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (article_id, label, score, confidence, datetime.utcnow()))
            conn.commit()

def main():
    while True:
        print("\n=== Financial News Labeling Tool ===")
        articles = get_unlabeled_articles()
        
        if not articles:
            print("No more articles to label!")
            break
            
        for article in articles:
            print(f"\nArticle ID: {article['id']}")
            print(f"Headline: {article['headline']}")
            print(f"Content: {article['content'][:200]}...")
            print(f"Published: {article['published_at']}")
            
            while True:
                label = input("\nEnter label (positive/negative/neutral) or 'skip': ").lower()
                if label in ['positive', 'negative', 'neutral', 'skip']:
                    break
                print("Invalid label! Please enter positive, negative, neutral, or skip")
            
            if label == 'skip':
                continue
                
            while True:
                try:
                    score = float(input("Enter sentiment score (-1 to 1): "))
                    if -1 <= score <= 1:
                        break
                    print("Score must be between -1 and 1")
                except ValueError:
                    print("Please enter a valid number")
            
            while True:
                try:
                    confidence = float(input("Enter confidence score (0 to 1): "))
                    if 0 <= confidence <= 1:
                        break
                    print("Confidence must be between 0 and 1")
                except ValueError:
                    print("Please enter a valid number")
            
            label_article(article['id'], label, score, confidence)
            print("Article labeled successfully!")
            
        if input("\nContinue labeling? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()
