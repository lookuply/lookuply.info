"""
Content Extraction Module
Extracts clean text content from HTML pages.
"""

import logging
import re
from typing import Optional, Dict
from bs4 import BeautifulSoup, Comment

logger = logging.getLogger(__name__)


class ContentExtractor:
    """
    Extract clean text content from HTML pages.
    Removes boilerplate, navigation, ads, and other non-content elements.
    """

    # Tags that typically contain boilerplate content
    BOILERPLATE_TAGS = [
        'nav', 'header', 'footer', 'aside', 'script', 'style',
        'noscript', 'iframe', 'form', 'button'
    ]

    # Classes/IDs that often indicate non-content
    BOILERPLATE_PATTERNS = [
        r'nav', r'menu', r'sidebar', r'footer', r'header', r'advertisement',
        r'ad-', r'ads', r'cookie', r'popup', r'modal', r'social', r'share',
        r'comment', r'related', r'recommended', r'trending'
    ]

    def __init__(self, min_text_length: int = 100):
        """
        Initialize content extractor.

        Args:
            min_text_length: Minimum length of text to consider valid content
        """
        self.min_text_length = min_text_length

    def extract(self, html: str, url: str = None) -> Dict[str, any]:
        """
        Extract content from HTML.

        Args:
            html: HTML content
            url: URL of the page (for logging)

        Returns:
            Dict containing extracted content:
                - text: Main content text
                - text_length: Length of extracted text
                - paragraphs: List of paragraphs
                - headings: List of headings
                - links: List of internal links
        """
        try:
            soup = BeautifulSoup(html, 'lxml')

            # Remove boilerplate elements
            self._remove_boilerplate(soup)

            # Extract main content
            main_content = self._find_main_content(soup)

            # Extract text
            text = self._extract_text(main_content)

            # Extract structural elements
            paragraphs = self._extract_paragraphs(main_content)
            headings = self._extract_headings(main_content)
            links = self._extract_links(main_content, url)

            return {
                'text': text,
                'text_length': len(text),
                'paragraphs': paragraphs,
                'headings': headings,
                'links': links,
                'is_valid': len(text) >= self.min_text_length
            }

        except Exception as e:
            logger.error(f"Content extraction failed for {url}: {e}")
            return {
                'text': '',
                'text_length': 0,
                'paragraphs': [],
                'headings': [],
                'links': [],
                'is_valid': False
            }

    def _remove_boilerplate(self, soup: BeautifulSoup):
        """Remove boilerplate elements from soup."""
        # Remove by tag name
        for tag in self.BOILERPLATE_TAGS:
            for element in soup.find_all(tag):
                element.decompose()

        # Remove HTML comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Remove by class/id patterns
        for pattern in self.BOILERPLATE_PATTERNS:
            regex = re.compile(pattern, re.IGNORECASE)

            for element in soup.find_all(class_=regex):
                element.decompose()

            for element in soup.find_all(id=regex):
                element.decompose()

    def _find_main_content(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Find the main content area of the page.
        Tries common content containers first, falls back to body.
        """
        # Try common main content selectors
        selectors = [
            ('article', None),
            ('main', None),
            ('div', 'main'),
            ('div', 'content'),
            ('div', 'article'),
            ('div', 'post'),
        ]

        for tag, class_name in selectors:
            if class_name:
                element = soup.find(tag, class_=re.compile(class_name, re.IGNORECASE))
            else:
                element = soup.find(tag)

            if element:
                return element

        # Fallback to body
        return soup.find('body') or soup

    def _extract_text(self, element: BeautifulSoup) -> str:
        """Extract clean text from element."""
        if not element:
            return ''

        # Get text
        text = element.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    def _extract_paragraphs(self, element: BeautifulSoup) -> list:
        """Extract paragraphs from element."""
        if not element:
            return []

        paragraphs = []
        for p in element.find_all('p'):
            text = p.get_text().strip()
            if len(text) > 50:  # Filter out short paragraphs
                paragraphs.append(text)

        return paragraphs

    def _extract_headings(self, element: BeautifulSoup) -> list:
        """Extract headings from element."""
        if not element:
            return []

        headings = []
        for level in range(1, 7):  # h1 to h6
            for heading in element.find_all(f'h{level}'):
                text = heading.get_text().strip()
                if text:
                    headings.append({
                        'level': level,
                        'text': text
                    })

        return headings

    def _extract_links(self, element: BeautifulSoup, base_url: Optional[str] = None) -> list:
        """Extract links from element."""
        if not element:
            return []

        from urllib.parse import urljoin, urlparse

        links = []
        for a in element.find_all('a', href=True):
            href = a['href'].strip()
            text = a.get_text().strip()

            # Skip empty or anchor-only links
            if not href or href.startswith('#'):
                continue

            # Convert to absolute URL if base_url provided
            if base_url:
                href = urljoin(base_url, href)

            # Parse URL
            parsed = urlparse(href)

            # Skip non-http(s) links
            if parsed.scheme not in ['http', 'https']:
                continue

            links.append({
                'url': href,
                'text': text,
                'domain': parsed.netloc
            })

        return links

    def extract_main_text_only(self, html: str) -> str:
        """
        Quick extraction of main text only.

        Args:
            html: HTML content

        Returns:
            Extracted text
        """
        result = self.extract(html)
        return result['text']
