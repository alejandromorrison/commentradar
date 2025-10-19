"""
Real blog scraper that searches for actual blog posts and extracts real comments.
"""

from typing import List, Optional
from bs4 import BeautifulSoup
import logging
import re
from urllib.parse import urljoin, urlparse
import json

from commentradar.scrapers.base import BaseScraper
from commentradar.models import Comment


logger = logging.getLogger(__name__)


class RealBlogScraper(BaseScraper):
    """Scraper that finds real blog posts via search and extracts comments."""
    
    def get_platform_name(self) -> str:
        return "blog"
    
    def scrape(self) -> List[Comment]:
        """Scrape real comments from blog posts."""
        comments = []
        logger.info(f"Searching for real blogs about: {self.topic}")
        
        # Step 1: Find real blog posts
        blog_urls = self._search_real_blogs()
        
        if not blog_urls:
            logger.warning("No blog URLs found. Using fallback sources.")
            blog_urls = self._get_fallback_urls()
        
        # Step 2: Extract comments from each blog
        for url in blog_urls:
            if self.limit and len(comments) >= self.limit:
                break
            
            logger.info(f"Scraping: {url}")
            
            if not self.check_robots_permission(url):
                logger.warning(f"robots.txt disallows: {url}")
                continue
            
            page_comments = self._extract_comments_from_page(url)
            comments.extend(page_comments)
            
            # Rate limiting
            self.rate_limit(2.0)
        
        # Apply limit
        if self.limit:
            comments = comments[:self.limit]
        
        logger.info(f"Found {len(comments)} real blog comments")
        return comments
    
    def _search_real_blogs(self) -> List[str]:
        """
        Search for real blog posts using DuckDuckGo (no API key needed).
        """
        try:
            from duckduckgo_search import DDGS
            
            search_query = f"{self.topic} blog"
            urls = []
            
            with DDGS() as ddgs:
                results = ddgs.text(search_query, max_results=10)
                for result in results:
                    url = result.get('href') or result.get('link')
                    if url and self._is_blog_url(url):
                        urls.append(url)
            
            logger.info(f"Found {len(urls)} potential blog URLs via search")
            return urls[:5]  # Limit to 5 blogs
            
        except ImportError:
            logger.warning("duckduckgo-search not installed. Install with: pip install duckduckgo-search")
            return []
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def _is_blog_url(self, url: str) -> bool:
        """Check if URL looks like a blog post."""
        blog_indicators = [
            '/blog/', '/post/', '/article/', '/news/',
            'medium.com', 'wordpress.com', 'blogger.com',
            'substack.com', 'ghost.io'
        ]
        url_lower = url.lower()
        return any(indicator in url_lower for indicator in blog_indicators)
    
    def _get_fallback_urls(self) -> List[str]:
        """
        Fallback URLs for specific topics when search fails.
        """
        if 'nutrition' in self.topic.lower() and 'saas' in self.topic.lower():
            # Nutrition SaaS related blogs and review sites
            return [
                "https://www.capterra.com/nutrition-software/",
                "https://www.softwareadvice.com/nutrition/",
                "https://alternativeto.net/category/health-and-fitness/nutrition/",
            ]
        
        return []
    
    def _extract_comments_from_page(self, url: str) -> List[Comment]:
        """Extract real comments from a blog page."""
        comments = []
        
        html = self.fetch_page(url)
        if not html:
            return comments
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try multiple comment section patterns
        comment_patterns = [
            # WordPress/Generic comments
            {'class': re.compile(r'comment(?!-reply)')},
            {'class': re.compile(r'comment-body')},
            {'class': re.compile(r'comment-content')},
            {'id': re.compile(r'comment-\d+')},
            
            # Disqus
            {'id': 'disqus_thread'},
            
            # WordPress specific
            {'class': 'comment-list'},
            
            # Medium
            {'class': re.compile(r'.*response.*')},
            
            # Generic
            {'class': re.compile(r'review')},
            {'class': re.compile(r'user-comment')},
            {'itemprop': 'comment'},
        ]
        
        for pattern in comment_patterns:
            elements = soup.find_all(['div', 'article', 'li'], pattern, limit=50)
            
            for element in elements:
                try:
                    comment = self._parse_comment_element(element, url)
                    if comment and comment.comment_text:
                        comments.append(comment)
                        
                        if self.limit and len(comments) >= self.limit:
                            break
                except Exception as e:
                    logger.debug(f"Failed to parse comment: {e}")
                    continue
            
            if comments:
                break  # Found comments with this pattern
        
        # If no comments found, try to extract reviews
        if not comments:
            comments = self._extract_reviews(soup, url)
        
        logger.info(f"Extracted {len(comments)} comments from {url}")
        return comments
    
    def _parse_comment_element(self, element, source_url: str) -> Optional[Comment]:
        """Parse a comment element into a Comment object."""
        try:
            # Extract author name
            author_selectors = [
                {'class': re.compile(r'.*author.*', re.I)},
                {'class': re.compile(r'.*user.*name.*', re.I)},
                {'class': re.compile(r'.*commenter.*', re.I)},
                {'itemprop': 'author'},
                {'rel': 'author'},
            ]
            
            author_name = "Anonymous"
            for selector in author_selectors:
                author_elem = element.find(['span', 'div', 'a', 'p', 'cite'], selector)
                if author_elem:
                    author_name = author_elem.get_text(strip=True)
                    break
            
            # Extract comment text
            text_selectors = [
                {'class': re.compile(r'.*comment.*text.*', re.I)},
                {'class': re.compile(r'.*comment.*content.*', re.I)},
                {'class': re.compile(r'.*comment.*body.*', re.I)},
                {'itemprop': 'text'},
                {'class': re.compile(r'.*description.*', re.I)},
            ]
            
            comment_text = ""
            for selector in text_selectors:
                text_elem = element.find(['p', 'div', 'span'], selector)
                if text_elem:
                    comment_text = text_elem.get_text(strip=True)
                    break
            
            # If no specific text element, get all text from element
            if not comment_text:
                # Remove author name and date elements first
                temp_elem = element.__copy__()
                for unwanted in temp_elem.find_all(['time', 'footer', 'header']):
                    unwanted.decompose()
                comment_text = temp_elem.get_text(strip=True)
            
            # Validate
            if not comment_text or len(comment_text) < 10:
                return None
            
            # Clean up author name
            if len(author_name) > 100:
                author_name = author_name[:100]
            
            # Extract date
            date_posted = None
            date_elem = element.find(['time', 'span'], {'class': re.compile(r'.*date.*', re.I)})
            if date_elem:
                date_posted = date_elem.get('datetime') or date_elem.get_text(strip=True)
            
            return Comment(
                source_url=source_url,
                platform=self.get_platform_name(),
                commenter_name=author_name,
                comment_text=comment_text[:1000],  # Limit length
                date_posted=date_posted
            )
        except Exception as e:
            logger.debug(f"Failed to parse comment element: {e}")
            return None
    
    def _extract_reviews(self, soup: BeautifulSoup, source_url: str) -> List[Comment]:
        """Extract reviews as comments (for review sites)."""
        comments = []
        
        # Try to find review sections
        review_patterns = [
            {'class': re.compile(r'.*review.*', re.I)},
            {'itemprop': 'review'},
            {'class': re.compile(r'.*testimonial.*', re.I)},
            {'class': re.compile(r'.*rating.*comment.*', re.I)},
        ]
        
        for pattern in review_patterns:
            reviews = soup.find_all(['div', 'article'], pattern, limit=20)
            
            for review in reviews:
                try:
                    # Extract reviewer name
                    author_elem = review.find(['span', 'div', 'p'], 
                                             {'class': re.compile(r'.*author.*|.*name.*', re.I)})
                    author_name = author_elem.get_text(strip=True) if author_elem else "Reviewer"
                    
                    # Extract review text
                    text_elem = review.find(['p', 'div'], 
                                           {'class': re.compile(r'.*text.*|.*content.*|.*body.*', re.I)})
                    if not text_elem:
                        text_elem = review.find('p')
                    
                    if text_elem:
                        review_text = text_elem.get_text(strip=True)
                        
                        if len(review_text) >= 10:
                            comment = Comment(
                                source_url=source_url,
                                platform=self.get_platform_name(),
                                commenter_name=author_name,
                                comment_text=review_text[:1000],
                                date_posted=None
                            )
                            comments.append(comment)
                except Exception as e:
                    logger.debug(f"Failed to parse review: {e}")
                    continue
        
        return comments

