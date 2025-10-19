"""
Tests for utility functions.
"""

import pytest
from commentradar.utils.sentiment import analyze_sentiment
from commentradar.utils.filters import filter_by_length, filter_by_sentiment
from commentradar.models import Comment


def test_analyze_sentiment_positive():
    """Test positive sentiment detection."""
    text = "This is a great and wonderful product! I love it!"
    sentiment = analyze_sentiment(text)
    assert sentiment == "positive"


def test_analyze_sentiment_negative():
    """Test negative sentiment detection."""
    text = "This is terrible and awful. I hate it!"
    sentiment = analyze_sentiment(text)
    assert sentiment == "negative"


def test_analyze_sentiment_neutral():
    """Test neutral sentiment detection."""
    text = "This is a product with features."
    sentiment = analyze_sentiment(text)
    assert sentiment == "neutral"


def test_filter_by_length():
    """Test filtering comments by length."""
    comments = [
        Comment("url1", "blog", "User1", "Short"),
        Comment("url2", "blog", "User2", "This is a much longer comment"),
        Comment("url3", "blog", "User3", "Medium text")
    ]
    
    # Filter by minimum length
    filtered = filter_by_length(comments, min_length=10)
    assert len(filtered) == 2
    
    # Filter by maximum length
    filtered = filter_by_length(comments, max_length=15)
    assert len(filtered) == 2


def test_filter_by_sentiment():
    """Test filtering comments by sentiment."""
    comments = [
        Comment("url1", "blog", "User1", "Text1", sentiment="positive"),
        Comment("url2", "blog", "User2", "Text2", sentiment="negative"),
        Comment("url3", "blog", "User3", "Text3", sentiment="positive")
    ]
    
    filtered = filter_by_sentiment(comments, "positive")
    assert len(filtered) == 2
    
    filtered = filter_by_sentiment(comments, "negative")
    assert len(filtered) == 1

