"""
Metadata Extraction Module
Extracts metadata from HTML pages (title, description, keywords, etc.).
"""

import logging
from typing import Dict, Optional, List
from bs4 import BeautifulSoup
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class MetadataExtractor:
    """
    Extract metadata from HTML pages.
    Handles Open Graph, Twitter Cards, and standard meta tags.
    """

    def extract(self, html: str, url: str = None) -> Dict[str, any]:
        """
        Extract all metadata from HTML.

        Args:
            html: HTML content
            url: URL of the page

        Returns:
            Dict containing metadata
        """
        try:
            soup = BeautifulSoup(html, 'lxml')

            metadata = {
                'title': self._extract_title(soup),
                'description': self._extract_description(soup),
                'keywords': self._extract_keywords(soup),
                'author': self._extract_author(soup),
                'language': self._extract_language(soup),
                'canonical_url': self._extract_canonical_url(soup, url),
                'og': self._extract_open_graph(soup),
                'twitter': self._extract_twitter_card(soup),
                'published_date': self._extract_published_date(soup),
                'modified_date': self._extract_modified_date(soup),
                'favicon': self._extract_favicon(soup, url),
            }

            return metadata

        except Exception as e:
            logger.error(f"Metadata extraction failed for {url}: {e}")
            return self._empty_metadata()

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract page title."""
        # Try Open Graph title first
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()

        # Try standard title tag
        title_tag = soup.find('title')
        if title_tag and title_tag.string:
            return title_tag.string.strip()

        # Try h1 as fallback
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()

        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract page description."""
        # Try Open Graph description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc['content'].strip()

        # Try standard meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()

        return None

    def _extract_keywords(self, soup: BeautifulSoup) -> List[str]:
        """Extract keywords from meta tags."""
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_tag and keywords_tag.get('content'):
            keywords = keywords_tag['content'].strip()
            return [k.strip() for k in keywords.split(',') if k.strip()]

        return []

    def _extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract author information."""
        # Try meta author tag
        author_tag = soup.find('meta', attrs={'name': 'author'})
        if author_tag and author_tag.get('content'):
            return author_tag['content'].strip()

        # Try Open Graph article author
        og_author = soup.find('meta', property='article:author')
        if og_author and og_author.get('content'):
            return og_author['content'].strip()

        return None

    def _extract_language(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract language hints from HTML."""
        # Try html lang attribute
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            return html_tag['lang'].strip()

        # Try Open Graph locale
        og_locale = soup.find('meta', property='og:locale')
        if og_locale and og_locale.get('content'):
            return og_locale['content'].strip()

        # Try content-language meta tag
        lang_tag = soup.find('meta', attrs={'http-equiv': 'content-language'})
        if lang_tag and lang_tag.get('content'):
            return lang_tag['content'].strip()

        return None

    def _extract_canonical_url(self, soup: BeautifulSoup, fallback_url: str = None) -> Optional[str]:
        """Extract canonical URL."""
        # Try canonical link tag
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical.get('href'):
            return canonical['href'].strip()

        # Try Open Graph URL
        og_url = soup.find('meta', property='og:url')
        if og_url and og_url.get('content'):
            return og_url['content'].strip()

        return fallback_url

    def _extract_open_graph(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract Open Graph metadata."""
        og_data = {}

        og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))

        for tag in og_tags:
            property_name = tag['property'].replace('og:', '')
            content = tag.get('content', '').strip()
            if content:
                og_data[property_name] = content

        return og_data

    def _extract_twitter_card(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract Twitter Card metadata."""
        twitter_data = {}

        twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})

        for tag in twitter_tags:
            name = tag['name'].replace('twitter:', '')
            content = tag.get('content', '').strip()
            if content:
                twitter_data[name] = content

        return twitter_data

    def _extract_published_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract publication date."""
        # Try article:published_time
        published = soup.find('meta', property='article:published_time')
        if published and published.get('content'):
            return published['content'].strip()

        # Try datePublished
        date_published = soup.find('meta', attrs={'itemprop': 'datePublished'})
        if date_published and date_published.get('content'):
            return date_published['content'].strip()

        return None

    def _extract_modified_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract last modified date."""
        # Try article:modified_time
        modified = soup.find('meta', property='article:modified_time')
        if modified and modified.get('content'):
            return modified['content'].strip()

        # Try dateModified
        date_modified = soup.find('meta', attrs={'itemprop': 'dateModified'})
        if date_modified and date_modified.get('content'):
            return date_modified['content'].strip()

        return None

    def _extract_favicon(self, soup: BeautifulSoup, base_url: str = None) -> Optional[str]:
        """Extract favicon URL."""
        from urllib.parse import urljoin

        # Try icon link tags
        icon_tags = soup.find_all('link', rel=lambda x: x and 'icon' in x.lower())

        for tag in icon_tags:
            href = tag.get('href')
            if href:
                if base_url:
                    return urljoin(base_url, href)
                return href

        # Fallback to /favicon.ico
        if base_url:
            parsed = urlparse(base_url)
            return f"{parsed.scheme}://{parsed.netloc}/favicon.ico"

        return None

    def _empty_metadata(self) -> Dict[str, any]:
        """Return empty metadata structure."""
        return {
            'title': None,
            'description': None,
            'keywords': [],
            'author': None,
            'language': None,
            'canonical_url': None,
            'og': {},
            'twitter': {},
            'published_date': None,
            'modified_date': None,
            'favicon': None,
        }
