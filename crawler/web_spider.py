"""
Lookuply Web Spider

Multi-language web crawler supporting all 24 EU official languages.
Uses language detection and content extraction.
"""

import logging
from typing import Generator
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from config_languages import LANGUAGES, START_URLS, PAGES_PER_LANGUAGE
from language_detector import LanguageDetector
from content_extractor import ContentExtractor

logger = logging.getLogger(__name__)


class WebSpider(CrawlSpider):
    """
    Main web crawler spider for Lookuply

    Crawls websites in all 24 EU languages.
    Detects language automatically.
    Extracts content and metadata.
    """

    name = 'web_spider'
    allowed_domains = []
    start_urls = []

    # Crawl configuration
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOAD_DELAY': 1.5,
        'USER_AGENT': 'Mozilla/5.0 (compatible; LookuplyBot/1.0; +https://lookuply.info)',
        'COOKIES_ENABLED': False,
        'TELNETCONSOLE_ENABLED': False,
    }

    # Link extraction rules
    rules = (
        Rule(
            LinkExtractor(
                allow_domains=None,
                deny=[
                    r'\.pdf$',
                    r'\.jpg$|\.png$|\.gif$',
                    r'\.zip$|\.exe$',
                    r'twitter\.com',
                    r'facebook\.com',
                    r'youtube\.com',
                ],
            ),
            callback='parse_page',
            follow=True,
            errback='errback',
        ),
    )

    def __init__(self, language='en', *args, **kwargs):
        """
        Initialize spider for specific language

        Args:
            language: Language code (en, de, fr, etc.)
        """
        super(WebSpider, self).__init__(*args, **kwargs)

        self.language = language.lower()
        self.pages_crawled = 0
        self.pages_target = PAGES_PER_LANGUAGE.get(self.language, 50000)

        # Setup
        self._setup_language()
        self._setup_extractors()

        logger.info(f"🕷️ Crawler started for {self.language.upper()}")
        logger.info(f"Target: {self.pages_target} pages")

    def _setup_language(self):
        """Setup language-specific configuration"""
        if self.language not in LANGUAGES:
            logger.error(f"Unknown language: {self.language}")
            self.start_urls = []
            return

        # Get start URLs for language
        self.start_urls = START_URLS.get(self.language, [])

        # Setup allowed domains
        import re
        from urllib.parse import urlparse

        self.allowed_domains = list(set(
            urlparse(url).netloc.replace('www.', '')
            for url in self.start_urls
        ))

        logger.info(f"Start URLs: {len(self.start_urls)}")
        logger.info(f"Allowed domains: {len(self.allowed_domains)}")

    def _setup_extractors(self):
        """Initialize content extractors"""
        try:
            self.language_detector = LanguageDetector()
            self.content_extractor = ContentExtractor()
        except Exception as e:
            logger.error(f"Failed to initialize extractors: {e}")
            raise

    def parse_page(self, response):
        """
        Parse crawled page

        Args:
            response: Scrapy response object

        Yields:
            Extracted page data
        """
        self.pages_crawled += 1

        # Check if we've reached target
        if self.pages_crawled > self.pages_target:
            logger.info(f"Target reached for {self.language.upper()}: {self.pages_crawled} pages")
            return

        try:
            # Detect language
            sample_text = response.text[:1000]
            detected_lang, confidence = self.language_detector.detect(sample_text)

            # Skip if language doesn't match
            if detected_lang != self.language and confidence > 0.8:
                logger.debug(f"Skipped non-{self.language} page: {detected_lang} ({confidence:.2f})")
                return

            # Extract content
            extracted = self.content_extractor.extract(response.text, response.url)

            # Skip if no content
            if not extracted['content']:
                logger.debug(f"No content extracted from {response.url}")
                return

            # Yield page data
            yield {
                'url': response.url,
                'title': extracted['title'],
                'description': extracted['description'],
                'content': extracted['content'],
                'language': self.language,
                'detected_language': detected_lang,
                'language_confidence': confidence,
                'links': extracted['links'],
                'metadata': extracted['metadata'],
                'crawl_time': response.headers.get('Date', b'').decode('utf-8'),
                'status_code': response.status,
            }

            # Log progress
            if self.pages_crawled % 100 == 0:
                logger.info(f"[{self.language.upper()}] Progress: {self.pages_crawled}/{self.pages_target} pages")

        except Exception as e:
            logger.error(f"Error processing {response.url}: {e}")

    def errback(self, failure):
        """Handle request errors"""
        logger.warning(f"Request failed: {failure.request.url} - {failure.value}")


class MultiLanguageCrawler:
    """
    Controller for crawling multiple languages in parallel
    """

    def __init__(self):
        """Initialize multi-language crawler"""
        self.languages = list(LANGUAGES.keys())
        logger.info(f"Multi-language crawler initialized for {len(self.languages)} languages")

    def get_spider_for_language(self, language: str) -> WebSpider:
        """Get spider instance for specific language"""
        return WebSpider(language=language)

    def crawl_all(self):
        """Start crawling all languages"""
        from scrapy.crawler import CrawlerProcess

        process = CrawlerProcess()

        for language in self.languages:
            spider = self.get_spider_for_language(language)
            process.crawl(spider)

        logger.info(f"Starting crawling for {len(self.languages)} languages...")
        process.start()
