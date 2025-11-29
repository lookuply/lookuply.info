"""
Scrapy Settings for Lookuply Crawler

For more information on settings, see:
https://docs.scrapy.org/en/latest/topics/settings.html
"""

BOT_NAME = 'lookuply_crawler'

SPIDER_MODULES = ['lookuply_crawler.spiders']
NEWSPIDER_MODULE = 'lookuply_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (compatible; LookuplyBot/1.0; +https://lookuply.info)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1.5

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 0

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en,de,fr,es,it,nl,pl,pt,ro,sv,fi,da,cs,hu,el,bg,sk,sl,hr,lt,lv,et,ga,mt',
}

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'lookuply_crawler.middleware.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # Disabled
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
    'lookuply_crawler.middleware.ContentTypeFilterMiddleware': 543,
    'lookuply_crawler.middleware.LanguageDetectionMiddleware': 544,
    'lookuply_crawler.middleware.PolitenessPolicyMiddleware': 545,
}

# Enable or disable extensions
EXTENSIONS = {
    'scrapy.extensions.logstats.LogStats': 500,
    'scrapy.extensions.memusage.MemoryUsage': 100,
    'scrapy.extensions.corestats.CoreStats': 0,
}

# Configure item pipelines
ITEM_PIPELINES = {
    'lookuply_crawler.pipelines.ValidationPipeline': 100,
    'lookuply_crawler.pipelines.LanguageFilterPipeline': 200,
    'lookuply_crawler.pipelines.DuplicatesPipeline': 300,
    'lookuply_crawler.pipelines.JsonLinesPipeline': 400,
    'lookuply_crawler.pipelines.StatisticsPipeline': 500,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True

# The initial download delay
AUTOTHROTTLE_START_DELAY = 1.5

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10

# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 8.0

# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400  # 24 hours
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 403, 404, 408]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set download timeout
DOWNLOAD_TIMEOUT = 30

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# Memory usage
MEMUSAGE_LIMIT_MB = 2048
MEMUSAGE_WARNING_MB = 1536
MEMUSAGE_NOTIFY_MAIL = []

# Depth limit
DEPTH_LIMIT = 3
DEPTH_STATS_VERBOSE = True
DEPTH_PRIORITY = 1

# Redirect settings
REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 3

# DNS timeout
DNS_TIMEOUT = 10

# Compression
COMPRESSION_ENABLED = True

# URL length limit
URLLENGTH_LIMIT = 2048

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
LOG_STDOUT = False
LOG_FILE = None  # Set to file path to enable file logging

# Stats
STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'

# Custom settings
OUTPUT_DIR = './data/crawled'
ALLOWED_LANGUAGES = None  # None = all languages, or list of language codes
MIN_LANGUAGE_CONFIDENCE = 0.5
EU_LANGUAGES_ONLY = True  # Only keep EU language pages

# Redis settings (for distributed crawling - optional)
REDIS_URL = 'redis://localhost:6379'
REDIS_PARAMS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'retry_on_timeout': True,
    'encoding': 'utf-8',
}

# Scrapy-Redis settings (uncomment to enable distributed crawling)
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# SCHEDULER_PERSIST = True
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

# Feed export settings (alternative to custom pipeline)
FEEDS = {
    # Uncomment to use built-in feed export instead of custom pipeline
    # 'data/crawled/%(name)s_%(time)s.jsonl': {
    #     'format': 'jsonlines',
    #     'encoding': 'utf8',
    #     'store_empty': False,
    #     'overwrite': False,
    # },
}
