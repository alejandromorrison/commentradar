"""
Quick Scraper - Just run with topic as argument
Usage: python quick_scrape.py "your topic here"
"""

import sys
import logging
from commentradar.scrapers.multi_source_scraper import MultiSourceScraper
from commentradar.models import CommentCollection
from commentradar.utils.sentiment import add_sentiment_to_comments

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def main():
    """Quick scrape from command line."""
    
    # Get topic from command line
    if len(sys.argv) < 2:
        print("""
╔═══════════════════════════════════════════════════════════╗
║            CommentRadar Quick Scraper                    ║
╚═══════════════════════════════════════════════════════════╝

Usage: python quick_scrape.py "your topic"

Examples:
  python quick_scrape.py "AI tools"
  python quick_scrape.py "fitness apps"
  python quick_scrape.py "meal planning software"
  python quick_scrape.py "dental clinic reviews"

Options:
  --limit N         Max posts per source (default: unlimited)
  --no-sentiment    Skip sentiment analysis
  --output FILE     Output filename (default: auto-generated)

Full Example:
  python quick_scrape.py "AI writing tools" --limit 20 --output ai_tools.json
  python quick_scrape.py "fitness apps" (unlimited posts)
""")
        sys.exit(1)
    
    # Parse arguments
    topic = sys.argv[1]
    limit = None  # Unlimited by default
    analyze_sentiment = True
    output_file = None
    
    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--limit' and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--no-sentiment':
            analyze_sentiment = False
            i += 1
        elif sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    # Generate filename if not provided
    if not output_file:
        output_file = topic.replace(' ', '_').lower()[:30] + '_data.json'
    
    # Ensure scrape folder exists and add to path
    import os
    os.makedirs('scrape', exist_ok=True)
    if not output_file.startswith('scrape/') and not output_file.startswith('scrape\\'):
        output_file = os.path.join('scrape', output_file)
    
    # Show settings
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║            Scraping: {topic[:40]:<40} ║
╚═══════════════════════════════════════════════════════════╝

📊 Settings:
   Topic: {topic}
   Limit: {'Unlimited' if limit is None else f'{limit} posts per source'}
   Sentiment: {'Yes' if analyze_sentiment else 'No'}
   Output: {output_file}

🌐 Sources: Reddit, Hacker News, Twitter, GitHub, Quora, Medium

Starting in 2 seconds...
""")
    
    import time
    time.sleep(2)
    
    # Scrape
    print("📡 Collecting data...\n")
    scraper = MultiSourceScraper(topic=topic)
    comments = scraper.scrape_all(limit_per_source=limit)
    
    if not comments:
        print("\n❌ No data found. Try a different topic.\n")
        return
    
    # Process
    collection = CommentCollection()
    collection.extend(comments)
    
    if analyze_sentiment:
        print("\n😊 Analyzing sentiment...")
        add_sentiment_to_comments(collection.comments)
    
    # Save
    collection.save_to_file(output_file)
    
    # Results
    print(f"\n{'='*60}")
    print(f"✅ SUCCESS! Collected {len(comments)} posts")
    print(f"{'='*60}\n")
    
    # Platform breakdown
    by_platform = {}
    for c in comments:
        by_platform.setdefault(c.platform, []).append(c)
    
    print("📊 By Platform:")
    for platform, posts in sorted(by_platform.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {platform.upper():.<20} {len(posts)} posts")
    
    # Samples
    print(f"\n📝 Sample Posts:\n")
    for i, comment in enumerate(comments[:3], 1):
        print(f"{i}. [{comment.platform.upper()}] {comment.commenter_name}")
        if analyze_sentiment:
            print(f"   Sentiment: {comment.sentiment}")
        print(f"   {comment.comment_text[:100]}...")
        print()
    
    print(f"💾 Saved to: {output_file}\n")


if __name__ == '__main__':
    main()

