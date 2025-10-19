"""
Manager for coordinating different scrapers.
"""

from typing import List, Optional
import logging

from commentradar.models import Comment, CommentCollection
from commentradar.scrapers import (
    BlogScraper,
    FacebookScraper,
    InstagramScraper,
    GoogleScraper
)
from commentradar.utils.sentiment import add_sentiment_to_comments
from commentradar.utils.filters import apply_filters


logger = logging.getLogger(__name__)


class ScraperManager:
    """Manages multiple scrapers and coordinates scraping operations."""
    
    PLATFORM_MAP = {
        'blog': BlogScraper,
        'facebook': FacebookScraper,
        'instagram': InstagramScraper,
        'google': GoogleScraper,
    }
    
    def __init__(self, topic: str, platforms: Optional[List[str]] = None, limit: Optional[int] = None):
        """
        Initialize the scraper manager.
        
        Args:
            topic: The topic to search for
            platforms: List of platforms to scrape (default: all)
            limit: Maximum number of comments per platform
        """
        self.topic = topic
        self.platforms = platforms or list(self.PLATFORM_MAP.keys())
        self.limit = limit
        self.collection = CommentCollection()
    
    def scrape_all(self) -> CommentCollection:
        """
        Scrape comments from all configured platforms.
        
        Returns:
            CommentCollection with all scraped comments
        """
        logger.info(f"Starting scrape for topic: '{self.topic}' on platforms: {self.platforms}")
        
        for platform in self.platforms:
            if platform not in self.PLATFORM_MAP:
                logger.warning(f"Unknown platform: {platform}")
                continue
            
            try:
                comments = self._scrape_platform(platform)
                self.collection.extend(comments)
                logger.info(f"Collected {len(comments)} comments from {platform}")
            except Exception as e:
                logger.error(f"Error scraping {platform}: {e}", exc_info=True)
                continue
        
        logger.info(f"Total comments collected: {len(self.collection)}")
        return self.collection
    
    def _scrape_platform(self, platform: str) -> List[Comment]:
        """
        Scrape a single platform.
        
        Args:
            platform: Platform name
            
        Returns:
            List of Comment objects
        """
        scraper_class = self.PLATFORM_MAP[platform]
        scraper = scraper_class(topic=self.topic, limit=self.limit)
        
        try:
            comments = scraper.scrape()
            return comments
        finally:
            scraper.close()
    
    def add_sentiment_analysis(self):
        """Add sentiment analysis to all collected comments."""
        add_sentiment_to_comments(self.collection.comments)
    
    def apply_filters(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sentiment: Optional[str] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ):
        """
        Apply filters to the collected comments.
        
        Args:
            start_date: Filter comments after this date
            end_date: Filter comments before this date
            sentiment: Filter by sentiment
            min_length: Minimum comment length
            max_length: Maximum comment length
        """
        self.collection.comments = apply_filters(
            self.collection.comments,
            start_date=start_date,
            end_date=end_date,
            sentiment=sentiment,
            min_length=min_length,
            max_length=max_length
        )
    
    def save_results(self, output_file: str):
        """
        Save the collected comments to a JSON file.
        
        Args:
            output_file: Path to output file
        """
        self.collection.save_to_file(output_file)
        logger.info(f"Saved {len(self.collection)} comments to {output_file}")

