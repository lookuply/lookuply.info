"""
Web Spider - Main crawler for multi-language web pages
"""

import logging
from urllib.parse import urlparse
import scrapy
from .base_spider import BaseSpider
from ..items import WebPageItem
from ..config import get_all_start_urls, LANGUAGE_CODES

logger = logging.getLogger(__name__)


class WebSpider(BaseSpider):
    """
    Main web spider for crawling multi-language content.

    Features:
    - Crawls from curated start URLs for all 24 EU languages
    - Detects language of each page
    - Follows internal and relevant external links
    - Respects robots.txt and politeness policies
    - Stores data organized by language
    """

    name = 'web_spider'

    def __init__(self, languages=None, max_pages=None, *args, **kwargs):
        """
        Initialize web spider.

        Args:
            languages: Comma-separated list of language codes to crawl (default: all)
            max_pages: Maximum number of pages to crawl per language (default: unlimited)
        """
        super(WebSpider, self).__init__(*args, **kwargs)

        # Parse language filter
        if languages:
            self.target_languages = [lang.strip() for lang in languages.split(',')]
        else:
            self.target_languages = LANGUAGE_CODES

        # Max pages per language
        self.max_pages = int(max_pages) if max_pages else None

        # Track pages crawled per language
        self.pages_per_language = {lang: 0 for lang in self.target_languages}

        logger.info(f"Spider initialized for languages: {', '.join(self.target_languages)}")
        if self.max_pages:
            logger.info(f"Maximum pages per language: {self.max_pages}")

    def start_requests(self):
        """
        Generate initial requests from start URLs.
        """
        from ..config import get_start_urls

        for lang_code in self.target_languages:
            start_urls = get_start_urls(lang_code)

            logger.info(f"Starting crawl for {lang_code}: {len(start_urls)} seed URLs")

            for url in start_urls:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    errback=self.errback_httpbin,
                    meta={
                        'target_language': lang_code,
                        'depth': 0,
                    },
                    dont_filter=False,
                )

    def parse(self, response):
        """
        Parse response and extract data.

        Args:
            response: Scrapy response object

        Yields:
            WebPageItem: Scraped item
            scrapy.Request: Follow-up requests
        """
        self.stats['responses_received'] += 1

        try:
            # Extract content
            data = self.extract_content(response)

            if not data:
                logger.warning(f"Failed to extract content from {response.url}")
                return

            # Create item
            item = WebPageItem(**data)

            # Check language limit
            lang_code = data['language_code']
            if lang_code in self.pages_per_language:
                if self.max_pages and self.pages_per_language[lang_code] >= self.max_pages:
                    logger.info(f"Reached max pages for {lang_code}, skipping {response.url}")
                    return

                self.pages_per_language[lang_code] += 1

            self.stats['items_scraped'] += 1

            yield item

            # Extract and follow links
            if response.meta.get('depth', 0) < self.settings.get('DEPTH_LIMIT', 3):
                for link in self.extract_links(response):
                    if self.should_follow_link(link.url, response.url):
                        self.stats['requests_sent'] += 1

                        yield scrapy.Request(
                            url=link.url,
                            callback=self.parse,
                            errback=self.errback_httpbin,
                            meta={
                                'depth': response.meta.get('depth', 0) + 1,
                                'referrer': response.url,
                            },
                        )

        except Exception as e:
            logger.error(f"Error parsing {response.url}: {e}")
            self.stats['errors'] += 1
