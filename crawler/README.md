# Lookuply Crawler

**Privacy-First Web Crawler for ALL 24 EU Languages**

A production-ready Scrapy-based web crawler that crawls and indexes content in all 24 official EU languages.

**Status:** ✅ **Week 7 Configuration Complete & Tested** (2025-11-29)
- All 24 languages configured ✓
- All tests passing (4/4) ✓
- Language detection accuracy: 100% ✓
- Ready for Week 7-8 testing & deployment

## 🌍 Features

- ✅ **All 24 EU Languages** - Bulgarian, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, German, Greek, Hungarian, Irish, Italian, Latvian, Lithuanian, Maltese, Polish, Portuguese, Romanian, Slovak, Slovenian, Spanish, Swedish
- ✅ **Multi-Language Support** - Automatic language detection using fastText
- ✅ **Distributed Crawling** - Redis-based URL queue for parallel crawling
- ✅ **Content Extraction** - HTML parsing, text extraction, metadata collection
- ✅ **robots.txt Compliance** - Respects website crawling policies
- ✅ **Politeness Policies** - 1-2 second delays between requests
- ✅ **Open Source** - GPL-3.0 License
- ✅ **Docker Ready** - Container configuration included

## 📊 Crawling Targets

**Total Target: 4M pages**

```
English:      1,000,000 pages (largest global audience)
German:         300,000 pages
French:         300,000 pages
Spanish:        200,000 pages
Italian:        200,000 pages
Polish:         200,000 pages
Dutch:          150,000 pages
Romanian:       100,000 pages
Portuguese:     100,000 pages
Czech:          100,000 pages
Hungarian:      100,000 pages
Swedish:        100,000 pages
... and 12 more languages (50k-30k each)
```

## 📚 Documentation

**Week 7 Setup Complete** - Review these documents:

- 📋 **[CONFIGURATION_REPORT.md](CONFIGURATION_REPORT.md)** - Detailed status report with all test results
- 🧪 **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - How to test and validate the crawler
- 📖 **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation for all modules
- 📑 **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Week 7 setup summary

**Latest Test Results:**
```
✓ Configuration Module    - All 24 languages configured
✓ Language Detector       - 100% accuracy (10/10 sample texts)
✓ Content Extractor       - All fields working correctly
✓ Spider Configuration    - All languages initialize properly

Total: 4/4 tests passed ✅
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Redis (for distributed crawling)
- Docker & Docker Compose (optional)

### Installation

```bash
# Navigate to crawler directory
cd /home/baskervil/websearch/crawler

# Install dependencies
pip install --break-system-packages -r requirements.txt

# Verify installation (runs 4 validation tests)
python test_crawler_config.py

# Expected: ✅ All tests passed! Crawler is ready for deployment.
```

### Run Crawler (After Tests Pass)

```bash
# Crawl English
python -m scrapy crawl web_spider -a language=en

# Crawl German
python -m scrapy crawl web_spider -a language=de

# Save to JSON
python -m scrapy crawl web_spider -a language=en -o output.json

# Debug mode
python -m scrapy crawl web_spider -a language=en -L DEBUG
```

### With Docker

```bash
# Start Redis + distributed crawlers
docker-compose up

# Monitor progress
docker-compose logs -f

# Stop services
docker-compose down
```

## 📁 Project Structure

```
crawler/
├── requirements.txt              # Python dependencies
├── config_languages.py           # Language configuration (24 languages)
├── language_detector.py          # Language detection module
├── content_extractor.py          # Content extraction logic
├── base_spider.py               # Base spider class
├── web_spider.py                # Main web crawler spider
├── items.py                     # Data models
├── settings.py                  # Scrapy settings
├── pipelines.py                 # Data processing pipelines
├── README.md                    # This file
└── docker/
    ├── Dockerfile               # Container definition
    └── docker-compose.yml       # Multi-service setup
```

## 🔧 Configuration

### Language Configuration

Edit `config_languages.py` to:
- Add new languages
- Modify start URLs
- Adjust pages per language
- Set domain filters

### Crawler Settings

Edit `settings.py` to:
- Configure Redis connection
- Adjust concurrent requests
- Modify download delays
- Set user agent
- Enable/disable middleware

## 📝 Usage

### Crawl Specific Language

```bash
python -m scrapy crawl web_spider -a language=de
```

### Crawl All Languages (Distributed)

```bash
# Start Redis
redis-server

# Run crawler services in Docker
docker-compose -f docker/docker-compose.yml up -d

# Monitor progress
python scripts/monitor_crawler.py
```

### Research Start URLs

```bash
python scripts/research_urls.py --language en
```

## 🎯 Content Extraction

The crawler extracts:
- **Text Content** - Main article/page text
- **Metadata** - Title, description, keywords
- **Links** - Internal and external links
- **Language** - Detected language code
- **URL** - Source URL
- **Timestamp** - Crawl date/time

## 🛡️ Compliance

- ✅ **robots.txt** - Fully compliant
- ✅ **Politeness** - 1-2 second delays
- ✅ **User-Agent** - Identifies as LookuplyBot
- ✅ **Privacy** - No user tracking
- ✅ **GDPR** - Respects data protection laws

## 📦 Storage

Crawled data stored as:
- **Format** - JSON/CSV
- **Location** - Local disk or S3-compatible storage
- **Compression** - Gzip compression for efficiency
- **Deduplication** - Automatic duplicate URL filtering

## 📊 Monitoring

Monitor crawler progress with:

```bash
# Real-time statistics
python scripts/monitor_crawler.py

# Prometheus metrics (if enabled)
# http://localhost:9090/metrics
```

## 🚨 Error Handling

Handles:
- Network timeouts
- Invalid HTML
- Non-UTF8 encodings
- Redirects (301, 302, etc.)
- Rate limiting (429 errors)
- Server errors (500, 503, etc.)

## 🐛 Troubleshooting

### Redis Connection Error
```bash
redis-cli ping
# Should respond: PONG
```

### Memory Issues
```bash
# Reduce concurrent requests in settings.py
CONCURRENT_REQUESTS = 16  # Default is 32
```

### Slow Crawling
```bash
# Check:
1. Network bandwidth
2. Redis performance
3. Target server rate limiting
4. Download delay settings
```

## 📚 Documentation

- `config_languages.py` - Language configuration reference
- `language_detector.py` - Language detection documentation
- `content_extractor.py` - Content extraction API
- `web_spider.py` - Spider documentation

## 🤝 Contributing

Contributions welcome! Please:
1. Follow PEP 8 style guide
2. Add tests for new features
3. Update documentation
4. Open pull request

## 📄 License

GPL-3.0 - See LICENSE file for details

## 🔗 Links

- **GitHub:** https://github.com/lookuply/crawler
- **Website:** https://lookuply.info
- **API Docs:** https://docs.lookuply.info

## 📧 Support

- **Email:** crawler@lookuply.info
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions

---

**Lookuply Crawler** - Powering Privacy-First Search in 24 Languages
