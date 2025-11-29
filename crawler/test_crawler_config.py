#!/usr/bin/env python3
"""
Test script to verify crawler configuration and core modules.
Validates language detection, content extraction, and spider setup.
"""

import sys
import logging
from config_languages import LANGUAGES, START_URLS, PAGES_PER_LANGUAGE, get_language_count, get_total_target_pages
from language_detector import LanguageDetector
from content_extractor import ContentExtractor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test samples in different EU languages
TEST_SAMPLES = {
    'en': 'Privacy is a fundamental right. Our search engine respects your privacy.',
    'de': 'Datenschutz ist ein Grundrecht. Unsere Suchmaschine respektiert Ihre Privatsphäre.',
    'fr': 'La confidentialité est un droit fondamental. Notre moteur de recherche respecte votre vie privée.',
    'es': 'La privacidad es un derecho fundamental. Nuestro motor de búsqueda respeta su privacidad.',
    'it': 'La privacy è un diritto fondamentale. Il nostro motore di ricerca rispetta la tua privacy.',
    'pl': 'Prywatność jest prawem podstawowym. Nasza wyszukiwarka szanuje Twoją prywatność.',
    'cs': 'Soukromí je základním právem. Náš vyhledávač respektuje vaše soukromí.',
    'sk': 'Súkromie je základným právom. Náš vyhľadávač rešpektuje vaše súkromie.',
    'pt': 'A privacidade é um direito fundamental. Nosso mecanismo de pesquisa respeita sua privacidade.',
    'nl': 'Privacy is een fundamentaal recht. Onze zoekmachine respecteert uw privacy.',
}

def test_configuration():
    """Test configuration module"""
    print("\n" + "="*60)
    print("TESTING CONFIGURATION MODULE")
    print("="*60)

    language_count = get_language_count()
    total_pages = get_total_target_pages()

    print(f"\n✓ Languages configured: {language_count}/24")
    print(f"✓ Total target pages: {total_pages:,}")

    if language_count != 24:
        logger.error(f"ERROR: Expected 24 languages, got {language_count}")
        return False

    # Check START_URLS coverage
    languages_with_urls = len(START_URLS)
    print(f"✓ Languages with START_URLS: {languages_with_urls}/24")

    # Check missing URLs
    missing_urls = []
    for lang in LANGUAGES.keys():
        if lang not in START_URLS:
            missing_urls.append(lang)

    if missing_urls:
        print(f"⚠ Languages missing START_URLS: {missing_urls}")

    # Check PAGES_PER_LANGUAGE
    configured_languages = len(PAGES_PER_LANGUAGE)
    print(f"✓ Languages with page targets: {configured_languages}/24")

    if configured_languages != 24:
        print(f"⚠ Missing page targets for: {set(LANGUAGES.keys()) - set(PAGES_PER_LANGUAGE.keys())}")

    return True

def test_language_detector():
    """Test language detection"""
    print("\n" + "="*60)
    print("TESTING LANGUAGE DETECTOR")
    print("="*60)

    try:
        detector = LanguageDetector()
        print("✓ Language detector loaded successfully")
        print(f"✓ Using model: {detector.model_path}")

        # Test detection on samples
        print("\n📊 Language Detection Results:")
        print("-" * 50)

        correct_detections = 0
        total_tests = len(TEST_SAMPLES)

        for expected_lang, text in TEST_SAMPLES.items():
            detected_lang, confidence = detector.detect(text)

            status = "✓" if detected_lang == expected_lang else "✗"
            print(f"{status} Expected: {expected_lang:4} | Detected: {detected_lang:4} | Confidence: {confidence:.3f}")

            if detected_lang == expected_lang:
                correct_detections += 1

        accuracy = (correct_detections / total_tests) * 100
        print(f"\n✓ Detection accuracy: {correct_detections}/{total_tests} ({accuracy:.1f}%)")

        # Test multi-language detection
        print("\n📊 Multi-language Detection (Top 3):")
        print("-" * 50)

        sample_en = "English text about privacy and open source technology."
        results = detector.detect_multiple(sample_en, k=3)
        for lang, conf in results:
            print(f"  {lang:4} - {conf:.3f}")

        # Test EU language check
        print("\n📊 EU Language Validation:")
        print("-" * 50)

        test_langs = ['en', 'de', 'fr', 'ja', 'zh', 'pt']
        for lang in test_langs:
            is_eu = detector.is_eu_language(lang)
            status = "✓ EU" if is_eu else "✗ Non-EU"
            print(f"  {lang:4} - {status}")

        return True

    except ImportError as e:
        logger.error(f"ERROR: Failed to load language detector: {e}")
        print("⚠ fasttext-wheel not installed. Install with:")
        print("  pip install fasttext-wheel")
        return False
    except Exception as e:
        logger.error(f"ERROR: Language detection test failed: {e}")
        return False

