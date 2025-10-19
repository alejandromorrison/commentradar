"""
Tests for data models.
"""

import json
import pytest
from commentradar.models import Comment, CommentCollection


def test_comment_creation():
    """Test creating a Comment object."""
    comment = Comment(
        source_url="https://example.com",
        platform="blog",
        commenter_name="Test User",
        comment_text="This is a test comment"
    )
    
    assert comment.source_url == "https://example.com"
    assert comment.platform == "blog"
    assert comment.commenter_name == "Test User"
    assert comment.comment_text == "This is a test comment"


def test_comment_to_dict():
    """Test converting Comment to dictionary."""
    comment = Comment(
        source_url="https://example.com",
        platform="blog",
        commenter_name="Test User",
        comment_text="Test"
    )
    
    data = comment.to_dict()
    assert isinstance(data, dict)
    assert data['source_url'] == "https://example.com"


def test_comment_to_json():
    """Test converting Comment to JSON."""
    comment = Comment(
        source_url="https://example.com",
        platform="blog",
        commenter_name="Test User",
        comment_text="Test"
    )
    
    json_str = comment.to_json()
    assert isinstance(json_str, str)
    
    # Verify it's valid JSON
    data = json.loads(json_str)
    assert data['platform'] == "blog"


def test_comment_collection():
    """Test CommentCollection functionality."""
    collection = CommentCollection()
    
    comment1 = Comment(
        source_url="https://example.com/1",
        platform="blog",
        commenter_name="User1",
        comment_text="Comment 1"
    )
    
    comment2 = Comment(
        source_url="https://example.com/2",
        platform="blog",
        commenter_name="User2",
        comment_text="Comment 2"
    )
    
    collection.add(comment1)
    collection.add(comment2)
    
    assert len(collection) == 2


def test_comment_collection_to_json():
    """Test converting CommentCollection to JSON."""
    collection = CommentCollection()
    
    comment = Comment(
        source_url="https://example.com",
        platform="blog",
        commenter_name="Test",
        comment_text="Test"
    )
    
    collection.add(comment)
    
    json_str = collection.to_json()
    assert isinstance(json_str, str)
    
    # Verify it's valid JSON
    data = json.loads(json_str)
    assert isinstance(data, list)
    assert len(data) == 1


def test_comment_collection_iteration():
    """Test iterating over CommentCollection."""
    collection = CommentCollection()
    
    for i in range(3):
        comment = Comment(
            source_url=f"https://example.com/{i}",
            platform="blog",
            commenter_name=f"User{i}",
            comment_text=f"Comment {i}"
        )
        collection.add(comment)
    
    count = 0
    for comment in collection:
        count += 1
    
    assert count == 3

