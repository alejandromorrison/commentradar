"""
Filtering utilities for comments.
"""

from typing import List, Optional
from datetime import datetime
import logging

from commentradar.models import Comment


logger = logging.getLogger(__name__)


def apply_filters(
    comments: List[Comment],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    sentiment: Optional[str] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None
) -> List[Comment]:
    """
    Apply various filters to a list of comments.
    
    Args:
        comments: List of Comment objects
        start_date: Filter comments after this date (ISO format)
        end_date: Filter comments before this date (ISO format)
        sentiment: Filter by sentiment (positive, negative, neutral)
        min_length: Minimum comment text length
        max_length: Maximum comment text length
        
    Returns:
        Filtered list of Comment objects
    """
    filtered = comments
    
    # Date filtering
    if start_date or end_date:
        filtered = filter_by_date(filtered, start_date, end_date)
    
    # Sentiment filtering
    if sentiment:
        filtered = filter_by_sentiment(filtered, sentiment)
    
    # Length filtering
    if min_length or max_length:
        filtered = filter_by_length(filtered, min_length, max_length)
    
    logger.info(f"Filtered {len(comments)} comments down to {len(filtered)}")
    return filtered


def filter_by_date(
    comments: List[Comment],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Comment]:
    """
    Filter comments by date range.
    
    Args:
        comments: List of Comment objects
        start_date: Start date (ISO format)
        end_date: End date (ISO format)
        
    Returns:
        Filtered list of Comment objects
    """
    filtered = []
    
    for comment in comments:
        if not comment.date_posted:
            continue
        
        try:
            # Simple string comparison for ISO dates
            if start_date and comment.date_posted < start_date:
                continue
            if end_date and comment.date_posted > end_date:
                continue
            
            filtered.append(comment)
        except Exception as e:
            logger.debug(f"Error filtering date for comment: {e}")
            continue
    
    return filtered


def filter_by_sentiment(comments: List[Comment], sentiment: str) -> List[Comment]:
    """
    Filter comments by sentiment.
    
    Args:
        comments: List of Comment objects
        sentiment: Sentiment to filter by (positive, negative, neutral)
        
    Returns:
        Filtered list of Comment objects
    """
    sentiment = sentiment.lower()
    return [c for c in comments if c.sentiment and c.sentiment.lower() == sentiment]


def filter_by_length(
    comments: List[Comment],
    min_length: Optional[int] = None,
    max_length: Optional[int] = None
) -> List[Comment]:
    """
    Filter comments by text length.
    
    Args:
        comments: List of Comment objects
        min_length: Minimum length
        max_length: Maximum length
        
    Returns:
        Filtered list of Comment objects
    """
    filtered = []
    
    for comment in comments:
        text_length = len(comment.comment_text)
        
        if min_length and text_length < min_length:
            continue
        if max_length and text_length > max_length:
            continue
        
        filtered.append(comment)
    
    return filtered

