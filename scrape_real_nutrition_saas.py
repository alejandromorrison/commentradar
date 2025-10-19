"""
Real scraper for Nutrition SaaS platforms.
This searches the web and extracts real comments/reviews.
"""

import sys
import logging
from commentradar.scrapers.real_blog_scraper import RealBlogScraper
from commentradar.models import CommentCollection
from commentradar.utils.sentiment import add_sentiment_to_comments

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Scrape real data about nutrition SaaS platforms."""
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║     CommentRadar - Real Nutrition SaaS Scraper           ║
╚═══════════════════════════════════════════════════════════╝

Searching for real comments and reviews about nutrition SaaS platforms...
This may take a few moments...

""")
    
    # Create scraper
    scraper = RealBlogScraper(
        topic="nutrition SaaS platform software reviews",
        limit=20
    )
    
    try:
        # Scrape real comments
        logger.info("Starting real scraping...")
        comments = scraper.scrape()
        
        if not comments:
            print("\n⚠️  No comments found. This could be because:")
            print("   1. The websites don't allow scraping (robots.txt)")
            print("   2. The search didn't find suitable blogs")
            print("   3. The blogs don't have comment sections")
            print("\n💡 Try installing: pip install duckduckgo-search")
            print("   This enables web search to find more blogs.")
            return
        
        # Add to collection
        collection = CommentCollection()
        collection.extend(comments)
        
        # Add sentiment analysis
        logger.info("Analyzing sentiment...")
        add_sentiment_to_comments(collection.comments)
        
        # Save results
        output_file = "nutrition_saas_comments.json"
        collection.save_to_file(output_file)
        
        # Display results
        print(f"\n{'='*60}")
        print(f"✅ SUCCESS! Found {len(comments)} real comments")
        print(f"{'='*60}\n")
        
        # Show samples
        print("📝 Sample Comments:\n")
        for i, comment in enumerate(comments[:3], 1):
            print(f"{i}. {comment.commenter_name}")
            print(f"   Platform: {comment.platform}")
            print(f"   Sentiment: {comment.sentiment or 'N/A'}")
            print(f"   Text: {comment.comment_text[:150]}...")
            print(f"   Source: {comment.source_url}")
            print()
        
        print(f"💾 All {len(comments)} comments saved to: {output_file}")
        print("\nYou can now:")
        print(f"  1. View the file: type {output_file}")
        print("  2. Analyze the data in your preferred tool")
        print("  3. Run the scheduler to collect more over time\n")
        
    except KeyboardInterrupt:
        print("\n\n✋ Stopped by user")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
    finally:
        scraper.close()


if __name__ == '__main__':
    main()

