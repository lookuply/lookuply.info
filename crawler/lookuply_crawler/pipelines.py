"""
Scrapy Pipelines - Data Processing
Process and store crawled items.
"""

import logging
import json
import os
from datetime import datetime
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class ValidationPipeline:
    """
    Validate items before processing.
    Drop invalid items.
    """

    def process_item(self, item, spider):
        """Validate item."""
        adapter = ItemAdapter(item)

        # Check required fields
        if not adapter.get('url'):
            raise DropItem(f"Missing URL in {item}")

        if not adapter.get('text') or adapter.get('text_length', 0) < 100:
            raise DropItem(f"Insufficient text content in {adapter['url']}")

        # Check if EU language (if configured to only keep EU languages)
        if hasattr(spider, 'eu_languages_only') and spider.eu_languages_only:
            if not adapter.get('is_eu_language', False):
                raise DropItem(f"Non-EU language in {adapter['url']}")

        return item


class LanguageFilterPipeline:
    """
    Filter items by language.
    """

    def __init__(self, allowed_languages=None, min_confidence=0.5):
        """
        Initialize pipeline.

        Args:
            allowed_languages: List of allowed language codes (None = allow all)
            min_confidence: Minimum language detection confidence
        """
        self.allowed_languages = allowed_languages
        self.min_confidence = min_confidence

    @classmethod
    def from_crawler(cls, crawler):
        """Create pipeline from crawler settings."""
        return cls(
            allowed_languages=crawler.settings.getlist('ALLOWED_LANGUAGES', None),
            min_confidence=crawler.settings.getfloat('MIN_LANGUAGE_CONFIDENCE', 0.5),
        )

    def process_item(self, item, spider):
        """Filter by language."""
        adapter = ItemAdapter(item)

        # Check confidence
        confidence = adapter.get('language_confidence', 0.0)
        if confidence < self.min_confidence:
            raise DropItem(f"Low language confidence ({confidence}) in {adapter['url']}")

        # Check allowed languages
        if self.allowed_languages:
            lang_code = adapter.get('language_code')
            if lang_code not in self.allowed_languages:
                raise DropItem(f"Language {lang_code} not allowed in {adapter['url']}")

        return item


class DuplicatesPipeline:
    """
    Filter duplicate URLs.
    """

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        """Check for duplicates."""
        adapter = ItemAdapter(item)
        url = adapter['url']

        if url in self.urls_seen:
            raise DropItem(f"Duplicate URL: {url}")
        else:
            self.urls_seen.add(url)
            return item


class JsonLinesPipeline:
    """
    Store items as JSON Lines format.
    One JSON object per line, organized by language.
    """

    def __init__(self, output_dir):
        """
        Initialize pipeline.

        Args:
            output_dir: Directory to store output files
        """
        self.output_dir = output_dir
        self.files = {}
        self.stats = {}

    @classmethod
    def from_crawler(cls, crawler):
        """Create pipeline from crawler settings."""
        output_dir = crawler.settings.get('OUTPUT_DIR', './data/crawled')
        return cls(output_dir)

    def open_spider(self, spider):
        """Initialize when spider opens."""
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Output directory: {self.output_dir}")

    def close_spider(self, spider):
        """Clean up when spider closes."""
        # Close all open files
        for file_handle in self.files.values():
            file_handle.close()

        # Log statistics
        logger.info("Crawl statistics by language:")
        for lang, count in sorted(self.stats.items()):
            logger.info(f"  {lang}: {count} pages")

    def process_item(self, item, spider):
        """Store item to appropriate language file."""
        adapter = ItemAdapter(item)
        lang_code = adapter.get('language_code', 'unknown')

        # Get or create file handle for this language
        if lang_code not in self.files:
            filename = os.path.join(self.output_dir, f'{lang_code}.jsonl')
            self.files[lang_code] = open(filename, 'a', encoding='utf-8')
            self.stats[lang_code] = 0

        # Write item as JSON line
        line = json.dumps(dict(adapter), ensure_ascii=False) + '\n'
        self.files[lang_code].write(line)

        # Update statistics
        self.stats[lang_code] += 1

        return item


class StatisticsPipeline:
    """
    Collect crawl statistics.
    """

    def __init__(self):
        self.stats = {
            'total_pages': 0,
            'by_language': {},
            'by_domain': {},
            'avg_text_length': 0,
            'total_text_length': 0,
        }

    def process_item(self, item, spider):
        """Update statistics."""
        adapter = ItemAdapter(item)

        # Total pages
        self.stats['total_pages'] += 1

        # By language
        lang_code = adapter.get('language_code', 'unknown')
        self.stats['by_language'][lang_code] = self.stats['by_language'].get(lang_code, 0) + 1

        # By domain
        domain = adapter.get('domain', 'unknown')
        self.stats['by_domain'][domain] = self.stats['by_domain'].get(domain, 0) + 1

        # Text length
        text_length = adapter.get('text_length', 0)
        self.stats['total_text_length'] += text_length

        # Calculate average
        if self.stats['total_pages'] > 0:
            self.stats['avg_text_length'] = self.stats['total_text_length'] / self.stats['total_pages']

        return item

    def close_spider(self, spider):
        """Log final statistics."""
        logger.info("=" * 60)
        logger.info("FINAL CRAWL STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Total pages crawled: {self.stats['total_pages']}")
        logger.info(f"Average text length: {self.stats['avg_text_length']:.0f} chars")
        logger.info("")
        logger.info("Pages by language:")
        for lang, count in sorted(self.stats['by_language'].items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {lang}: {count}")
        logger.info("")
        logger.info("Top 10 domains:")
        top_domains = sorted(self.stats['by_domain'].items(), key=lambda x: x[1], reverse=True)[:10]
        for domain, count in top_domains:
            logger.info(f"  {domain}: {count}")
        logger.info("=" * 60)
