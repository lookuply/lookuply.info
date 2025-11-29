#!/usr/bin/env python3
"""
Lookuply Crawler - Main Entry Point

Run the crawler with various options.
"""

import sys
import os
import argparse
import logging
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lookuply_crawler.spiders.web_spider import WebSpider
from lookuply_crawler.config import LANGUAGE_CODES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for crawler."""
    parser = argparse.ArgumentParser(
        description='Lookuply Crawler - Multi-language web crawler for EU languages'
    )

    parser.add_argument(
        '--languages',
        type=str,
        help='Comma-separated list of language codes to crawl (e.g., en,de,fr). Default: all 24 EU languages',
        default=None
    )

    parser.add_argument(
        '--max-pages',
        type=int,
        help='Maximum number of pages to crawl per language',
        default=None
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        help='Output directory for crawled data',
        default='./data/crawled'
    )

    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level',
        default='INFO'
    )

    parser.add_argument(
        '--log-file',
        type=str,
        help='Log file path (default: stdout)',
        default=None
    )

    parser.add_argument(
        '--list-languages',
        action='store_true',
        help='List all supported languages and exit'
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode: crawl only 10 pages per language'
    )

    args = parser.parse_args()

    # List languages
    if args.list_languages:
        from lookuply_crawler.config import LANGUAGES
        print("\nSupported EU Languages:")
        print("=" * 50)
        for code, info in sorted(LANGUAGES.items()):
            print(f"{code:4s} - {info['name']:15s} ({info['native']})")
        print("=" * 50)
        print(f"Total: {len(LANGUAGES)} languages")
        return 0

    # Display banner
    print("=" * 60)
    print("LOOKUPLY CRAWLER")
    print("Multi-language Web Crawler for EU Languages")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Get settings
    settings = get_project_settings()

    # Override settings from command line
    settings.set('LOG_LEVEL', args.log_level)
    settings.set('OUTPUT_DIR', args.output_dir)

    if args.log_file:
        settings.set('LOG_FILE', args.log_file)

    # Test mode
    if args.test:
        args.max_pages = 10
        logger.info("TEST MODE: Crawling only 10 pages per language")

    # Validate languages
    if args.languages:
        requested_langs = [lang.strip() for lang in args.languages.split(',')]
        invalid_langs = [lang for lang in requested_langs if lang not in LANGUAGE_CODES]

        if invalid_langs:
            logger.error(f"Invalid language codes: {', '.join(invalid_langs)}")
            logger.info(f"Supported languages: {', '.join(LANGUAGE_CODES)}")
            return 1

        logger.info(f"Crawling languages: {', '.join(requested_langs)}")
    else:
        logger.info(f"Crawling all {len(LANGUAGE_CODES)} EU languages")

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    logger.info(f"Output directory: {args.output_dir}")

    # Create crawler process
    process = CrawlerProcess(settings)

    # Start crawler
    process.crawl(
        WebSpider,
        languages=args.languages,
        max_pages=args.max_pages
    )

    # Start crawling
    logger.info("Starting crawler...")
    process.start()

    print("=" * 60)
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
