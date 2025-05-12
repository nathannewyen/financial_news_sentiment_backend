from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch
from typing import Dict, Any, List
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        # Load pre-trained model and tokenizer
        self.model_name = "finiteautomata/bertweet-base-sentiment-analysis"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        
        # Move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Initialize pipeline
        self.analyzer = pipeline(
            "sentiment-analysis",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of a given text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, Any]: Sentiment analysis results
        """
        try:
            # Get sentiment prediction
            result = self.analyzer(text)[0]
            
            # Map labels to our format
            label_mapping = {
                'POS': 'positive',
                'NEG': 'negative',
                'NEU': 'neutral'
            }
            
            return {
                "label": label_mapping.get(result['label'], 'neutral'),
                "score": result['score'],
                "confidence": result['score']
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            return {
                "label": "neutral",
                "score": 0.0,
                "confidence": 0.0
            }

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze sentiment of multiple texts.
        
        Args:
            texts (List[str]): List of texts to analyze
            
        Returns:
            List[Dict[str, Any]]: List of sentiment analysis results
        """
        try:
            results = self.analyzer(texts)
            return [self.analyze_text(text) for text in texts]
        except Exception as e:
            print(f"Error in batch sentiment analysis: {str(e)}")
            return [{"label": "neutral", "score": 0.0, "confidence": 0.0} for _ in texts]

# Create singleton instance
sentiment_analyzer = SentimentAnalyzer() 