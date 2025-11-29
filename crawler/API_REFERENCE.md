# Lookuply Crawler - API Reference

Complete API documentation for all crawler modules.

---

## Table of Contents

1. [Configuration Module](#configuration-module)
2. [Language Detector](#language-detector)
3. [Content Extractor](#content-extractor)
4. [Web Spider](#web-spider)
5. [Multi-Language Crawler](#multi-language-crawler)

---

## Configuration Module

**File:** `config_languages.py`

### Dictionary: LANGUAGES

```python
LANGUAGES = {
    'en': {
        'name': 'English',
        'native': 'English',
        'country': '🇬🇧'
    },
    'de': {
        'name': 'German',
        'native': 'Deutsch',
        'country': '🇩🇪'
    },
    # ... (24 total languages)
}
```

**Access:**
```python
from config_languages import LANGUAGES

# Get all languages
all_langs = LANGUAGES.keys()  # dict_keys(['en', 'de', ...])

# Get specific language info
en_info = LANGUAGES['en']  # {'name': 'English', ...}
native_name = LANGUAGES['de']['native']  # 'Deutsch'
```

---

### Dictionary: START_URLS

URLs to begin crawling for each language.

```python
START_URLS = {
    'en': [
        'https://en.wikipedia.org/wiki/Portal:Contents',
        'https://news.ycombinator.com/',
        # ... (typically 4-5 URLs per language)
    ],
    # ... (24 languages)
}
```

**Access:**
```python
from config_languages import START_URLS

# Get start URLs for English
en_urls = START_URLS['en']  # List of URLs

# Get URL count per language
de_count = len(START_URLS['de'])
```

---

### Dictionary: PAGES_PER_LANGUAGE

Target number of pages to crawl per language.

```python
PAGES_PER_LANGUAGE = {
    'en': 1000000,
    'de': 300000,
    'fr': 300000,
    # ... (24 languages totaling 3.24M pages)
}
```

**Access:**
```python
from config_languages import PAGES_PER_LANGUAGE

# Get target for English
en_target = PAGES_PER_LANGUAGE['en']  # 1000000

# Sum all targets
total = sum(PAGES_PER_LANGUAGE.values())  # 3240000
```

---

### Function: get_language_count()

Returns total number of configured languages.

```python
from config_languages import get_language_count

count = get_language_count()  # 24
```

---

### Function: get_total_target_pages()

Returns total pages target across all languages.

```python
from config_languages import get_total_target_pages

total = get_total_target_pages()  # 3240000
```

---

## Language Detector

**File:** `language_detector.py`

### Class: LanguageDetector

Detects language of text using fastText language identification model.

#### Constructor

```python
from language_detector import LanguageDetector

# Initialize with auto-download
detector = LanguageDetector()

# Initialize with custom model path
detector = LanguageDetector(model_path='/path/to/model.ftz')
```

**Parameters:**
- `model_path` (str, optional): Path to fastText model file. If not provided, auto-downloads to `~/.fasttext/lid.176.ftz`

**Raises:**
- `ImportError`: If fasttext-wheel not installed
- `Exception`: If model fails to load

---

#### Method: detect()

Detect primary language of text.

```python
text = "Hello, this is an English text."
lang_code, confidence = detector.detect(text)

print(f"Language: {lang_code}")      # 'en'
print(f"Confidence: {confidence}")   # 0.995
```

**Parameters:**
- `text` (str): Text to detect language for
- `k` (int, optional): Number of top predictions (default: 1)

**Returns:**
- `tuple`: (language_code, confidence_score)
  - language_code (str): ISO 639-1 code ('en', 'de', 'fr', etc.)
  - confidence_score (float): 0.0-1.0 confidence value

**Returns:** `('unknown', 0.0)` if text is empty or too short

**Example:**
```python
lang, conf = detector.detect("Bonjour, comment allez-vous?")
# Returns: ('fr', 0.987)
```

---

#### Method: detect_with_confidence()

Detect language only if confidence meets threshold.

```python
text = "Hello, world."
lang = detector.detect_with_confidence(text, min_confidence=0.9)

if lang:
    print(f"Detected: {lang}")  # 'en'
else:
    print("Confidence too low")  # None if < 0.9
```

**Parameters:**
- `text` (str): Text to detect
- `min_confidence` (float): Minimum confidence threshold (0.0-1.0, default: 0.8)

**Returns:**
- `str | None`: Language code if confidence >= threshold, else None

---

#### Method: detect_multiple()

Get top K language predictions.

```python
text = "Some ambiguous text..."
results = detector.detect_multiple(text, k=3)

for lang_code, confidence in results:
    print(f"{lang_code}: {confidence:.3f}")
```

**Parameters:**
- `text` (str): Text to analyze
- `k` (int): Number of top predictions to return (default: 3)

**Returns:**
- `list`: [(language_code, confidence), ...] sorted by confidence (descending)

**Example:**
```python
results = detector.detect_multiple("Hello world", k=3)
# Returns: [('en', 0.995), ('de', 0.012), ('fr', 0.008)]
```

---

#### Method: is_eu_language()

Check if language is one of 24 EU official languages.

```python
if detector.is_eu_language('en'):
    print("English is an EU language")

if detector.is_eu_language('ja'):
    print("Japanese is NOT an EU language")
```

**Parameters:**
- `lang_code` (str): ISO 639-1 language code

**Returns:**
- `bool`: True if EU language, False otherwise

**EU Languages:**
Bulgarian, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, German, Greek, Hungarian, Irish, Italian, Latvian, Lithuanian, Maltese, Polish, Portuguese, Romanian, Slovak, Slovenian, Spanish, Swedish

---

## Content Extractor

**File:** `content_extractor.py`

### Class: ContentExtractor

Extracts meaningful content from HTML pages.

#### Constructor

```python
from content_extractor import ContentExtractor

extractor = ContentExtractor()
```

**No parameters required.**

---

#### Method: extract()

Extract all content from HTML page.

```python
html = """
<html>
<head>
    <title>Example Page</title>
    <meta name="description" content="This is an example">
</head>
<body>
    <article>
        <h1>Main Title</h1>
        <p>Content here...</p>
    </article>
</body>
</html>
"""

result = extractor.extract(html, 'https://example.com/page')
```

**Parameters:**
- `html` (str): Raw HTML content
- `url` (str): Page URL (for resolving relative links)

**Returns:** `dict` with keys:

```python
{
    'title': 'Page Title',                           # str
    'description': 'Meta description',               # str
    'content': 'Main text content...',              # str (max 50KB)
    'links': [                                       # list[str] (max 100)
        'https://example.com/page1',
        'https://example.com/page2',
    ],
    'language_hints': ['en', 'fr'],                 # list[str]
    'metadata': {                                    # dict
        'author': 'John Doe',
        'keywords': 'example, test',
        'published': '2025-01-01',
        'image': 'https://example.com/image.jpg'
    }
}
```

**Example:**
```python
import requests
from content_extractor import ContentExtractor

response = requests.get('https://example.com')
extractor = ContentExtractor()
result = extractor.extract(response.text, response.url)

print(f"Title: {result['title']}")
print(f"Content length: {len(result['content'])}")
print(f"Links found: {len(result['links'])}")
```

---

### Content Extraction Rules

**Title Sources** (in order of priority):
1. `<title>` tag content
2. `og:title` meta property
3. `<h1>` tag content

**Description Sources:**
1. `<meta name="description">` tag
2. `<meta property="og:description">` tag

**Content Extraction:**
- Removes boilerplate (script, style, nav, footer, header, iframe, form)
- Looks for semantic content areas (article, main, post-content, content)
- Falls back to body content if no semantic area found
- Max 50KB per page

**Links:**
- Converts relative URLs to absolute
- Filters junk URLs (ads, analytics, tracking)
- Max 100 links per page

**Metadata:**
- Author (from `author` meta tag)
- Keywords (from `keywords` meta tag)
- Published date (from `article:published_time` meta property)
- Image (from `og:image` meta property)

---

## Web Spider

**File:** `web_spider.py`

### Class: WebSpider

Main Scrapy spider for crawling websites.

#### Constructor

```python
from web_spider import WebSpider

# Create spider for English
spider = WebSpider(language='en')

# Create spider for German
spider = WebSpider(language='de')
```

**Parameters:**
- `language` (str): Language code ('en', 'de', 'fr', etc., default: 'en')

**Attributes:**
```python
spider.language            # Language code
spider.pages_crawled       # Pages processed so far
spider.pages_target        # Target pages from config
spider.start_urls          # List of seed URLs
spider.allowed_domains     # List of allowed domains
spider.language_detector   # LanguageDetector instance
spider.content_extractor   # ContentExtractor instance
```

---

#### Spider Settings

```python
custom_settings = {
    'ROBOTSTXT_OBEY': True,           # Respect robots.txt
    'CONCURRENT_REQUESTS': 32,         # Parallel requests
    'DOWNLOAD_DELAY': 1.5,             # Delay between requests (seconds)
    'USER_AGENT': 'Mozilla/5.0 (compatible; LookuplyBot/1.0; +https://lookuply.info)',
    'COOKIES_ENABLED': False,
    'TELNETCONSOLE_ENABLED': False,
}
```

---

#### Method: parse_page()

Process crawled page and extract data.

```python
# Automatically called by Scrapy for each response
# Yields extracted page data

# Typical output:
{
    'url': 'https://example.com/article',
    'title': 'Article Title',
    'description': 'Meta description',
    'content': 'Main content...',
    'language': 'en',
    'detected_language': 'en',
    'language_confidence': 0.98,
    'links': ['https://...', 'https://...'],
    'metadata': {
        'author': '...',
        'keywords': '...',
        'published': '2025-01-01',
        'image': '...'
    },
    'crawl_time': 'Wed, 29 Nov 2025 10:00:00 GMT',
    'status_code': 200
}
```

---

#### Method: errback()

Handle request errors.

```python
# Automatically handles failed requests
# Logs warnings for network errors, timeouts, etc.
```

---

### Running the Spider

```bash
# Crawl English
python -m scrapy crawl web_spider -a language=en

# Crawl German
python -m scrapy crawl web_spider -a language=de

# Save output to JSON
python -m scrapy crawl web_spider -a language=en -o output.json

# Save output to CSV
python -m scrapy crawl web_spider -a language=en -o output.csv

# Verbose logging
python -m scrapy crawl web_spider -a language=en -L DEBUG
```

---

## Multi-Language Crawler

**File:** `web_spider.py`

### Class: MultiLanguageCrawler

Controller for parallel multi-language crawling.

#### Constructor

```python
from web_spider import MultiLanguageCrawler

crawler = MultiLanguageCrawler()
```

**No parameters required. Automatically discovers all 24 languages.**

#### Attributes

```python
crawler.languages  # List of all configured language codes
```

---

#### Method: get_spider_for_language()

Get spider instance for specific language.

```python
spider = crawler.get_spider_for_language('en')
# Returns: WebSpider(language='en')
```

**Parameters:**
- `language` (str): Language code

**Returns:**
- `WebSpider`: Spider instance for that language

---

#### Method: crawl_all()

Start crawling all 24 languages in parallel.

```python
crawler = MultiLanguageCrawler()
crawler.crawl_all()  # Blocks until all crawling completes
```

**Note:** This uses Scrapy's CrawlerProcess and will block execution. For distributed crawling, use Docker Compose instead.

---

## Docker Usage

### Docker Compose

```bash
# Start all services (Redis + crawlers)
docker-compose up

# Run specific service
docker-compose up redis
docker-compose up crawler-en

# Run in background
docker-compose up -d

# Monitor logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f crawler-en

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Scale Crawlers

```bash
# Create multiple instances of same crawler
docker-compose up --scale crawler-en=3

# Different approach: modify docker-compose.yml
# Add multiple services: crawler-en1, crawler-en2, crawler-en3
```

---

## Common Patterns

### Pattern 1: Detect Language and Extract Content

```python
from language_detector import LanguageDetector
from content_extractor import ContentExtractor
import requests

detector = LanguageDetector()
extractor = ContentExtractor()

response = requests.get('https://example.com')

# Detect language
sample = response.text[:500]
lang, confidence = detector.detect(sample)
print(f"Language: {lang} ({confidence:.3f})")

# Extract content
result = extractor.extract(response.text, response.url)
print(f"Title: {result['title']}")
print(f"Content: {result['content'][:100]}...")
```

### Pattern 2: Batch Process Multiple URLs

```python
from language_detector import LanguageDetector
from content_extractor import ContentExtractor
import requests

detector = LanguageDetector()
extractor = ContentExtractor()

urls = [
    'https://example.com/1',
    'https://example.com/2',
    'https://example.com/3',
]

results = []
for url in urls:
    try:
        response = requests.get(url, timeout=10)
        extracted = extractor.extract(response.text, url)

        sample = extracted['content'][:500]
        lang, conf = detector.detect(sample)

        results.append({
            'url': url,
            'language': lang,
            'confidence': conf,
            'title': extracted['title'],
        })
    except Exception as e:
        print(f"Error: {url} - {e}")

print(results)
```

### Pattern 3: Filter by Language

```python
from language_detector import LanguageDetector

detector = LanguageDetector()

pages = [...]  # List of extracted content

# Filter only English pages
english_pages = []
for page in pages:
    lang, conf = detector.detect(page['content'])
    if lang == 'en' and conf > 0.9:
        english_pages.append(page)

print(f"Found {len(english_pages)} English pages")
```

---

## Error Handling

### Handle Missing Content

```python
from content_extractor import ContentExtractor

extractor = ContentExtractor()
result = extractor.extract(html, url)

if not result['content']:
    print("No content extracted")

if not result['title']:
    print("No title found")
```

### Handle Language Detection Failure

```python
from language_detector import LanguageDetector

detector = LanguageDetector()
lang, conf = detector.detect(text)

if lang == 'unknown':
    print("Could not detect language")
    # Use fallback or skip page

if conf < 0.7:
    print("Low confidence detection")
    # Verify with other method or skip
```

### Handle Extraction Timeout

```python
from content_extractor import ContentExtractor
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Extraction took too long")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)  # 5 second timeout

try:
    result = extractor.extract(html, url)
finally:
    signal.alarm(0)  # Cancel timeout
```

---

## Performance Tips

1. **Use multi-prediction for ambiguous content:**
   ```python
   results = detector.detect_multiple(text, k=5)
   # Analyze top predictions
   ```

2. **Limit text for faster detection:**
   ```python
   lang, conf = detector.detect(text[:500])
   # First 500 chars usually sufficient
   ```

3. **Cache language detection results:**
   ```python
   cache = {}
   def get_language(text):
       key = hash(text)
       if key not in cache:
           lang, conf = detector.detect(text)
           cache[key] = lang
       return cache[key]
   ```

4. **Batch extract multiple pages:**
   ```python
   pages = [...]
   for page in pages:
       result = extractor.extract(page['html'], page['url'])
       # Process result
   ```

---

## Version Information

- **Python:** 3.9+
- **Scrapy:** 2.11.2
- **fastText:** 0.9.2+
- **BeautifulSoup4:** 4.12.2+
- **Redis:** 5.0.1+ (optional, for distributed crawling)

---

**Last Updated:** 2025-11-29
**Reference:** `CONFIGURATION_REPORT.md`, `TESTING_GUIDE.md`
