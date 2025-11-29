"""
Base Spider - Foundation for all Lookuply spiders
"""

import logging
from datetime import datetime
from urllib.parse import urlparse
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

logger = logging.getLogger(__name__)


class BaseSpider(scrapy.Spider):
    """
    Base spider class with common functionality for all Lookuply spiders.

    Features:
    - robots.txt compliance
    - Politeness policies
    - Error handling
    - Language detection
    - Domain filtering
    """

    name = 'base_spider'

    # Custom settings that all spiders inherit
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'DOWNLOAD_DELAY': 1.5,
        'DOWNLOAD_TIMEOUT': 30,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429],

        # AutoThrottle for adaptive crawling
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1.5,
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 8.0,

        # Memory and item limits
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_WARNING_MB': 1536,

        # Cookies and redirects
        'COOKIES_ENABLED': False,
        'REDIRECT_ENABLED': True,
        'REDIRECT_MAX_TIMES': 3,

        # Compression
        'COMPRESSION_ENABLED': True,

        # Depth limit
        'DEPTH_LIMIT': 3,
        'DEPTH_PRIORITY': 1,

        # Item pipelines
        'ITEM_PIPELINES': {
            'lookuply_crawler.pipelines.ValidationPipeline': 100,
            'lookuply_crawler.pipelines.LanguageFilterPipeline': 200,
            'lookuply_crawler.pipelines.DuplicatesPipeline': 300,
            'lookuply_crawler.pipelines.JsonLinesPipeline': 400,
            'lookuply_crawler.pipelines.StatisticsPipeline': 500,
        },

        # Middleware
        'DOWNLOADER_MIDDLEWARES': {
            'lookuply_crawler.middleware.RandomUserAgentMiddleware': 400,
            'lookuply_crawler.middleware.ContentTypeFilterMiddleware': 543,
            'lookuply_crawler.middleware.LanguageDetectionMiddleware': 544,
            'lookuply_crawler.middleware.PolitenessPolicyMiddleware': 545,
        },

        # Logging
        'LOG_LEVEL': 'INFO',
        'LOG_FORMAT': '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        'LOG_DATEFORMAT': '%Y-%m-%d %H:%M:%S',
    }

    def __init__(self, *args, **kwargs):
        """Initialize base spider."""
        super(BaseSpider, self).__init__(*args, **kwargs)

        # Statistics
        self.stats = {
            'requests_sent': 0,
            'responses_received': 0,
            'items_scraped': 0,
            'errors': 0,
        }

        # Link extractor for following links
        self.link_extractor = LinkExtractor(
            allow_domains=None,  # Set in subclass
            deny_extensions=[
                'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
                'zip', 'rar', 'tar', 'gz', '7z',
                'mp3', 'mp4', 'avi', 'mov', 'wmv', 'flv',
                'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'ico',
                'exe', 'dmg', 'pkg', 'deb', 'rpm',
            ],
            unique=True,
        )

    def parse(self, response):
        """
        Default parse method - should be overridden in subclasses.
        """
        raise NotImplementedError("Subclasses must implement parse method")

    def extract_content(self, response):
        """
        Extract content from response.

        Args:
            response: Scrapy response object

        Returns:
            dict: Extracted content
        """
        from ..extractors import ContentExtractor, MetadataExtractor, get_detector

        try:
            # Extract content
            content_extractor = ContentExtractor()
            content = content_extractor.extract(response.text, response.url)

            # Extract metadata
            metadata_extractor = MetadataExtractor()
            metadata = metadata_extractor.extract(response.text, response.url)

            # Detect language
            detector = get_detector()
            lang_code, confidence = detector.detect(content['text'])

            # Check if EU language
            from ..config import is_valid_language
            is_eu_lang = is_valid_language(lang_code)

            # Get language name
            from ..config import get_language_info
            lang_info = get_language_info(lang_code)
            lang_name = lang_info['name'] if lang_info else 'Unknown'

            # Combine all data
            return {
                'url': response.url,
                'domain': urlparse(response.url).netloc,
                'canonical_url': metadata['canonical_url'],
                'title': metadata['title'],
                'description': metadata['description'],
                'text': content['text'],
                'text_length': content['text_length'],
                'paragraphs': content['paragraphs'],
                'headings': content['headings'],
                'language_code': lang_code,
                'language_confidence': confidence,
                'language_name': lang_name,
                'keywords': metadata['keywords'],
                'author': metadata['author'],
                'published_date': metadata['published_date'],
                'modified_date': metadata['modified_date'],
                'og_metadata': metadata['og'],
                'twitter_metadata': metadata['twitter'],
                'links': content['links'],
                'internal_links_count': len([l for l in content['links'] if urlparse(response.url).netloc in l['url']]),
                'external_links_count': len([l for l in content['links'] if urlparse(response.url).netloc not in l['url']]),
                'status_code': response.status,
                'content_type': response.headers.get('Content-Type', b'').decode('utf-8', errors='ignore'),
                'encoding': response.encoding,
                'favicon': metadata['favicon'],
                'crawled_at': datetime.utcnow().isoformat(),
                'crawl_depth': response.meta.get('depth', 0),
                'referrer': response.request.headers.get('Referer', b'').decode('utf-8', errors='ignore'),
                'is_valid': content['is_valid'],
                'is_eu_language': is_eu_lang,
            }

        except Exception as e:
            logger.error(f"Content extraction failed for {response.url}: {e}")
            return None

    def extract_links(self, response):
        """
        Extract links from response for crawling.

        Args:
            response: Scrapy response object

        Returns:
            list: Extracted links
        """
        try:
            links = self.link_extractor.extract_links(response)
            return links
        except Exception as e:
            logger.error(f"Link extraction failed for {response.url}: {e}")
            return []

    def should_follow_link(self, url, source_url=None):
        """
        Determine if a link should be followed.

        Args:
            url: URL to check
            source_url: Source URL (optional)

        Returns:
            bool: True if link should be followed
        """
        from ..config import is_domain_allowed

        return is_domain_allowed(url)

    def errback_httpbin(self, failure):
        """
        Handle request errors.

        Args:
            failure: Twisted failure object
        """
        self.stats['errors'] += 1

        # Log errors
        if failure.check(HttpError):
            response = failure.value.response
            logger.error(f'HttpError on {response.url}: {response.status}')

        elif failure.check(DNSLookupError):
            request = failure.request
            logger.error(f'DNSLookupError on {request.url}')

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            logger.error(f'TimeoutError on {request.url}')

        else:
            request = failure.request
            logger.error(f'Error on {request.url}: {failure.value}')

    def closed(self, reason):
        """
        Called when spider closes.

        Args:
            reason: Reason for closing
        """
        logger.info("=" * 60)
        logger.info(f"Spider {self.name} closed: {reason}")
        logger.info("=" * 60)
        logger.info(f"Requests sent: {self.stats['requests_sent']}")
        logger.info(f"Responses received: {self.stats['responses_received']}")
        logger.info(f"Items scraped: {self.stats['items_scraped']}")
        logger.info(f"Errors: {self.stats['errors']}")
        logger.info("=" * 60)
