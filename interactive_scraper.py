"""
Interactive CommentRadar Scraper
User-friendly console interface to scrape any topic from all sources.
"""

import sys
import logging
from datetime import datetime
from commentradar.scrapers.multi_source_scraper import MultiSourceScraper
from commentradar.models import CommentCollection
from commentradar.utils.sentiment import add_sentiment_to_comments

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print welcome banner."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║            CommentRadar Interactive Scraper              ║
║                      All Sources                         ║
╚═══════════════════════════════════════════════════════════╝

🌐 Data Sources: Reddit, Hacker News, Twitter, GitHub, Quora, Medium
📊 Output: JSON with sentiment analysis
🔄 Options: One-time or scheduled scraping

""")


def get_user_input():
    """Get scraping parameters from user."""
    
    print("=" * 60)
    print("📝 Enter Scraping Details")
    print("=" * 60 + "\n")
    
    # Get topic
    while True:
        topic = input("🔍 What topic do you want to scrape?\n   (e.g., 'nutrition SaaS', 'AI tools', 'fitness apps')\n   Topic: ").strip()
        if topic:
            break
        print("   ⚠️  Topic cannot be empty. Please try again.\n")
    
    # Get mode
    print("\n📋 Choose scraping mode:")
    print("   [1] One-time scrape (get results now)")
    print("   [2] Scheduled scraping (runs every X minutes)")
    
    while True:
        mode = input("\n   Mode [1/2]: ").strip()
        if mode in ['1', '2']:
            break
        print("   ⚠️  Please enter 1 or 2")
    
    # Get limit
    print("\n🔢 How many posts to collect per source?")
    while True:
        limit_input = input("   Limit (press Enter for default 20): ").strip()
        if not limit_input:
            limit = 20
            break
        try:
            limit = int(limit_input)
            if limit > 0:
                break
            print("   ⚠️  Please enter a positive number")
        except ValueError:
            print("   ⚠️  Please enter a valid number")
    
    # Get interval if scheduled
    interval = None
    if mode == '2':
        print("\n⏱️  How often should it scrape?")
        while True:
            interval_input = input("   Minutes between scrapes (default 30): ").strip()
            if not interval_input:
                interval = 30
                break
            try:
                interval = int(interval_input)
                if interval > 0:
                    break
                print("   ⚠️  Please enter a positive number")
            except ValueError:
                print("   ⚠️  Please enter a valid number")
    
    # Get output file
    print("\n💾 Where should the data be saved?")
    default_filename = topic.replace(' ', '_').lower() + '_data.json'
    output_file = input(f"   Filename (default '{default_filename}'): ").strip()
    if not output_file:
        output_file = default_filename
    if not output_file.endswith('.json'):
        output_file += '.json'
    
    # Sentiment analysis
    print("\n😊 Analyze sentiment?")
    sentiment_input = input("   [Y/n]: ").strip().lower()
    analyze_sentiment = sentiment_input != 'n'
    
    return {
        'topic': topic,
        'mode': mode,
        'limit': limit,
        'interval': interval,
        'output_file': output_file,
        'analyze_sentiment': analyze_sentiment
    }


def confirm_settings(settings):
    """Show settings and confirm."""
    
    print("\n" + "=" * 60)
    print("✅ Your Settings")
    print("=" * 60)
    print(f"🔍 Topic: {settings['topic']}")
    print(f"📋 Mode: {'One-time' if settings['mode'] == '1' else 'Scheduled'}")
    if settings['mode'] == '2':
        print(f"⏱️  Interval: Every {settings['interval']} minutes")
    print(f"🔢 Limit: {settings['limit']} posts per source")
    print(f"💾 Output: {settings['output_file']}")
    print(f"😊 Sentiment: {'Yes' if settings['analyze_sentiment'] else 'No'}")
    print("=" * 60 + "\n")
    
    confirm = input("Continue with these settings? [Y/n]: ").strip().lower()
    return confirm != 'n'


def run_one_time_scrape(settings):
    """Execute a one-time scrape."""
    
    print("\n🚀 Starting scrape...\n")
    
    # Create scraper
    scraper = MultiSourceScraper(topic=settings['topic'])
    
    # Scrape all sources
    print("📡 Collecting data from all sources...")
    print("   This may take 30-60 seconds...\n")
    
    comments = scraper.scrape_all()
    
    if not comments:
        print("\n❌ No data found. Try a different topic or check your connection.\n")
        return
    
    # Create collection
    collection = CommentCollection()
    collection.extend(comments)
    
    # Add sentiment if requested
    if settings['analyze_sentiment']:
        print("\n😊 Analyzing sentiment...")
        add_sentiment_to_comments(collection.comments)
    
    # Save results
    collection.save_to_file(settings['output_file'])
    
    # Show results
    print("\n" + "=" * 60)
    print("✅ SUCCESS!")
    print("=" * 60)
    print(f"📊 Collected: {len(comments)} posts")
    
    # Platform breakdown
    by_platform = {}
    for c in comments:
        by_platform.setdefault(c.platform, []).append(c)
    
    print(f"\n🌐 By Platform:")
    for platform, posts in sorted(by_platform.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {platform.capitalize():.<20} {len(posts)} posts")
    
    # Show samples
    print(f"\n📝 Sample Posts:\n")
    for i, comment in enumerate(comments[:3], 1):
        print(f"{i}. [{comment.platform.upper()}] {comment.commenter_name}")
        if settings['analyze_sentiment']:
            print(f"   Sentiment: {comment.sentiment}")
        print(f"   {comment.comment_text[:100]}...")
        print(f"   🔗 {comment.source_url}\n")
    
    print(f"💾 All data saved to: {settings['output_file']}")
    print()


def run_scheduled_scrape(settings):
    """Execute scheduled scraping."""
    
    import time
    import schedule
    import json
    import os
    
    run_count = [0]
    
    def scrape_job():
        """Single scrape cycle."""
        run_count[0] += 1
        
        print(f"\n{'='*60}")
        print(f"🔄 Scraping Run #{run_count[0]}")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        try:
            # Create scraper
            scraper = MultiSourceScraper(topic=settings['topic'])
            
            # Scrape
            comments = scraper.scrape_all()
            
            if not comments:
                logger.warning("No data found in this cycle")
                return
            
            # Add sentiment
            if settings['analyze_sentiment']:
                add_sentiment_to_comments(comments)
            
            # Load existing data
            if os.path.exists(settings['output_file']):
                with open(settings['output_file'], 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            else:
                existing_data = []
            
            # Remove duplicates
            existing_urls = {c['source_url'] for c in existing_data}
            new_comments = [c for c in comments if c.source_url not in existing_urls]
            
            # Merge
            merged_data = existing_data + [c.to_dict() for c in new_comments]
            
            # Save
            with open(settings['output_file'], 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, ensure_ascii=False, indent=2)
            
            # Report
            print(f"✅ Added {len(new_comments)} new posts")
            print(f"📊 Total in database: {len(merged_data)}")
            print(f"💾 Saved to: {settings['output_file']}")
            
            if new_comments:
                sample = new_comments[0]
                print(f"\n📝 Latest: [{sample.platform.upper()}] {sample.commenter_name}")
                print(f"   {sample.comment_text[:100]}...")
            
        except Exception as e:
            logger.error(f"Error in scrape cycle: {e}")
    
    # Setup scheduler
    print(f"\n🚀 Starting scheduled scraper...")
    print(f"📌 Topic: {settings['topic']}")
    print(f"⏱️  Interval: Every {settings['interval']} minutes")
    print(f"💾 Output: {settings['output_file']}")
    print("\nPress Ctrl+C to stop.\n")
    
    # Schedule
    schedule.every(settings['interval']).minutes.do(scrape_job)
    
    # Run immediately
    scrape_job()
    
    print(f"\n⏰ Next run in {settings['interval']} minutes...\n")
    
    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n✋ Scheduler stopped")
        print(f"📊 Completed {run_count[0]} scraping cycles")
        print(f"💾 Data saved in: {settings['output_file']}\n")


def main():
    """Main interactive flow."""
    
    print_banner()
    
    # Get user input
    settings = get_user_input()
    
    # Confirm settings
    if not confirm_settings(settings):
        print("\n❌ Cancelled by user.\n")
        return
    
    # Run appropriate mode
    if settings['mode'] == '1':
        run_one_time_scrape(settings)
    else:
        run_scheduled_scrape(settings)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Stopped by user.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        logger.error("Fatal error", exc_info=True)