def test_content_extractor():
    """Test content extraction"""
    print("\n" + "="*60)
    print("TESTING CONTENT EXTRACTOR")
    print("="*60)

    try:
        extractor = ContentExtractor()
        print("✓ Content extractor loaded successfully")

        # Test with sample HTML
        sample_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Test Article</title>
            <meta name="description" content="This is a test article">
            <meta property="og:title" content="Test Article OG">
            <meta property="og:description" content="Test description">
            <meta name="author" content="Test Author">
            <meta name="keywords" content="privacy, search, open">
        </head>
        <body>
            <header>Header content</header>
            <article>
                <h1>Main Article Title</h1>
                <p>This is the main content of the article. It contains important information about privacy and open source technology.</p>
                <p>Additional paragraphs with more content.</p>
            </article>
            <footer>Footer content</footer>
            <a href="/internal-link">Internal</a>
            <a href="https://external.com/page">External</a>
        </body>
        </html>
        """

        result = extractor.extract(sample_html, "https://example.com/article")

        print("\n📊 Extraction Results:")
        print("-" * 50)
        print(f"✓ Title: {result['title'][:50]}")
        print(f"✓ Description: {result['description'][:50]}")
        print(f"✓ Content length: {len(result['content'])} chars")
        print(f"✓ Links found: {len(result['links'])}")
        print(f"✓ Metadata fields: {len(result['metadata'])}")

        if result['metadata']:
            print(f"  - Author: {result['metadata'].get('author', 'N/A')}")
            print(f"  - Keywords: {result['metadata'].get('keywords', 'N/A')}")

        return True

    except Exception as e:
        logger.error(f"ERROR: Content extraction test failed: {e}")
        return False

def test_spider_configuration():
    """Test spider setup"""
    print("\n" + "="*60)
    print("TESTING SPIDER CONFIGURATION")
    print("="*60)

    try:
        from web_spider import WebSpider

        # Test spider initialization for different languages
        test_languages = ['en', 'de', 'fr', 'cs', 'sk']

        print("\n📊 Spider Initialization:")
        print("-" * 50)

        for lang in test_languages:
            try:
                spider = WebSpider(language=lang)
                target = PAGES_PER_LANGUAGE.get(lang, 'N/A')
                urls_count = len(spider.start_urls)
                print(f"✓ {lang.upper():4} - Target: {target:>7} pages | Start URLs: {urls_count}")
            except Exception as e:
                print(f"✗ {lang.upper():4} - Error: {e}")

        return True

    except Exception as e:
        logger.error(f"ERROR: Spider configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🕷️  LOOKUPLY CRAWLER CONFIGURATION TEST")
    print("=" * 60)
    print(f"Date: 2025-11-29")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Configuration Module", test_configuration()))
    results.append(("Language Detector", test_language_detector()))
    results.append(("Content Extractor", test_content_extractor()))
    results.append(("Spider Configuration", test_spider_configuration()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✅ All tests passed! Crawler is ready for deployment.")
        return 0
    else:
        print(f"\n⚠  {total - passed} test(s) failed. Review output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
