"""
Multi-source scraper for collecting data from various platforms.
Includes: Reddit, Hacker News, Product Hunt, Twitter/X, GitHub, Quora, Medium
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import List
import time
import json

from commentradar.models import Comment

logger = logging.getLogger(__name__)


class MultiSourceScraper:
    """Scraper that collects from multiple sources."""
    
    def __init__(self, topic: str):
        self.topic = topic
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_reddit(self, limit=None) -> List[Comment]:
        """Scrape Reddit using public JSON API."""
        comments = []
        
        try:
            # Reddit API max is 100 per request, default to 100 if unlimited
            api_limit = limit if limit else 100
            search_url = f"https://www.reddit.com/search.json?q={self.topic}&sort=relevance&limit={api_limit}"
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            for post in posts:
                post_data = post.get('data', {})
                
                comment = Comment(
                    source_url=f"https://reddit.com{post_data.get('permalink', '')}",
                    platform="reddit",
                    commenter_name=post_data.get('author', 'Unknown'),
                    comment_text=f"{post_data.get('title', '')} - {post_data.get('selftext', '')}"[:500],
                    date_posted=str(post_data.get('created_utc', '')),
                    likes=post_data.get('score', 0)
                )
                
                if len(comment.comment_text.strip()) > 20:
                    comments.append(comment)
            
            logger.info(f"✓ Reddit: {len(comments)} posts")
            
        except Exception as e:
            logger.error(f"Reddit failed: {e}")
        
        return comments
    
    def scrape_hackernews(self, limit=None) -> List[Comment]:
        """Scrape Hacker News using Algolia API."""
        comments = []
        
        try:
            search_url = f"http://hn.algolia.com/api/v1/search?query={self.topic}&tags=story"
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            hits = data.get('hits', [])
            
            # Use all hits if unlimited, otherwise slice
            hits_to_process = hits if limit is None else hits[:limit]
            
            for hit in hits_to_process:
                comment = Comment(
                    source_url=hit.get('url', f"https://news.ycombinator.com/item?id={hit.get('objectID')}"),
                    platform="hackernews",
                    commenter_name=hit.get('author', 'Unknown'),
                    comment_text=f"{hit.get('title', '')} - {hit.get('story_text', '')}"[:500],
                    date_posted=hit.get('created_at', ''),
                    likes=hit.get('points', 0)
                )
                
                if len(comment.comment_text.strip()) > 20:
                    comments.append(comment)
            
            logger.info(f"✓ Hacker News: {len(comments)} posts")
            
        except Exception as e:
            logger.error(f"Hacker News failed: {e}")
        
        return comments
    
    def scrape_twitter_nitter(self, limit=None) -> List[Comment]:
        """
        Scrape Twitter via Nitter (privacy-focused Twitter frontend).
        Nitter provides public access without API keys.
        """
        comments = []
        
        try:
            # Using Nitter instances (public Twitter frontend)
            nitter_instances = [
                'https://nitter.net',
                'https://nitter.privacydev.net',
                'https://nitter.poast.org'
            ]
            
            search_query = self.topic.replace(' ', '%20')
            
            for instance in nitter_instances:
                try:
                    search_url = f"{instance}/search?f=tweets&q={search_query}"
                    response = self.session.get(search_url, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Find tweet containers (use limit if provided)
                        tweets = soup.find_all('div', class_='timeline-item', limit=limit if limit else None)
                        
                        for tweet in tweets:
                            try:
                                # Extract username
                                username_elem = tweet.find('a', class_='username')
                                username = username_elem.get_text(strip=True) if username_elem else 'Twitter User'
                                
                                # Extract tweet text
                                content_elem = tweet.find('div', class_='tweet-content')
                                if content_elem:
                                    tweet_text = content_elem.get_text(strip=True)
                                    
                                    # Get tweet link
                                    link_elem = tweet.find('a', class_='tweet-link')
                                    tweet_url = f"{instance}{link_elem['href']}" if link_elem else instance
                                    
                                    # Get stats
                                    stats = tweet.find_all('span', class_='tweet-stat')
                                    likes = 0
                                    if stats:
                                        for stat in stats:
                                            text = stat.get_text()
                                            if '❤' in str(stat) or 'icon-heart' in str(stat):
                                                try:
                                                    likes = int(''.join(filter(str.isdigit, text)))
                                                except:
                                                    pass
                                    
                                    if len(tweet_text) > 20:
                                        comment = Comment(
                                            source_url=tweet_url,
                                            platform="twitter",
                                            commenter_name=username,
                                            comment_text=tweet_text[:500],
                                            date_posted=None,
                                            likes=likes
                                        )
                                        comments.append(comment)
                            except Exception as e:
                                logger.debug(f"Failed to parse tweet: {e}")
                                continue
                        
                        if comments:
                            break  # Found results, no need to try other instances
                        
                except Exception as e:
                    logger.debug(f"Nitter instance {instance} failed: {e}")
                    continue
            
            logger.info(f"✓ Twitter: {len(comments)} tweets")
            
        except Exception as e:
            logger.error(f"Twitter scraping failed: {e}")
        
        return comments
    
    def scrape_github_discussions(self, limit=None) -> List[Comment]:
        """Scrape GitHub discussions and issues (public API, no auth needed for public repos)."""
        comments = []
        
        try:
            # Search GitHub for relevant repositories and issues (max 100 per page)
            per_page = limit if limit and limit <= 100 else 100
            search_url = f"https://api.github.com/search/issues?q={self.topic}+in:title,body&sort=updated&per_page={per_page}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                for item in items:
                    comment = Comment(
                        source_url=item.get('html_url', ''),
                        platform="github",
                        commenter_name=item.get('user', {}).get('login', 'GitHub User'),
                        comment_text=f"{item.get('title', '')} - {item.get('body', '')}"[:500],
                        date_posted=item.get('created_at', ''),
                        likes=item.get('reactions', {}).get('total_count', 0)
                    )
                    
                    if len(comment.comment_text.strip()) > 20:
                        comments.append(comment)
                
                logger.info(f"✓ GitHub: {len(comments)} issues/discussions")
            
        except Exception as e:
            logger.error(f"GitHub scraping failed: {e}")
        
        return comments
    
    def scrape_quora(self, limit=None) -> List[Comment]:
        """
        Scrape Quora questions/answers.
        Note: Quora blocks most scrapers, this is a best-effort attempt.
        """
        comments = []
        
        try:
            search_url = f"https://www.quora.com/search?q={self.topic.replace(' ', '+')}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try to find question cards
                questions = soup.find_all('div', class_=lambda x: x and 'question' in x.lower(), limit=limit if limit else None)
                
                for q in questions:
                    try:
                        title_elem = q.find(['a', 'span'], class_=lambda x: x and 'title' in x.lower())
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                            
                            if link and not link.startswith('http'):
                                link = f"https://www.quora.com{link}"
                            
                            if len(title) > 20:
                                comment = Comment(
                                    source_url=link or search_url,
                                    platform="quora",
                                    commenter_name="Quora User",
                                    comment_text=title[:500],
                                    date_posted=None
                                )
                                comments.append(comment)
                    except:
                        continue
                
                logger.info(f"✓ Quora: {len(comments)} questions")
            
        except Exception as e:
            logger.error(f"Quora scraping failed: {e}")
        
        return comments
    
    def scrape_medium(self, limit=None) -> List[Comment]:
        """Scrape Medium articles using public RSS feed."""
        comments = []
        
        try:
            # Medium RSS search (limited but works without auth)
            search_query = self.topic.replace(' ', '-')
            search_url = f"https://medium.com/search?q={self.topic}"
            
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find article elements
                articles = soup.find_all('article', limit=limit if limit else None)
                
                for article in articles:
                    try:
                        # Extract title
                        title_elem = article.find('h2')
                        if not title_elem:
                            title_elem = article.find('h3')
                        
                        # Extract subtitle/preview
                        preview_elem = article.find('h3')
                        if not preview_elem:
                            preview_elem = article.find('p')
                        
                        # Extract author
                        author_elem = article.find('a', class_=lambda x: x and 'author' in str(x).lower())
                        if not author_elem:
                            author_elem = article.find('p', class_=lambda x: x and 'author' in str(x).lower())
                        
                        # Extract link
                        link_elem = article.find('a')
                        
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            preview = preview_elem.get_text(strip=True) if preview_elem else ""
                            author = author_elem.get_text(strip=True) if author_elem else "Medium Writer"
                            link = link_elem.get('href', '') if link_elem else ''
                            
                            if link and not link.startswith('http'):
                                link = f"https://medium.com{link}"
                            
                            text = f"{title} - {preview}"
                            
                            if len(text.strip()) > 20:
                                comment = Comment(
                                    source_url=link or search_url,
                                    platform="medium",
                                    commenter_name=author,
                                    comment_text=text[:500],
                                    date_posted=None
                                )
                                comments.append(comment)
                    except:
                        continue
                
                logger.info(f"✓ Medium: {len(comments)} articles")
            
        except Exception as e:
            logger.error(f"Medium scraping failed: {e}")
        
        return comments
    
    def scrape_all(self, limit_per_source=None, include_extended=True) -> List[Comment]:
        """Scrape from all available sources."""
        all_comments = []
        
        logger.info(f"Scraping from multiple sources for: {self.topic}")
        
        # Scrape each platform (unlimited if limit_per_source is None)
        all_comments.extend(self.scrape_reddit(limit=limit_per_source))
        time.sleep(1)  # Rate limiting
        
        all_comments.extend(self.scrape_hackernews(limit=limit_per_source))
        time.sleep(1)
        
        all_comments.extend(self.scrape_twitter_nitter(limit=limit_per_source))
        time.sleep(1)
        
        all_comments.extend(self.scrape_github_discussions(limit=limit_per_source))
        time.sleep(1)
        
        all_comments.extend(self.scrape_quora(limit=limit_per_source))
        time.sleep(1)
        
        all_comments.extend(self.scrape_medium(limit=limit_per_source))
        
        # Add extended sources if requested
        if include_extended:
            try:
                from commentradar.scrapers.extended_sources import ExtendedSourcesScraper
                extended_scraper = ExtendedSourcesScraper(topic=self.topic)
                all_comments.extend(extended_scraper.scrape_all(limit_per_source=limit_per_source))
            except Exception as e:
                logger.warning(f"Extended sources not available: {e}")
        
        logger.info(f"Total collected: {len(all_comments)} posts from {len(set(c.platform for c in all_comments))} platforms")
        
        return all_comments

