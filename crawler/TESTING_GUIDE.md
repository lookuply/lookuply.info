# Lookuply Crawler - Testing Guide

Quick reference for testing the configured crawler before full deployment.

---

## Quick Start (5 minutes)

### 1. Verify Installation

```bash
cd /home/baskervil/websearch/crawler

# Check Python version
python --version  # Should be 3.9+

# Verify dependencies
pip list | grep -E "scrapy|fasttext|beautifulsoup"
```

### 2. Run Configuration Tests

```bash
# Test all components (5 minutes)
python test_crawler_config.py

# Expected output:
# ✅ All tests passed! Crawler is ready for deployment.
```

### 3. Quick Language Detection Test

```bash
python -c "
from language_detector import LanguageDetector
detector = LanguageDetector()
text = 'Hello, this is a test of the language detection system.'
lang, conf = detector.detect(text)
print(f'Language: {lang} | Confidence: {conf:.3f}')
"
```

---

## Single Language Testing

### Test English Crawler (10-20 pages)

```bash
# Modify config to test small number of pages
# Edit config_languages.py and temporarily set:
# PAGES_PER_LANGUAGE['en'] = 20

# Run spider
python -m scrapy crawl web_spider -a language=en

# Monitor output for:
# - Language detection
# - Content extraction
# - Page count
# - Errors/warnings
```

### Test German Crawler

```bash
python -m scrapy crawl web_spider -a language=de
```

### Test French Crawler

```bash
python -m scrapy crawl web_spider -a language=fr
```

---

## Multi-Language Testing (Docker)

### Start Services

```bash
# Terminal 1: Start services
docker-compose up

# Terminal 2: Monitor logs
docker-compose logs -f
```

### Scale to Multiple Crawlers

```bash
# Scale crawler service (example: 3 instances)
docker-compose up --scale crawler-en=1 --scale crawler-de=1 --scale crawler-fr=1
```

### Stop Services

```bash
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Data Collection & Validation

### Check Output Format

```bash
# After crawler runs, check output
ls -la data/

# If using JSON format
cat data/en_crawl.json | head -10

# Count pages crawled
grep -c '"url"' data/en_crawl.json
```

### Verify Data Quality

Expected fields in output:
```json
{
  "url": "https://...",
  "title": "Page Title",
  "description": "Meta description",
  "content": "Main text content...",
  "language": "en",
  "detected_language": "en",
  "language_confidence": 0.98,
  "links": ["https://...", "https://..."],
  "metadata": {
    "author": "...",
    "keywords": "...",
    "published": "2025-01-01"
  },
  "status_code": 200
}
```

---

## Performance Testing

### Measure Crawling Speed

```bash
# Start crawler and monitor
time python -m scrapy crawl web_spider -a language=en

# Record:
# - Time taken
# - Pages crawled
# - Pages per minute
```

### Monitor Resource Usage

```bash
# In separate terminal
watch -n 1 'ps aux | grep scrapy'

# Check:
# - CPU usage
# - Memory usage
# - Process count
```

---

## Language Detection Accuracy

### Test on Real Content

```python
from language_detector import LanguageDetector
from content_extractor import ContentExtractor
import requests

detector = LanguageDetector()
extractor = ContentExtractor()

# Test URLs per language
test_urls = {
    'en': 'https://en.wikipedia.org/wiki/Python_(programming_language)',
    'de': 'https://de.wikipedia.org/wiki/Programmiersprache',
    'fr': 'https://fr.wikipedia.org/wiki/Langage_de_programmation',
}

for expected_lang, url in test_urls.items():
    try:
        response = requests.get(url, timeout=10)
        extracted = extractor.extract(response.text, url)

        sample = extracted['content'][:500]
        detected_lang, confidence = detector.detect(sample)

        status = "✓" if detected_lang == expected_lang else "✗"
        print(f"{status} {expected_lang}: detected {detected_lang} ({confidence:.3f})")
    except Exception as e:
        print(f"Error testing {expected_lang}: {e}")
```

---

## Troubleshooting

### Language Detector Error: "Model not found"

```bash
# Download model manually
python download_fasttext_model.py

# Verify download
ls -lh ~/.fasttext/lid.176.ftz
```

### Spider Won't Start

```bash
# Check Scrapy installation
python -m scrapy version

# Check spider configuration
python -c "from web_spider import WebSpider; spider = WebSpider(language='en'); print(f'URLs: {len(spider.start_urls)}')"
```

### Redis Connection Error (if using Docker)

```bash
# Check Redis is running
docker ps | grep redis

# Restart services
docker-compose restart redis

# Test connection
redis-cli ping  # Should return PONG
```

### Memory Issues

```bash
# Reduce concurrent requests
# Edit web_spider.py and change:
# CONCURRENT_REQUESTS = 16  (from 32)

# Or limit output:
# In web_spider.py parse_page() method
# Add: if self.pages_crawled > 100: return
```

---

## Testing Checklist

Before full deployment, verify:

- [ ] Configuration tests pass (4/4)
- [ ] Language detector works on real content
- [ ] Content extractor extracts expected fields
- [ ] Single language crawl completes (10+ pages)
- [ ] Multi-language crawl works (Docker)
- [ ] Output format is consistent
- [ ] No critical errors in logs
- [ ] Performance is acceptable (>10 pages/minute)
- [ ] Language detection accuracy is high (>90%)
- [ ] Links are properly extracted
- [ ] Metadata is captured

---

## Common Test Commands

```bash
# Run all configuration tests
python test_crawler_config.py

# Test specific language
python -m scrapy crawl web_spider -a language=en

# List all spiders
python -m scrapy list

# Check spider help
python -m scrapy crawl web_spider --help

# Run with debug logging
python -m scrapy crawl web_spider -a language=en -L DEBUG

# Save output to file
python -m scrapy crawl web_spider -a language=en -o output.json

# Limit crawling to N pages
# (Modify PAGES_PER_LANGUAGE temporarily in config_languages.py)
```

---

## Next: Full Crawl

Once testing validates everything:

1. **Scale to all 24 languages** via Docker
2. **Monitor progress** with Redis queue
3. **Store data** in persistent storage
4. **Proceed to Week 8** search engine setup

---

**Location:** `/home/baskervil/websearch/crawler/`
**Reference:** `CONFIGURATION_REPORT.md`
