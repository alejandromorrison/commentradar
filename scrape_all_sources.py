"""
Scrape nutrition SaaS data from ALL sources:
Reddit, Hacker News, Twitter, GitHub, Quora, Medium, Product Hunt
"""

import logging
from commentradar.scrapers.multi_source_scraper import MultiSourceScraper
from commentradar.models import CommentCollection
from commentradar.utils.sentiment import add_sentiment_to_comments

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Scrape from all sources."""
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║     Multi-Source Nutrition SaaS Scraper                  ║
╚═══════════════════════════════════════════════════════════╝

Collecting data from:
  📱 Reddit
  💻 Hacker News
  🐦 Twitter/X (via Nitter)
  🔧 GitHub Discussions
  ❓ Quora
  📝 Medium
  🚀 Product Hunt

This will take 30-60 seconds...
""")
    
    # Create multi-source scraper
    scraper = MultiSourceScraper(topic="nutrition SaaS platform software")
    
    # Scrape all sources
    logger.info("Starting multi-source scraping...")
    all_comments = scraper.scrape_all()
    
    if not all_comments:
        print("\n⚠️  No data collected. Check your internet connection.")
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
    output_file = os.path.join('scrape', "nutrition_saas_all_sources.json")
    collection.save_to_file(output_file)
    
    # Display results
    print(f"\n{'='*60}")
    print(f"✅ SUCCESS! Collected {len(all_comments)} posts")
    print(f"{'='*60}\n")
    
    # Group by platform
    by_platform = {}
    for c in all_comments:
        by_platform.setdefault(c.platform, []).append(c)
    
    print("📊 Breakdown by Platform:\n")
    for platform, comments in sorted(by_platform.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {platform.upper():.<20} {len(comments)} posts")
    
    print(f"\n📝 Sample Posts:\n")
    for i, comment in enumerate(all_comments[:5], 1):
        print(f"{i}. [{comment.platform.upper()}] {comment.commenter_name}")
        print(f"   Sentiment: {comment.sentiment}")
        print(f"   {comment.comment_text[:100]}...")
        print(f"   🔗 {comment.source_url}\n")
    
    print(f"💾 All {len(all_comments)} posts saved to: {output_file}")
    print(f"\n🔄 To run this automatically every 30 minutes:")
    print(f"   python scheduled_all_sources.py\n")


if __name__ == '__main__':
    main()

