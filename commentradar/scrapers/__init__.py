"""
Scrapers module for different platforms.
"""

from commentradar.scrapers.base import BaseScraper
from commentradar.scrapers.blog_scraper import BlogScraper
from commentradar.scrapers.facebook_scraper import FacebookScraper
from commentradar.scrapers.instagram_scraper import InstagramScraper
from commentradar.scrapers.google_scraper import GoogleScraper

__all__ = [
    'BaseScraper',
    'BlogScraper',
    'FacebookScraper',
    'InstagramScraper',
    'GoogleScraper',
]

