import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime, timedelta

class TrendAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)

    def analyze_sentiment_trends(self, sentiment_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze sentiment trends over time.
        
        Args:
            sentiment_data (List[Dict[str, Any]]): List of sentiment data points
            
        Returns:
            Dict[str, Any]: Trend analysis results
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame(sentiment_data)
            
            # Calculate basic statistics
            stats = {
                "mean_sentiment": float(df["score"].mean()),
                "sentiment_volatility": float(df["score"].std()),
                "trend_direction": self._calculate_trend_direction(df["score"]),
                "sentiment_distribution": {
                    "positive": float(df[df["label"] == "positive"].shape[0] / len(df)),
                    "negative": float(df[df["label"] == "negative"].shape[0] / len(df)),
                    "neutral": float(df[df["label"] == "neutral"].shape[0] / len(df))
                },
                "time_analysis": {
                    "daily_pattern": self._calculate_daily_pattern(df),
                    "weekly_pattern": self._calculate_weekly_pattern(df)
                }
            }
            
            return stats
            
        except Exception as e:
            print(f"Error in trend analysis: {str(e)}")
            # Return default structure if analysis fails
            return {
                "mean_sentiment": 0.0,
                "sentiment_volatility": 0.0,
                "trend_direction": "neutral",
                "sentiment_distribution": {
                    "positive": 0.0,
                    "negative": 0.0,
                    "neutral": 1.0
                },
                "time_analysis": {
                    "daily_pattern": {},
                    "weekly_pattern": {}
                }
            }

    def _calculate_trend_direction(self, scores: pd.Series) -> str:
        """Calculate the overall trend direction."""
        if len(scores) < 2:
            return "neutral"
        
        slope = np.polyfit(range(len(scores)), scores, 1)[0]
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        return "stable"

    def _calculate_sentiment_distribution(self, labels: pd.Series) -> Dict[str, float]:
        """Calculate the distribution of sentiment labels."""
        return labels.value_counts(normalize=True).to_dict()

    def _analyze_time_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze temporal patterns in sentiment."""
        df['datetime'] = pd.to_datetime(df['datetime'], unit='s')
        
        return {
            "daily_pattern": self._calculate_daily_pattern(df),
            "weekly_pattern": self._calculate_weekly_pattern(df)
        }

    def _calculate_daily_pattern(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate average sentiment by hour of day."""
        df['hour'] = df['datetime'].dt.hour
        return df.groupby('hour')['score'].mean().to_dict()

    def _calculate_weekly_pattern(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate average sentiment by day of week."""
        df['day'] = df['datetime'].dt.day_name()
        return df.groupby('day')['score'].mean().to_dict()

    def _perform_advanced_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform advanced statistical analysis."""
        try:
            # Only perform PCA if we have enough data points
            if len(df) > 2:
                # Perform PCA on sentiment scores
                scores_2d = self.pca.fit_transform(
                    self.scaler.fit_transform(df[["score"]])
                )
                
                return {
                    "pca_components": self.pca.components_.tolist(),
                    "explained_variance": self.pca.explained_variance_ratio_.tolist(),
                    "sentiment_clusters": self._identify_sentiment_clusters(scores_2d)
                }
            else:
                # Return simplified analysis for small datasets
                return {
                    "pca_components": [],
                    "explained_variance": [],
                    "sentiment_clusters": {
                        "cluster_centers": [],
                        "cluster_sizes": []
                    }
                }
        except Exception as e:
            print(f"Error in advanced analysis: {str(e)}")
            return {
                "pca_components": [],
                "explained_variance": [],
                "sentiment_clusters": {
                    "cluster_centers": [],
                    "cluster_sizes": []
                }
            }

    def _identify_sentiment_clusters(self, scores_2d: np.ndarray) -> Dict[str, Any]:
        """Identify clusters in sentiment data."""
        from sklearn.cluster import KMeans
        
        kmeans = KMeans(n_clusters=3)
        clusters = kmeans.fit_predict(scores_2d)
        
        return {
            "cluster_centers": kmeans.cluster_centers_.tolist(),
            "cluster_sizes": np.bincount(clusters).tolist()
        }

# Create singleton instance
trend_analyzer = TrendAnalyzer() 