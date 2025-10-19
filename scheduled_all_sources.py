"""
Scheduled scraper for ALL sources - runs every 30 minutes.
Collects from: Reddit, HN, Twitter, GitHub, Quora, Medium
"""

import time
import schedule
from datetime import datetime
import logging
import json
import os

from commentradar.scrapers.multi_source_scraper import MultiSourceScraper
from commentradar.utils.sentiment import add_sentiment_to_comments

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AllSourcesScheduler:
    """Scheduler for multi-source scraping."""
    
    def __init__(self, output_file="nutrition_saas_complete_feed.json"):
        # Ensure scrape folder exists
        import os
        os.makedirs('scrape', exist_ok=True)
        
        # Add scrape folder to path if not already there
        if not output_file.startswith('scrape/') and not output_file.startswith('scrape\\'):
            output_file = os.path.join('scrape', output_file)
        
        self.output_file = output_file
        self.run_count = 0
        self.scraper = MultiSourceScraper(topic="nutrition SaaS platform software")
    
    def scrape_job(self):
        """Execute one scraping cycle."""
        self.run_count += 1
        
        print(f"\n{'='*60}")
        print(f"🔄 Multi-Source Scraping Run #{self.run_count}")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        try:
            # Collect from all sources
            new_comments = self.scraper.scrape_all()
            
            if not new_comments:
                logger.warning("No new data found in this cycle")
                return
            
            # Add sentiment
            add_sentiment_to_comments(new_comments)
            
            # Load existing data
            if os.path.exists(self.output_file):
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            else:
                existing_data = []
            
            # Remove duplicates
            existing_urls = {c['source_url'] for c in existing_data}
            unique_new = [
                c.to_dict() for c in new_comments 
                if c.source_url not in existing_urls
            ]
            
            # Merge and save
            merged_data = existing_data + unique_new
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, ensure_ascii=False, indent=2)
            
            # Report
            print(f"\n✅ Added {len(unique_new)} new posts")
            print(f"📊 Total in database: {len(merged_data)}")
            print(f"💾 Saved to: {self.output_file}")
            
            # Platform breakdown
            by_platform = {}
            for c in unique_new:
                by_platform.setdefault(c['platform'], 0)
                by_platform[c['platform']] += 1
            
            if by_platform:
                print(f"\n📈 New posts by platform:")
                for platform, count in sorted(by_platform.items(), key=lambda x: x[1], reverse=True):
                    print(f"   {platform}: {count}")
            
            # Show sample
            if unique_new:
                sample = unique_new[0]
                print(f"\n📝 Latest: [{sample['platform'].upper()}] {sample['commenter_name']}")
                print(f"   {sample['comment_text'][:100]}...")
            
        except Exception as e:
            logger.error(f"Error in scrape cycle: {e}", exc_info=True)
    
    def run(self, interval_minutes=30):
        """Run the scheduler."""
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║        ALL SOURCES - Scheduled Feed Collector            ║
╚═══════════════════════════════════════════════════════════╝

📌 Topic: Nutrition SaaS Platforms
🔄 Interval: Every {interval_minutes} minutes
💾 Output: {self.output_file}

🌐 Data Sources:
   ✓ Reddit
   ✓ Hacker News
   ✓ Twitter/X
   ✓ GitHub
   ✓ Quora
   ✓ Medium

This will run continuously and collect from all sources.
The JSON file will grow over time with unique posts.

Press Ctrl+C to stop.
""")
        
        # Schedule
        schedule.every(interval_minutes).minutes.do(self.scrape_job)
        
        # Run immediately
        logger.info("Running initial scrape from all sources...")
        self.scrape_job()
        
        print(f"\n⏰ Next run in {interval_minutes} minutes...\n")
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n✋ Scheduler stopped")
            print(f"📊 Completed {self.run_count} scraping cycles")
            print(f"💾 Data saved in: {self.output_file}\n")


if __name__ == '__main__':
    import sys
    
    # Get interval from command line or use default
    interval = 30
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except:
            pass
    
    scheduler = AllSourcesScheduler(output_file="nutrition_saas_complete_feed.json")
    scheduler.run(interval_minutes=interval)

