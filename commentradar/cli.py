"""
Command-line interface for CommentRadar.
"""

import argparse
import sys
import logging
from typing import Optional

from commentradar.scraper_manager import ScraperManager
from commentradar import __version__


def setup_logging(verbose: bool = False):
    """
    Configure logging.
    
    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def create_parser() -> argparse.ArgumentParser:
    """
    Create the argument parser for the CLI.
    
    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog='commentradar',
        description='CommentRadar - CLI Insight Scraper for public comments',
        epilog='Example: commentradar --topic "nutrition blogs" --platform blog --limit 20 --output nutrition_comments.json'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    parser.add_argument(
        '--topic',
        type=str,
        required=True,
        help='Topic to search for (e.g., "dental clinics in Santo Domingo")'
    )
    
    parser.add_argument(
        '--platform',
        type=str,
        nargs='+',
        choices=['blog', 'facebook', 'instagram', 'google', 'all'],
        default=['all'],
        help='Platform(s) to scrape (default: all)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Maximum number of comments to collect per platform'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='comments.json',
        help='Output JSON file path (default: comments.json)'
    )
    
    # Filtering options
    filter_group = parser.add_argument_group('filtering options')
    
    filter_group.add_argument(
        '--filter-date-start',
        type=str,
        help='Filter comments after this date (ISO format: YYYY-MM-DD)'
    )
    
    filter_group.add_argument(
        '--filter-date-end',
        type=str,
        help='Filter comments before this date (ISO format: YYYY-MM-DD)'
    )
    
    filter_group.add_argument(
        '--sentiment',
        type=str,
        choices=['positive', 'negative', 'neutral'],
        help='Filter by sentiment'
    )
    
    filter_group.add_argument(
        '--min-length',
        type=int,
        help='Minimum comment text length'
    )
    
    filter_group.add_argument(
        '--max-length',
        type=int,
        help='Maximum comment text length'
    )
    
    # Additional options
    parser.add_argument(
        '--analyze-sentiment',
        action='store_true',
        help='Add sentiment analysis to comments'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser


def main(args: Optional[list] = None):
    """
    Main entry point for the CLI.
    
    Args:
        args: Command-line arguments (for testing)
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    # Setup logging
    setup_logging(parsed_args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info(f"CommentRadar v{__version__}")
    
    try:
        # Determine platforms
        platforms = parsed_args.platform
        if 'all' in platforms:
            platforms = ['blog', 'facebook', 'instagram', 'google']
        
        # Create scraper manager
        manager = ScraperManager(
            topic=parsed_args.topic,
            platforms=platforms,
            limit=parsed_args.limit
        )
        
        # Scrape comments
        logger.info(f"Scraping topic: '{parsed_args.topic}'")
        manager.scrape_all()
        
        # Add sentiment analysis if requested
        if parsed_args.analyze_sentiment:
            logger.info("Analyzing sentiment...")
            manager.add_sentiment_analysis()
        
        # Apply filters
        if any([
            parsed_args.filter_date_start,
            parsed_args.filter_date_end,
            parsed_args.sentiment,
            parsed_args.min_length,
            parsed_args.max_length
        ]):
            logger.info("Applying filters...")
            manager.apply_filters(
                start_date=parsed_args.filter_date_start,
                end_date=parsed_args.filter_date_end,
                sentiment=parsed_args.sentiment,
                min_length=parsed_args.min_length,
                max_length=parsed_args.max_length
            )
        
        # Save results
        manager.save_results(parsed_args.output)
        
        logger.info(f"✓ Successfully saved {len(manager.collection)} comments to {parsed_args.output}")
        return 0
    
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        return 130
    
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=parsed_args.verbose)
        return 1


if __name__ == '__main__':
    sys.exit(main())

