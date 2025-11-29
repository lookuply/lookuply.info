"""
Content Extraction Module for Lookuply Crawler

Extracts text content, metadata, and links from HTML pages.
Handles boilerplate removal and content cleaning.
"""

import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ContentExtractor:
    """Extracts meaningful content from HTML pages"""

    # Tags to remove (boilerplate, navigation, ads)
    REMOVE_TAGS = {
        'script', 'style', 'nav', 'footer', 'header',
        'aside', 'form', 'noscript', 'iframe'
    }

    # Text extraction selectors (content areas)
    CONTENT_SELECTORS = [
        'article',
        'main',
        '[role="main"]',
        '.post-content',
        '.entry-content',
        '.content',
        '#content',
    ]

    def __init__(self):
        """Initialize content extractor"""
        self.logger = logging.getLogger(__name__)

    def extract(self, html: str, url: str) -> Dict:
        """
        Extract all content from HTML page

        Args:
            html: Raw HTML content
            url: Page URL (for resolving relative links)

        Returns:
            Dictionary with extracted content:
            {
                'title': 'Page Title',
                'description': 'Meta description',
                'content': 'Main text content',
                'links': ['url1', 'url2', ...],
                'language_hints': ['en', 'fr'],
                'metadata': {
                    'author': '...',
                    'published': '2025-01-01',
                    'keywords': 'word1, word2'
                }
            }
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
        except Exception as e:
            self.logger.error(f"Failed to parse HTML: {e}")
            return self._empty_result()

        result = {
            'title': self._extract_title(soup),
            'description': self._extract_description(soup),
            'content': self._extract_content(soup),
            'links': self._extract_links(soup, url),
            'language_hints': self._extract_language_hints(soup),
            'metadata': self._extract_metadata(soup),
        }

        return result

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        # Try various title sources
        title = None

        # <title> tag
        if soup.title:
            title = soup.title.string

        # og:title meta tag
        if not title:
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                title = og_title.get('content')

        # h1 tag as fallback
        if not title:
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text(strip=True)

        return (title or '').strip()[:200]

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description"""
        # Try meta description
        desc = soup.find('meta', attrs={'name': 'description'})
        if desc and desc.get('content'):
            return desc.get('content').strip()[:300]

        # Try og:description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc.get('content').strip()[:300]

        return ''

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main text content"""
        # Remove boilerplate
        for tag in soup.find_all(self.REMOVE_TAGS):
            tag.decompose()

        # Try to find main content area
        content_elem = None
        for selector in self.CONTENT_SELECTORS:
            content_elem = soup.select_one(selector)
            if content_elem:
                break

        # Fallback to body
        if not content_elem:
            content_elem = soup.find('body') or soup

        # Extract text
        text = content_elem.get_text(separator='\n', strip=True)

        # Clean up whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)

        # Limit length
        return text[:50000]

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all internal and external links"""
        links = set()

        try:
            base_domain = urlparse(base_url).netloc
        except:
            base_domain = ''

        for link in soup.find_all('a', href=True):
            try:
                url = link.get('href')
                if not url or url.startswith('#'):
                    continue

                # Convert relative to absolute URLs
                absolute_url = urljoin(base_url, url)

                # Filter out common junk URLs
                if not self._is_junk_url(absolute_url):
                    links.add(absolute_url)
            except Exception as e:
                self.logger.debug(f"Error processing link: {e}")
                continue

        return list(links)[:100]  # Limit to 100 links

    def _extract_language_hints(self, soup: BeautifulSoup) -> List[str]:
        """Extract language hints from HTML"""
        hints = []

        # HTML lang attribute
        html = soup.find('html')
        if html and html.get('lang'):
            hints.append(html.get('lang')[:2].lower())

        # Meta language tags
        for meta in soup.find_all('meta', attrs={'http-equiv': 'content-language'}):
            if meta.get('content'):
                hints.append(meta.get('content')[:2].lower())

        return list(set(hints))

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict:
        """Extract additional metadata"""
        metadata = {}

        # Author
        author = soup.find('meta', attrs={'name': 'author'})
        if author and author.get('content'):
            metadata['author'] = author.get('content')

        # Keywords
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        if keywords and keywords.get('content'):
            metadata['keywords'] = keywords.get('content')

        # Published date
        published = soup.find('meta', attrs={'property': 'article:published_time'})
        if published and published.get('content'):
            metadata['published'] = published.get('content')

        # Open Graph image
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            metadata['image'] = og_image.get('content')

        return metadata

    @staticmethod
    def _is_junk_url(url: str) -> bool:
        """Check if URL is junk (ads, trackers, etc.)"""
        junk_patterns = [
            'doubleclick.net',
            'facebook.com/tr',
            'google-analytics',
            'googleads',
            'ads.google',
            'adservice',
            'tracking',
            'analytics',
        ]

        for pattern in junk_patterns:
            if pattern in url.lower():
                return True

        return False

    @staticmethod
    def _empty_result() -> Dict:
        """Return empty result structure"""
        return {
            'title': '',
            'description': '',
            'content': '',
            'links': [],
            'language_hints': [],
            'metadata': {},
        }
