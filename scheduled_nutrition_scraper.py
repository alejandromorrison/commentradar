"""
Scheduled scraper for nutrition SaaS - runs every 30 minutes.
Continuously collects real data from Reddit and Hacker News.
"""

import time
import schedule
from datetime import datetime
import logging
from scrape_nutrition_targeted import scrape_reddit_posts, scrape_hackernews, scrape_producthunt
from commentradar.models import CommentCollection
from commentradar.utils.sentiment import add_sentiment_to_comments
import json
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NutritionSaaSScheduler:
    """Scheduler for nutrition SaaS scraping."""
    
    def __init__(self, output_file="nutrition_saas_feed.json"):
        # Ensure scrape folder exists
        import os
        os.makedirs('scrape', exist_ok=True)
        
        # Add scrape folder to path if not already there
        if not output_file.startswith('scrape/') and not output_file.startswith('scrape\\'):
            output_file = os.path.join('scrape', output_file)
        
        self.output_file = output_file
        self.run_count = 0
    
    def scrape_job(self):
        """Execute one scraping cycle."""
        self.run_count += 1
        
        print(f"\n{'='*60}")
        print(f"🔄 Scraping Run #{self.run_count}")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        try:
            # Collect from all sources
            new_comments = []
            new_comments.extend(scrape_reddit_posts("nutrition SaaS platform software", limit=10))
            new_comments.extend(scrape_hackernews("nutrition software app", limit=8))
            
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
            print(f"✅ Added {len(unique_new)} new posts")
            print(f"📊 Total in database: {len(merged_data)}")
            print(f"💾 Saved to: {self.output_file}")
            
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
║     Nutrition SaaS - Scheduled Feed Collector            ║
╚═══════════════════════════════════════════════════════════╝

📌 Topic: Nutrition SaaS Platforms
🔄 Interval: Every {interval_minutes} minutes
💾 Output: {self.output_file}
🌐 Sources: Reddit, Hacker News

This will run continuously and collect new posts every {interval_minutes} minutes.
The JSON file will grow over time with unique posts.

Press Ctrl+C to stop.
""")
        
        # Schedule
        schedule.every(interval_minutes).minutes.do(self.scrape_job)
        
        # Run immediately
        logger.info("Running initial scrape...")
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
    # Run every 30 minutes (change to 1 for testing)
    scheduler = NutritionSaaSScheduler(output_file="nutrition_saas_feed.json")
    scheduler.run(interval_minutes=30)  # Change to 1 for quick testing

