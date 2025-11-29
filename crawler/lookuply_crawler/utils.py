"""
Utility Functions for Lookuply Crawler
"""

import hashlib
import os
import logging
from urllib.parse import urlparse, urljoin
from datetime import datetime

logger = logging.getLogger(__name__)


def normalize_url(url):
    """
    Normalize URL for consistency.

    Args:
        url: URL to normalize

    Returns:
        str: Normalized URL
    """
    from urllib.parse import urlunparse

    parsed = urlparse(url)

    # Convert scheme and netloc to lowercase
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Remove default ports
    if netloc.endswith(':80') and scheme == 'http':
        netloc = netloc[:-3]
    elif netloc.endswith(':443') and scheme == 'https':
        netloc = netloc[:-4]

    # Rebuild URL
    normalized = urlunparse((
        scheme,
        netloc,
        parsed.path or '/',
        parsed.params,
        parsed.query,
        ''  # Remove fragment
    ))

    return normalized


def get_domain(url):
    """
    Extract domain from URL.

    Args:
        url: URL to extract domain from

    Returns:
        str: Domain name
    """
    parsed = urlparse(url)
    return parsed.netloc


def get_url_hash(url):
    """
    Generate hash for URL.

    Args:
        url: URL to hash

    Returns:
        str: SHA256 hash of URL
    """
    normalized = normalize_url(url)
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def is_valid_url(url):
    """
    Check if URL is valid.

    Args:
        url: URL to validate

    Returns:
        bool: True if valid
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
    except Exception:
        return False


def get_file_extension(url):
    """
    Get file extension from URL.

    Args:
        url: URL to extract extension from

    Returns:
        str: File extension (without dot) or None
    """
    parsed = urlparse(url)
    path = parsed.path
    if '.' in path:
        return path.split('.')[-1].lower()
    return None


def clean_text(text):
    """
    Clean text content.

    Args:
        text: Text to clean

    Returns:
        str: Cleaned text
    """
    if not text:
        return ''

    # Remove extra whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    cleaned = '\n'.join(chunk for chunk in chunks if chunk)

    return cleaned


def truncate_text(text, max_length=1000):
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        str: Truncated text
    """
    if not text or len(text) <= max_length:
        return text

    return text[:max_length] + '...'


def ensure_dir(directory):
    """
    Ensure directory exists.

    Args:
        directory: Directory path
    """
    os.makedirs(directory, exist_ok=True)


def get_timestamp():
    """
    Get current timestamp.

    Returns:
        str: ISO format timestamp
    """
    return datetime.utcnow().isoformat()


def format_bytes(bytes_num):
    """
    Format bytes to human-readable format.

    Args:
        bytes_num: Number of bytes

    Returns:
        str: Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.1f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.1f} PB"


def calculate_crawl_rate(pages, duration_seconds):
    """
    Calculate crawl rate.

    Args:
        pages: Number of pages crawled
        duration_seconds: Duration in seconds

    Returns:
        float: Pages per second
    """
    if duration_seconds == 0:
        return 0.0
    return pages / duration_seconds


def estimate_time_remaining(pages_done, pages_total, duration_seconds):
    """
    Estimate time remaining for crawl.

    Args:
        pages_done: Pages already crawled
        pages_total: Total pages to crawl
        duration_seconds: Time spent so far

    Returns:
        float: Estimated seconds remaining
    """
    if pages_done == 0:
        return 0.0

    rate = calculate_crawl_rate(pages_done, duration_seconds)
    if rate == 0:
        return 0.0

    pages_remaining = pages_total - pages_done
    return pages_remaining / rate


def format_duration(seconds):
    """
    Format duration in seconds to human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        str: Formatted duration (e.g., "2h 15m 30s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return ' '.join(parts)


def safe_filename(text, max_length=200):
    """
    Create safe filename from text.

    Args:
        text: Text to convert
        max_length: Maximum filename length

    Returns:
        str: Safe filename
    """
    import re

    # Remove invalid characters
    safe = re.sub(r'[^\w\s-]', '', text).strip()
    # Replace spaces with underscores
    safe = re.sub(r'[-\s]+', '_', safe)
    # Truncate
    safe = safe[:max_length]

    return safe or 'unnamed'


def load_config(config_file):
    """
    Load configuration from file.

    Args:
        config_file: Path to config file (JSON or Python)

    Returns:
        dict: Configuration dictionary
    """
    import json

    if not os.path.exists(config_file):
        logger.error(f"Config file not found: {config_file}")
        return {}

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            if config_file.endswith('.json'):
                return json.load(f)
            else:
                # Execute Python file and extract variables
                namespace = {}
                exec(f.read(), namespace)
                return {k: v for k, v in namespace.items() if not k.startswith('_')}
    except Exception as e:
        logger.error(f"Failed to load config from {config_file}: {e}")
        return {}
