"""
Blog scraper for extracting comments from blog posts.
"""

from typing import List, Optional
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
import re

from commentradar.scrapers.base import BaseScraper
from commentradar.models import Comment


logger = logging.getLogger(__name__)


class BlogScraper(BaseScraper):
    """Scraper for blog comments."""
    
    def get_platform_name(self) -> str:
        return "blog"
    
    def scrape(self) -> List[Comment]:
        """
        Scrape comments from blogs.
        
        This implementation searches for blogs related to the topic
        and extracts comments from them.
        """
        comments = []
        logger.info(f"Scraping blogs for topic: {self.topic}")
        
        # Step 1: Find blog posts related to the topic
        blog_urls = self._find_blog_posts()
        
        # Step 2: Extract comments from each blog post
        for url in blog_urls:
            if self.limit and len(comments) >= self.limit:
                break
            
            if not self.check_robots_permission(url):
                logger.warning(f"Robots.txt disallows scraping: {url}")
                continue
            
            page_comments = self._extract_comments_from_page(url)
            comments.extend(page_comments)
            
            # Rate limiting
            self.rate_limit(1.5)
        
        # Apply limit
        if self.limit:
            comments = comments[:self.limit]
        
        logger.info(f"Found {len(comments)} blog comments")
        return comments
    
    def _find_blog_posts(self) -> List[str]:
        """
        Find blog posts related to the topic.
        
        In a production environment, this would use a search API
        or a predefined list of blog URLs.
        """
        # Example blog URLs - in production, this would search for real blogs
        # For demonstration, returning sample blog structure
        example_blogs = [
            f"https://example-blog.com/posts/{self.topic.replace(' ', '-')}",
            f"https://tech-blog.com/articles/{self.topic.replace(' ', '-')}",
        ]
        
        logger.info(f"Found {len(example_blogs)} potential blog posts")
        return example_blogs
    
    def _extract_comments_from_page(self, url: str) -> List[Comment]:
        """
        Extract comments from a single blog page.
        
        Args:
            url: The blog post URL
            
        Returns:
            List of Comment objects
        """
        comments = []
        
        html = self.fetch_page(url)
        if not html:
            return comments
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Common comment selectors (adapt based on actual blog structure)
        comment_selectors = [
            {'class': 'comment'},
            {'class': 'comment-body'},
            {'class': 'user-comment'},
            {'id': re.compile(r'comment-\d+')},
        ]
        
        for selector in comment_selectors:
            comment_elements = soup.find_all('div', selector)
            
            for element in comment_elements:
                try:
                    comment = self._parse_comment_element(element, url)
                    if comment:
                        comments.append(comment)
                except Exception as e:
                    logger.debug(f"Failed to parse comment element: {e}")
                    continue
        
        return comments
    
    def _parse_comment_element(self, element, source_url: str) -> Optional[Comment]:
        """
        Parse a comment element into a Comment object.
        
        Args:
            element: BeautifulSoup element containing the comment
            source_url: URL of the blog post
            
        Returns:
            Comment object or None
        """
        try:
            # Extract commenter name
            name_element = element.find(['span', 'div', 'p'], class_=re.compile(r'author|name|user'))
            commenter_name = name_element.get_text(strip=True) if name_element else "Anonymous"
            
            # Extract comment text
            text_element = element.find(['p', 'div'], class_=re.compile(r'text|content|body'))
            if not text_element:
                text_element = element
            comment_text = text_element.get_text(strip=True)
            
            if not comment_text or len(comment_text) < 5:
                return None
            
            # Extract date
            date_element = element.find(['time', 'span'], class_=re.compile(r'date|time'))
            date_posted = None
            if date_element:
                date_posted = date_element.get('datetime') or date_element.get_text(strip=True)
            
            return Comment(
                source_url=source_url,
                platform=self.get_platform_name(),
                commenter_name=commenter_name,
                comment_text=comment_text,
                date_posted=date_posted
            )
        except Exception as e:
            logger.debug(f"Failed to parse comment: {e}")
            return None

