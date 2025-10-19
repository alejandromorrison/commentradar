"""
Example: Run CommentRadar on a schedule.

This script demonstrates how to run automated scraping every 30 minutes.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from commentradar.scheduler import ScheduledScraper


def main():
    """Run scheduled scraping example."""
    
    # Configure your scraping job
    scheduler = ScheduledScraper(
        topic="nutrition blogs",
        platforms=["blog"],
        output_file="scheduled_comments.json",
        limit=50,
        analyze_sentiment=True,
        append_mode=True  # Append new comments to existing file
    )
    
    # Run every 30 minutes
    scheduler.run_every(minutes=30)


if __name__ == '__main__':
    print("=" * 60)
    print("CommentRadar - Scheduled Scraper")
    print("=" * 60)
    print("\nThis will scrape comments every 30 minutes.")
    print("Press Ctrl+C to stop.\n")
    
    main()

