"""
Utilities for checking robots.txt compliance.
"""

import urllib.robotparser
from urllib.parse import urlparse
import logging


logger = logging.getLogger(__name__)


def check_robots_txt(url: str, user_agent: str = "*") -> bool:
    """
    Check if a URL can be scraped according to robots.txt.
    
    Args:
        url: The URL to check
        user_agent: The user agent string
        
    Returns:
        True if scraping is allowed, False otherwise
    """
    try:
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        can_fetch = rp.can_fetch(user_agent, url)
        
        if not can_fetch:
            logger.info(f"robots.txt disallows scraping: {url}")
        
        return can_fetch
    except Exception as e:
        logger.warning(f"Error checking robots.txt for {url}: {e}")
        # If we can't check robots.txt, err on the side of caution
        return True


def get_crawl_delay(url: str, user_agent: str = "*") -> float:
    """
    Get the crawl delay specified in robots.txt.
    
    Args:
        url: The URL to check
        user_agent: The user agent string
        
    Returns:
        Crawl delay in seconds (default: 1.0)
    """
    try:
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        delay = rp.crawl_delay(user_agent)
        return float(delay) if delay else 1.0
    except Exception as e:
        logger.warning(f"Error getting crawl delay for {url}: {e}")
        return 1.0

