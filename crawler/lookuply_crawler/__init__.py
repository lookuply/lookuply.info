"""
Lookuply Crawler - Multi-language Web Crawler

A production-ready Scrapy crawler for crawling web pages in all 24 EU languages.
"""

__version__ = '1.0.0'
__author__ = 'Lookuply Team'
__license__ = 'GPL-3.0'

from . import config
from . import extractors
from . import spiders
from . import pipelines
from . import middleware
from . import storage
from . import utils

__all__ = [
    'config',
    'extractors',
    'spiders',
    'pipelines',
    'middleware',
    'storage',
    'utils',
]
