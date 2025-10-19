"""
Sentiment analysis utilities.
"""

import logging
from typing import List

from commentradar.models import Comment


logger = logging.getLogger(__name__)


def analyze_sentiment(text: str) -> str:
    """
    Analyze the sentiment of a text.
    
    This is a placeholder implementation. In production, this would use:
    - TextBlob
    - VADER sentiment analyzer
    - Transformers (BERT-based models)
    - Cloud APIs (Google Cloud Natural Language, AWS Comprehend)
    
    Args:
        text: The text to analyze
        
    Returns:
        Sentiment label: 'positive', 'negative', or 'neutral'
    """
    # Simple keyword-based sentiment (placeholder)
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'best', 'awesome']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'poor', 'disappointing']
    
    text_lower = text.lower()
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'


def add_sentiment_to_comments(comments: List[Comment]) -> List[Comment]:
    """
    Add sentiment analysis to a list of comments.
    
    Args:
        comments: List of Comment objects
        
    Returns:
        List of Comment objects with sentiment added
    """
    for comment in comments:
        if not comment.sentiment:
            comment.sentiment = analyze_sentiment(comment.comment_text)
    
    logger.info(f"Added sentiment analysis to {len(comments)} comments")
    return comments

