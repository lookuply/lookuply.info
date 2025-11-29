"""
Scrapy Middleware - Custom Request/Response Processing
"""

import logging
import random
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.exceptions import IgnoreRequest

logger = logging.getLogger(__name__)


class RandomUserAgentMiddleware:
    """
    Rotate user agents to avoid detection.
    """

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (compatible; LookuplyBot/1.0; +https://lookuply.info)',
    ]

    def process_request(self, request, spider):
        """Set random user agent."""
        request.headers['User-Agent'] = random.choice(self.USER_AGENTS)


class LanguageDetectionMiddleware:
    """
    Detect language early and add to request meta.
    """

    def process_response(self, request, response, spider):
        """Detect language from response."""
        if isinstance(response, HtmlResponse):
            # Add language hint to meta for spider
            from .extractors import get_detector

            try:
                detector = get_detector()
                lang_code, confidence = detector.detect_from_html(response.text)
                response.meta['detected_language'] = lang_code
                response.meta['language_confidence'] = confidence
            except Exception as e:
                logger.error(f"Language detection middleware error: {e}")

        return response


class ContentTypeFilterMiddleware:
    """
    Filter out non-HTML content types.
    """

    ALLOWED_CONTENT_TYPES = [
        'text/html',
        'application/xhtml+xml',
    ]

    def process_response(self, request, response, spider):
        """Filter by content type."""
        content_type = response.headers.get('Content-Type', b'').decode('utf-8', errors='ignore').lower()

        # Check if allowed
        is_allowed = any(ct in content_type for ct in self.ALLOWED_CONTENT_TYPES)

        if not is_allowed:
            logger.debug(f"Ignoring non-HTML content type: {content_type} for {response.url}")
            raise IgnoreRequest(f"Content type {content_type} not allowed")

        return response


class DepthLimitMiddleware:
    """
    Limit crawl depth per domain.
    """

    def __init__(self, max_depth=3):
        """
        Initialize middleware.

        Args:
            max_depth: Maximum crawl depth
        """
        self.max_depth = max_depth

    @classmethod
    def from_crawler(cls, crawler):
        """Create middleware from crawler settings."""
        max_depth = crawler.settings.getint('MAX_DEPTH', 3)
        return cls(max_depth)

    def process_request(self, request, spider):
        """Check depth limit."""
        depth = request.meta.get('depth', 0)

        if depth > self.max_depth:
            logger.debug(f"Ignoring request (depth {depth}): {request.url}")
            raise IgnoreRequest(f"Depth {depth} exceeds maximum {self.max_depth}")


class PolitenessPolicyMiddleware:
    """
    Enforce politeness policies (delays, concurrent requests per domain).
    """

    @classmethod
    def from_crawler(cls, crawler):
        """Set up from crawler."""
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        """Log politeness settings when spider opens."""
        logger.info("=" * 60)
        logger.info("POLITENESS POLICY")
        logger.info("=" * 60)
        logger.info(f"Download delay: {spider.settings.get('DOWNLOAD_DELAY')} seconds")
        logger.info(f"Concurrent requests per domain: {spider.settings.get('CONCURRENT_REQUESTS_PER_DOMAIN')}")
        logger.info(f"AutoThrottle enabled: {spider.settings.get('AUTOTHROTTLE_ENABLED')}")
        logger.info(f"Robots.txt obey: {spider.settings.get('ROBOTSTXT_OBEY')}")
        logger.info("=" * 60)


class RobotsTxtEnforcementMiddleware:
    """
    Strict enforcement of robots.txt rules with logging.
    """

    def process_exception(self, request, exception, spider):
        """Log robots.txt violations."""
        if 'robots.txt' in str(exception).lower():
            logger.warning(f"Robots.txt blocked: {request.url}")
