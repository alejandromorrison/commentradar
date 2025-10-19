"""
Scheduled scraping module for CommentRadar.
Run scraping tasks on a schedule (e.g., every 30 minutes).
"""

import time
import logging
import schedule
from datetime import datetime
from typing import Optional, List
import json
import os

from commentradar.scraper_manager import ScraperManager


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScheduledScraper:
    """Run scraping tasks on a schedule."""
    
    def __init__(
        self,
        topic: str,
        platforms: List[str],
        output_file: str = "comments.json",
        limit: Optional[int] = None,
        analyze_sentiment: bool = False,
        append_mode: bool = True
    ):
        """
        Initialize the scheduled scraper.
        
        Args:
            topic: Topic to scrape
            platforms: List of platforms
            output_file: Output JSON file path
            limit: Max comments per run
            analyze_sentiment: Whether to analyze sentiment
            append_mode: If True, append to existing file; if False, overwrite
        """
        self.topic = topic
        self.platforms = platforms
        self.output_file = output_file
        self.limit = limit
        self.analyze_sentiment = analyze_sentiment
        self.append_mode = append_mode
        self.run_count = 0
        
    def scrape_job(self):
        """Execute a single scraping job."""
        self.run_count += 1
        logger.info(f"Starting scheduled scrape #{self.run_count} at {datetime.now()}")
        
        try:
            # Create scraper manager
            manager = ScraperManager(
                topic=self.topic,
                platforms=self.platforms,
                limit=self.limit
            )
            
            # Scrape comments
            collection = manager.scrape_all()
            
            # Add sentiment if requested
            if self.analyze_sentiment:
                manager.add_sentiment_analysis()
            
            if len(collection) == 0:
                logger.warning("No new comments found")
                return
            
            # Handle append vs overwrite mode
            if self.append_mode and os.path.exists(self.output_file):
                # Load existing data
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                # Get new data
                new_data = collection.to_dict()
                
                # Remove duplicates based on source_url and comment_text
                existing_keys = {
                    (c['source_url'], c['comment_text']) 
                    for c in existing_data
                }
                
                unique_new_comments = [
                    c for c in new_data 
                    if (c['source_url'], c['comment_text']) not in existing_keys
                ]
                
                # Merge
                merged_data = existing_data + unique_new_comments
                
                # Save merged data
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    json.dump(merged_data, f, ensure_ascii=False, indent=2)
                
                logger.info(
                    f"✓ Added {len(unique_new_comments)} new comments "
                    f"(Total: {len(merged_data)})"
                )
            else:
                # Overwrite mode
                manager.save_results(self.output_file)
                logger.info(f"✓ Saved {len(collection)} comments to {self.output_file}")
            
        except Exception as e:
            logger.error(f"Error in scrape job: {e}", exc_info=True)
    
    def run_every(self, minutes: int):
        """
        Run scraping every N minutes.
        
        Args:
            minutes: Interval in minutes
        """
        logger.info(f"Starting scheduler: scraping every {minutes} minutes")
        logger.info(f"Topic: {self.topic}")
        logger.info(f"Platforms: {self.platforms}")
        logger.info(f"Output: {self.output_file}")
        logger.info(f"Append mode: {self.append_mode}")
        
        # Schedule the job
        schedule.every(minutes).minutes.do(self.scrape_job)
        
        # Run once immediately
        logger.info("Running initial scrape...")
        self.scrape_job()
        
        # Keep running
        logger.info("Scheduler is running. Press Ctrl+C to stop.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\nScheduler stopped by user")
            logger.info(f"Total runs completed: {self.run_count}")


def main():
    """CLI entry point for scheduled scraping."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Run CommentRadar on a schedule',
        epilog='Example: python -m commentradar.scheduler --topic "tech news" --interval 30'
    )
    
    parser.add_argument('--topic', required=True, help='Topic to scrape')
    parser.add_argument(
        '--platform',
        nargs='+',
        choices=['blog', 'facebook', 'instagram', 'google', 'all'],
        default=['all'],
        help='Platforms to scrape'
    )
    parser.add_argument('--interval', type=int, default=30, help='Interval in minutes (default: 30)')
    parser.add_argument('--limit', type=int, help='Max comments per run')
    parser.add_argument('--output', default='comments.json', help='Output file')
    parser.add_argument('--analyze-sentiment', action='store_true', help='Analyze sentiment')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite instead of append')
    
    args = parser.parse_args()
    
    # Handle 'all' platform
    platforms = args.platform
    if 'all' in platforms:
        platforms = ['blog', 'facebook', 'instagram', 'google']
    
    # Create scheduler
    scheduler = ScheduledScraper(
        topic=args.topic,
        platforms=platforms,
        output_file=args.output,
        limit=args.limit,
        analyze_sentiment=args.analyze_sentiment,
        append_mode=not args.overwrite
    )
    
    # Run on schedule
    scheduler.run_every(args.interval)


if __name__ == '__main__':
    main()

