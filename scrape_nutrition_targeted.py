"""
Targeted scraper for nutrition SaaS - works with specific URLs or searches Reddit/HackerNews
where scraping is more commonly allowed.
"""

import sys
import logging
import json
from bs4 import BeautifulSoup
import requests
from commentradar.models import Comment, CommentCollection
from commentradar.utils.sentiment import add_sentiment_to_comments

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def scrape_reddit_posts(topic, limit=20):
    """
    Scrape Reddit posts about nutrition SaaS (JSON API - no auth needed).
    """
    comments = []
    
    try:
        # Reddit JSON API (public, no auth)
        search_url = f"https://www.reddit.com/search.json?q={topic}&sort=relevance&limit=25"
        headers = {'User-Agent': 'CommentRadar/1.0'}
        
        logger.info(f"Searching Reddit for: {topic}")
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        posts = data.get('data', {}).get('children', [])
        
        for post in posts[:limit]:
            post_data = post.get('data', {})
            
            # Create comment from post
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
        
        logger.info(f"✓ Found {len(comments)} Reddit posts")
        
    except Exception as e:
        logger.error(f"Reddit scraping failed: {e}")
    
    return comments


def scrape_hackernews(topic, limit=20):
    """
    Scrape Hacker News for nutrition SaaS discussions (Algolia API).
    """
    comments = []
    
    try:
        # HN Algolia API (public)
        search_url = f"http://hn.algolia.com/api/v1/search?query={topic}&tags=story"
        
        logger.info(f"Searching Hacker News for: {topic}")
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        hits = data.get('hits', [])
        
        for hit in hits[:limit]:
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
        
        logger.info(f"✓ Found {len(comments)} Hacker News posts")
        
    except Exception as e:
        logger.error(f"Hacker News scraping failed: {e}")
    
    return comments


def scrape_producthunt(query):
    """
    Scrape Product Hunt discussions (public data).
    """
    comments = []
    
    try:
        # Product Hunt's public posts page
        url = f"https://www.producthunt.com/search?q={query}"
        headers = {'User-Agent': 'CommentRadar/1.0'}
        
        logger.info(f"Searching Product Hunt for: {query}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find product listings
            products = soup.find_all(['div', 'article'], class_=lambda x: x and 'product' in x.lower(), limit=10)
            
            for product in products:
                try:
                    title_elem = product.find(['h3', 'h2', 'a'])
                    desc_elem = product.find(['p', 'span'], class_=lambda x: x and 'description' in x.lower())
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        description = desc_elem.get_text(strip=True) if desc_elem else ""
                        
                        link = product.find('a')
                        url = link.get('href', '') if link else ''
                        if url and not url.startswith('http'):
                            url = f"https://www.producthunt.com{url}"
                        
                        comment = Comment(
                            source_url=url or f"https://www.producthunt.com/search?q={query}",
                            platform="producthunt",
                            commenter_name="Product Hunt",
                            comment_text=f"{title} - {description}"[:500],
                            date_posted=None
                        )
                        
                        if len(comment.comment_text.strip()) > 20:
                            comments.append(comment)
                except:
                    continue
            
            logger.info(f"✓ Found {len(comments)} Product Hunt results")
    
    except Exception as e:
        logger.error(f"Product Hunt scraping failed: {e}")
    
    return comments


def main():
    """Main scraper for nutrition SaaS platforms."""
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║   Real Nutrition SaaS Platform Scraper                   ║
╚═══════════════════════════════════════════════════════════╝

Searching multiple sources for nutrition SaaS discussions...
- Reddit
- Hacker News  
- Product Hunt

This uses public APIs that allow data access.
""")
    
    topic = "nutrition SaaS platform"
    all_comments = []
    
    # Scrape from multiple sources
    all_comments.extend(scrape_reddit_posts(topic, limit=15))
    all_comments.extend(scrape_hackernews("nutrition software", limit=10))
    all_comments.extend(scrape_producthunt("nutrition"))
    
    if not all_comments:
        print("\n❌ No data found. Check your internet connection.")
        return
    
    # Create collection
    collection = CommentCollection()
    collection.extend(all_comments)
    
    # Add sentiment
    logger.info("Analyzing sentiment...")
    add_sentiment_to_comments(collection.comments)
    
    # Save
    import os
    os.makedirs('scrape', exist_ok=True)
    output_file = os.path.join('scrape', "nutrition_saas_real_data.json")
    collection.save_to_file(output_file)
    
    # Display results
    print(f"\n{'='*60}")
    print(f"✅ SUCCESS! Found {len(all_comments)} real posts/comments")
    print(f"{'='*60}\n")
    
    # Group by platform
    by_platform = {}
    for c in all_comments:
        by_platform.setdefault(c.platform, []).append(c)
    
    for platform, comments in by_platform.items():
        print(f"📊 {platform.upper()}: {len(comments)} posts")
    
    print(f"\n📝 Sample Results:\n")
    for i, comment in enumerate(all_comments[:5], 1):
        print(f"{i}. [{comment.platform.upper()}] {comment.commenter_name}")
        print(f"   Sentiment: {comment.sentiment}")
        print(f"   {comment.comment_text[:120]}...")
        print(f"   🔗 {comment.source_url}\n")
    
    print(f"💾 All {len(all_comments)} results saved to: {output_file}")
    print(f"\n🔄 To run this every 30 minutes, use:")
    print(f"   python scheduled_nutrition_scraper.py\n")


if __name__ == '__main__':
    main()

