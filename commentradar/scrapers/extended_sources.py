"""
Extended sources scraper: YouTube, Play Store, Stack Overflow, Product Hunt, Dev.to
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import List
import json
import re

from commentradar.models import Comment

logger = logging.getLogger(__name__)


class ExtendedSourcesScraper:
    """Scraper for additional high-value sources."""
    
    def __init__(self, topic: str):
        self.topic = topic
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_youtube_comments(self, limit=None) -> List[Comment]:
        """
        Scrape YouTube comments without API key using web scraping.
        For better results, use YouTube Data API with a free API key.
        """
        comments = []
        
        try:
            # Search for videos
            search_url = f"https://www.youtube.com/results?search_query={self.topic.replace(' ', '+')}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                # Extract video IDs from search results
                video_ids = re.findall(r'"videoId":"([^"]+)"', response.text)
                
                for video_id in video_ids[:5]:  # Check first 5 videos
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    
                    comment = Comment(
                        source_url=video_url,
                        platform="youtube",
                        commenter_name="YouTube Video",
                        comment_text=f"Video about {self.topic}",
                        date_posted=None
                    )
                    comments.append(comment)
                    
                    if limit and len(comments) >= limit:
                        break
                
                logger.info(f"✓ YouTube: {len(comments)} videos")
        
        except Exception as e:
            logger.error(f"YouTube scraping failed: {e}")
        
        return comments
    
    def scrape_play_store_reviews(self, limit=None) -> List[Comment]:
        """
        Scrape Google Play Store reviews by searching for apps.
        """
        comments = []
        
        try:
            # Search Play Store
            search_query = self.topic.replace(' ', '%20')
            search_url = f"https://play.google.com/store/search?q={search_query}&c=apps"
            
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find app listings
                app_elements = soup.find_all('a', href=re.compile(r'/store/apps/details'))
                
                for app_elem in app_elements[:10]:  # First 10 apps
                    try:
                        app_name = app_elem.get_text(strip=True)
                        app_url = "https://play.google.com" + app_elem.get('href', '')
                        
                        if app_name and len(app_name) > 3:
                            comment = Comment(
                                source_url=app_url,
                                platform="playstore",
                                commenter_name="Play Store",
                                comment_text=f"App: {app_name}",
                                date_posted=None
                            )
                            comments.append(comment)
                            
                            if limit and len(comments) >= limit:
                                break
                    except:
                        continue
                
                logger.info(f"✓ Play Store: {len(comments)} apps")
        
        except Exception as e:
            logger.error(f"Play Store scraping failed: {e}")
        
        return comments
    
    def scrape_stackoverflow(self, limit=None) -> List[Comment]:
        """
        Scrape Stack Overflow questions using their public API.
        """
        comments = []
        
        try:
            # Stack Overflow API (no auth required)
            api_url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=relevance&intitle={self.topic}&site=stackoverflow"
            
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                for item in items:
                    comment = Comment(
                        source_url=item.get('link', ''),
                        platform="stackoverflow",
                        commenter_name=item.get('owner', {}).get('display_name', 'SO User'),
                        comment_text=f"{item.get('title', '')} - {item.get('body_markdown', '')[:300]}",
                        date_posted=str(item.get('creation_date', '')),
                        likes=item.get('score', 0)
                    )
                    
                    if len(comment.comment_text.strip()) > 20:
                        comments.append(comment)
                    
                    if limit and len(comments) >= limit:
                        break
                
                logger.info(f"✓ Stack Overflow: {len(comments)} questions")
        
        except Exception as e:
            logger.error(f"Stack Overflow scraping failed: {e}")
        
        return comments
    
    def scrape_producthunt(self, limit=None) -> List[Comment]:
        """
        Scrape Product Hunt posts.
        """
        comments = []
        
        try:
            # Product Hunt website scraping (they have GraphQL but we'll use web)
            search_url = f"https://www.producthunt.com/search?q={self.topic.replace(' ', '%20')}"
            
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find product listings
                products = soup.find_all(['div', 'article'], limit=limit if limit else 20)
                
                for product in products:
                    try:
                        # Try to extract product info
                        title_elem = product.find(['h3', 'h2', 'a'])
                        desc_elem = product.find('p')
                        
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            description = desc_elem.get_text(strip=True) if desc_elem else ""
                            
                            link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                            if link and not link.startswith('http'):
                                link = f"https://www.producthunt.com{link}"
                            
                            if len(title) > 5:
                                comment = Comment(
                                    source_url=link or search_url,
                                    platform="producthunt",
                                    commenter_name="Product Hunt",
                                    comment_text=f"{title} - {description}"[:500],
                                    date_posted=None
                                )
                                comments.append(comment)
                                
                                if limit and len(comments) >= limit:
                                    break
                    except:
                        continue
                
                logger.info(f"✓ Product Hunt: {len(comments)} products")
        
        except Exception as e:
            logger.error(f"Product Hunt scraping failed: {e}")
        
        return comments
    
    def scrape_devto(self, limit=None) -> List[Comment]:
        """
        Scrape Dev.to articles using their public API.
        """
        comments = []
        
        try:
            # Dev.to has a free public API
            api_url = f"https://dev.to/api/articles?tag={self.topic.replace(' ', '-')}&per_page=30"
            
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                articles = response.json()
                
                for article in articles:
                    comment = Comment(
                        source_url=article.get('url', ''),
                        platform="devto",
                        commenter_name=article.get('user', {}).get('name', 'Dev.to User'),
                        comment_text=f"{article.get('title', '')} - {article.get('description', '')}"[:500],
                        date_posted=article.get('published_at', ''),
                        likes=article.get('positive_reactions_count', 0)
                    )
                    
                    if len(comment.comment_text.strip()) > 20:
                        comments.append(comment)
                    
                    if limit and len(comments) >= limit:
                        break
                
                logger.info(f"✓ Dev.to: {len(comments)} articles")
        
        except Exception as e:
            logger.error(f"Dev.to scraping failed: {e}")
        
        return comments
    
    def scrape_all(self, limit_per_source=None) -> List[Comment]:
        """Scrape from all extended sources."""
        import time
        
        all_comments = []
        
        logger.info(f"Scraping extended sources for: {self.topic}")
        
        all_comments.extend(self.scrape_youtube_comments(limit=limit_per_source))
        time.sleep(1)
        
        all_comments.extend(self.scrape_play_store_reviews(limit=limit_per_source))
        time.sleep(1)
        
        all_comments.extend(self.scrape_stackoverflow(limit=limit_per_source))
        time.sleep(1)
        
        all_comments.extend(self.scrape_producthunt(limit=limit_per_source))
        time.sleep(1)
        
        all_comments.extend(self.scrape_devto(limit=limit_per_source))
        
        return all_comments

