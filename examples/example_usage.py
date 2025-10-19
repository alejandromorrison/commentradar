"""
Example usage of CommentRadar as a Python library.
"""

from commentradar.scraper_manager import ScraperManager
from commentradar.utils.sentiment import add_sentiment_to_comments


def example_basic_usage():
    """Basic usage example."""
    print("Example 1: Basic scraping")
    print("-" * 50)
    
    # Create a scraper manager
    manager = ScraperManager(
        topic="nutrition blogs",
        platforms=["blog"],
        limit=20
    )
    
    # Scrape comments
    collection = manager.scrape_all()
    
    # Print results
    print(f"Collected {len(collection)} comments")
    for comment in collection:
        print(f"- {comment.commenter_name}: {comment.comment_text[:50]}...")
    
    # Save to file
    manager.save_results("nutrition_comments.json")
    print("\nSaved to nutrition_comments.json")


def example_with_sentiment():
    """Example with sentiment analysis."""
    print("\nExample 2: With sentiment analysis")
    print("-" * 50)
    
    manager = ScraperManager(
        topic="restaurant reviews",
        platforms=["blog"],
        limit=10
    )
    
    # Scrape and add sentiment
    manager.scrape_all()
    manager.add_sentiment_analysis()
    
    # Filter positive comments
    manager.apply_filters(sentiment="positive")
    
    print(f"Found {len(manager.collection)} positive comments")
    manager.save_results("positive_reviews.json")


def example_multiple_platforms():
    """Example with multiple platforms."""
    print("\nExample 3: Multiple platforms")
    print("-" * 50)
    
    manager = ScraperManager(
        topic="travel apps",
        platforms=["blog", "google"],
        limit=15
    )
    
    collection = manager.scrape_all()
    
    # Group by platform
    platforms = {}
    for comment in collection:
        if comment.platform not in platforms:
            platforms[comment.platform] = []
        platforms[comment.platform].append(comment)
    
    for platform, comments in platforms.items():
        print(f"{platform}: {len(comments)} comments")
    
    manager.save_results("travel_comments.json")


def example_with_filters():
    """Example with various filters."""
    print("\nExample 4: With filters")
    print("-" * 50)
    
    manager = ScraperManager(
        topic="product feedback",
        platforms=["blog"],
        limit=50
    )
    
    manager.scrape_all()
    manager.add_sentiment_analysis()
    
    # Apply multiple filters
    manager.apply_filters(
        start_date="2024-01-01",
        min_length=50,
        max_length=500
    )
    
    print(f"Filtered down to {len(manager.collection)} comments")
    manager.save_results("filtered_feedback.json")


if __name__ == "__main__":
    # Run examples
    print("CommentRadar - Example Usage\n")
    
    try:
        example_basic_usage()
        # example_with_sentiment()
        # example_multiple_platforms()
        # example_with_filters()
    except Exception as e:
        print(f"Error: {e}")

