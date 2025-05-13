import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any
import glob

def list_data_files() -> list:
    """List all data files in the data directory"""
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(data_dir):
        print("No data directory found!")
        return []
    
    # Get all JSON files
    files = glob.glob(os.path.join(data_dir, "*.json"))
    return sorted(files, reverse=True)  # Most recent first

def load_latest_data() -> pd.DataFrame:
    """Load the most recent data file"""
    files = list_data_files()
    if not files:
        raise ValueError("No data files found!")
    
    latest_file = files[0]
    print(f"Loading data from: {os.path.basename(latest_file)}")
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    return pd.DataFrame(data)

def analyze_data(df: pd.DataFrame):
    """Analyze and display data statistics"""
    print("\n=== Data Analysis ===")
    print(f"Total articles: {len(df)}")
    
    # Label distribution
    if 'label' in df.columns:
        print("\nLabel Distribution:")
        print(df['label'].value_counts())
    
    # Category distribution
    if 'category' in df.columns:
        print("\nCategory Distribution:")
        print(df['category'].value_counts())
    
    # Date range
    if 'publishedAt' in df.columns:
        df['publishedAt'] = pd.to_datetime(df['publishedAt'])
        print("\nDate Range:")
        print(f"From: {df['publishedAt'].min()}")
        print(f"To: {df['publishedAt'].max()}")
    
    # Sample articles
    print("\nSample Articles:")
    for idx, row in df.head(3).iterrows():
        print(f"\nArticle {idx + 1}:")
        print(f"Title: {row['title']}")
        print(f"Category: {row.get('category', 'N/A')}")
        print(f"Label: {row.get('label', 'N/A')}")
        print(f"Published: {row.get('publishedAt', 'N/A')}")
        print("-" * 80)

def main():
    try:
        # Load the latest data
        df = load_latest_data()
        
        # Analyze and display the data
        analyze_data(df)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 