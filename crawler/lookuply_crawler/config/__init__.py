"""
Configuration package for Lookuply Crawler.
"""

from .languages import (
    LANGUAGES,
    LANGUAGE_CODES,
    LANGUAGE_NAMES,
    NATIVE_NAMES,
    get_language_info,
    is_valid_language,
    get_all_language_codes,
)
from .urls import (
    START_URLS,
    get_start_urls,
    get_all_start_urls,
    get_urls_count_by_language,
)
from .domain_filters import (
    GLOBAL_BLOCKED_DOMAINS,
    PREFERRED_DOMAINS,
    BLOCKED_EXTENSIONS,
    is_domain_allowed,
    should_prioritize_domain,
)

__all__ = [
    'LANGUAGES',
    'LANGUAGE_CODES',
    'LANGUAGE_NAMES',
    'NATIVE_NAMES',
    'get_language_info',
    'is_valid_language',
    'get_all_language_codes',
    'START_URLS',
    'get_start_urls',
    'get_all_start_urls',
    'get_urls_count_by_language',
    'GLOBAL_BLOCKED_DOMAINS',
    'PREFERRED_DOMAINS',
    'BLOCKED_EXTENSIONS',
    'is_domain_allowed',
    'should_prioritize_domain',
]
