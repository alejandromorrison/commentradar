"""
Data models for CommentRadar.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


@dataclass
class Comment:
    """Represents a single comment from any platform."""
    
    source_url: str
    platform: str
    commenter_name: str
    comment_text: str
    date_posted: Optional[str] = None
    sentiment: Optional[str] = None
    likes: Optional[int] = None
    replies: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert comment to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert comment to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class CommentCollection:
    """Collection of comments with utility methods."""
    
    def __init__(self):
        self.comments: List[Comment] = []
    
    def add(self, comment: Comment):
        """Add a comment to the collection."""
        self.comments.append(comment)
    
    def extend(self, comments: List[Comment]):
        """Add multiple comments to the collection."""
        self.comments.extend(comments)
    
    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert all comments to a list of dictionaries."""
        return [comment.to_dict() for comment in self.comments]
    
    def to_json(self, indent: int = 2) -> str:
        """Convert all comments to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
    
    def save_to_file(self, filepath: str):
        """Save comments to a JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    def filter_by_date(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """Filter comments by date range."""
        if not start_date and not end_date:
            return self.comments
        
        filtered = []
        for comment in self.comments:
            if comment.date_posted:
                # Simple date comparison (assumes ISO format)
                if start_date and comment.date_posted < start_date:
                    continue
                if end_date and comment.date_posted > end_date:
                    continue
                filtered.append(comment)
        
        return filtered
    
    def filter_by_sentiment(self, sentiment: str):
        """Filter comments by sentiment (positive, negative, neutral)."""
        return [c for c in self.comments if c.sentiment == sentiment.lower()]
    
    def __len__(self):
        """Return the number of comments."""
        return len(self.comments)
    
    def __iter__(self):
        """Make the collection iterable."""
        return iter(self.comments)

