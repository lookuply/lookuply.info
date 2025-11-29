"""
Scrapy Items - Data Models
Define the structure of crawled data.
"""

import scrapy
from scrapy import Field


class WebPageItem(scrapy.Item):
    """
    Represents a crawled web page with all extracted data.
    """
    # URL and domain info
    url = Field()
    domain = Field()
    canonical_url = Field()

    # Content
    title = Field()
    description = Field()
    text = Field()
    text_length = Field()
    paragraphs = Field()
    headings = Field()

    # Language
    language_code = Field()
    language_confidence = Field()
    language_name = Field()

    # Metadata
    keywords = Field()
    author = Field()
    published_date = Field()
    modified_date = Field()

    # Open Graph & Social
    og_metadata = Field()
    twitter_metadata = Field()

    # Links
    links = Field()
    internal_links_count = Field()
    external_links_count = Field()

    # Technical
    status_code = Field()
    content_type = Field()
    encoding = Field()
    favicon = Field()

    # Crawl metadata
    crawled_at = Field()
    crawl_depth = Field()
    referrer = Field()

    # Flags
    is_valid = Field()
    is_eu_language = Field()


class LinkItem(scrapy.Item):
    """
    Represents a link found during crawling.
    """
    source_url = Field()
    target_url = Field()
    anchor_text = Field()
    link_type = Field()  # internal, external
    discovered_at = Field()
