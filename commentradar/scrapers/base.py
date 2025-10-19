"""
Base scraper class that all platform scrapers inherit from.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import requests
from urllib.parse import urlparse
import time
import logging

from commentradar.models import Comment
from commentradar.utils.robots import check_robots_txt


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all platform scrapers."""
    
    def __init__(self, topic: str, limit: Optional[int] = None):
        """
        Initialize the scraper.
        
        Args:
            topic: The topic to search for
            limit: Maximum number of comments to scrape
        """
        self.topic = topic
        self.limit = limit
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CommentRadar/0.1.0 (Educational Purpose; +https://github.com/commentradar)'
        })
    
    @abstractmethod
    def scrape(self) -> List[Comment]:
        """
        Scrape comments from the platform.
        
        Returns:
            List of Comment objects
        """
        pass
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """Return the name of the platform."""
        pass
    
    def check_robots_permission(self, url: str) -> bool:
        """
        Check if scraping is allowed by robots.txt.
        
        Args:
            url: The URL to check
            
        Returns:
            True if allowed, False otherwise
        """
        try:
            return check_robots_txt(url, self.session.headers.get('User-Agent', '*'))
        except Exception as e:
            logger.warning(f"Could not check robots.txt for {url}: {e}")
            return False
    
    def rate_limit(self, delay: float = 1.0):
        """
        Implement rate limiting between requests.
        
        Args:
            delay: Time to wait in seconds
        """
        time.sleep(delay)
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a web page with error handling.
        
        Args:
            url: The URL to fetch
            
        Returns:
            Page content as string, or None if failed
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def close(self):
        """Close the session."""
        self.session.close()

