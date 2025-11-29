"""
Domain Filtering Configuration
Define allowed and blocked domains per language and globally.
"""

# Global blocked domains (spam, adult content, etc.)
GLOBAL_BLOCKED_DOMAINS = [
    # Add spam/malicious domains here
    'example-spam.com',
    'malware-site.com',
]

# Preferred domains per language (optional - to prioritize certain domains)
PREFERRED_DOMAINS = {
    'bg': ['.bg', 'wikipedia.org'],
    'hr': ['.hr', 'wikipedia.org'],
    'cs': ['.cz', 'wikipedia.org'],
    'da': ['.dk', 'wikipedia.org'],
    'nl': ['.nl', '.be', 'wikipedia.org'],
    'en': ['.uk', '.ie', '.com', 'wikipedia.org'],
    'et': ['.ee', 'wikipedia.org'],
    'fi': ['.fi', 'wikipedia.org'],
    'fr': ['.fr', '.be', '.ch', 'wikipedia.org'],
    'de': ['.de', '.at', '.ch', 'wikipedia.org'],
    'el': ['.gr', 'wikipedia.org'],
    'hu': ['.hu', 'wikipedia.org'],
    'ga': ['.ie', 'wikipedia.org'],
    'it': ['.it', '.ch', 'wikipedia.org'],
    'lv': ['.lv', 'wikipedia.org'],
    'lt': ['.lt', 'wikipedia.org'],
    'mt': ['.mt', 'wikipedia.org'],
    'pl': ['.pl', 'wikipedia.org'],
    'pt': ['.pt', 'wikipedia.org'],
    'ro': ['.ro', 'wikipedia.org'],
    'sk': ['.sk', 'wikipedia.org'],
    'sl': ['.si', 'wikipedia.org'],
    'es': ['.es', 'wikipedia.org'],
    'sv': ['.se', 'wikipedia.org'],
}

# File extensions to skip
BLOCKED_EXTENSIONS = [
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'zip', 'rar', 'tar', 'gz', '7z',
    'mp3', 'mp4', 'avi', 'mov', 'wmv', 'flv',
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'ico',
    'exe', 'dmg', 'pkg', 'deb', 'rpm',
]


def is_domain_allowed(url: str, language_code: str = None) -> bool:
    """
    Check if a domain is allowed for crawling.

    Args:
        url: The URL to check
        language_code: Optional language code for language-specific filtering

    Returns:
        bool: True if domain is allowed, False otherwise
    """
    from urllib.parse import urlparse

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # Check global blocklist
    for blocked in GLOBAL_BLOCKED_DOMAINS:
        if blocked in domain:
            return False

    # Check file extensions
    path = parsed.path.lower()
    for ext in BLOCKED_EXTENSIONS:
        if path.endswith(f'.{ext}'):
            return False

    return True


def should_prioritize_domain(url: str, language_code: str) -> bool:
    """
    Check if a domain should be prioritized for a specific language.

    Args:
        url: The URL to check
        language_code: Language code

    Returns:
        bool: True if domain should be prioritized
    """
    from urllib.parse import urlparse

    if language_code not in PREFERRED_DOMAINS:
        return False

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    for preferred in PREFERRED_DOMAINS[language_code]:
        if preferred in domain:
            return True

    return False
