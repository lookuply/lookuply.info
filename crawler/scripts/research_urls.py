#!/usr/bin/env python3
"""
URL Research Helper

Helper script to research and validate start URLs for each language.
"""

import sys
import os
import argparse
import requests
from urllib.parse import urlparse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lookuply_crawler.config import LANGUAGES, get_start_urls
from lookuply_crawler.extractors import get_detector


def check_url(url, timeout=10):
    """
    Check if URL is accessible.

    Args:
        url: URL to check
        timeout: Request timeout

    Returns:
        dict: Status information
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; LookuplyBot/1.0; +https://lookuply.info)'
        }
        response = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)

        return {
            'url': url,
            'status': response.status_code,
            'accessible': response.status_code == 200,
            'final_url': response.url,
            'redirected': response.url != url,
        }
    except Exception as e:
        return {
            'url': url,
            'status': None,
            'accessible': False,
            'error': str(e),
        }


def detect_url_language(url, timeout=10):
    """
    Detect language of a URL.

    Args:
        url: URL to check
        timeout: Request timeout

    Returns:
        dict: Language detection result
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; LookuplyBot/1.0; +https://lookuply.info)'
        }
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)

        if response.status_code == 200:
            detector = get_detector()
            lang_code, confidence = detector.detect_from_html(response.text)

            return {
                'url': url,
                'detected_language': lang_code,
                'confidence': confidence,
                'success': True,
            }
        else:
            return {
                'url': url,
                'success': False,
                'error': f'HTTP {response.status_code}',
            }
    except Exception as e:
        return {
            'url': url,
            'success': False,
            'error': str(e),
        }


def validate_start_urls(language_code=None):
    """
    Validate start URLs for language(s).

    Args:
        language_code: Specific language code or None for all
    """
    languages_to_check = [language_code] if language_code else LANGUAGES.keys()

    print("=" * 70)
    print("START URL VALIDATION")
    print("=" * 70)
    print()

    for lang_code in languages_to_check:
        lang_name = LANGUAGES[lang_code]['name']
        urls = get_start_urls(lang_code)

        print(f"\n{lang_code.upper()} - {lang_name}")
        print("-" * 70)

        if not urls:
            print("  No start URLs configured!")
            continue

        for url in urls:
            result = check_url(url)

            status_icon = "✓" if result['accessible'] else "✗"
            status_text = f"HTTP {result['status']}" if result['status'] else "ERROR"

            print(f"  {status_icon} {url}")
            print(f"     Status: {status_text}")

            if result.get('redirected'):
                print(f"     Redirected to: {result['final_url']}")

            if result.get('error'):
                print(f"     Error: {result['error']}")

    print("\n" + "=" * 70)


def research_urls(language_code):
    """
    Research and suggest URLs for a language.

    Args:
        language_code: Language code
    """
    if language_code not in LANGUAGES:
        print(f"Error: Invalid language code '{language_code}'")
        return

    lang_info = LANGUAGES[language_code]
    print("=" * 70)
    print(f"URL RESEARCH FOR {language_code.upper()} - {lang_info['name']}")
    print("=" * 70)
    print()

    # Suggest common patterns
    suggestions = [
        f"https://{language_code}.wikipedia.org/",
        f"https://www.google.{language_code}/",
    ]

    print("Suggested URL patterns to research:")
    for suggestion in suggestions:
        print(f"  - {suggestion}")

    print("\nCommon sources to research:")
    print("  - Wikipedia editions")
    print("  - Major news websites")
    print("  - Government websites (.gov domains)")
    print("  - Popular blogs and forums")
    print("  - Educational institutions")

    print("\nTips:")
    print("  - Look for high-quality, frequently updated content")
    print("  - Prefer websites with good internal linking")
    print("  - Avoid paywalled or login-required content")
    print("  - Check robots.txt compliance")

    print("\n" + "=" * 70)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Research and validate start URLs')

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate existing start URLs'
    )

    parser.add_argument(
        '--research',
        type=str,
        help='Research URLs for a specific language code'
    )

    parser.add_argument(
        '--language',
        type=str,
        help='Language code to validate (default: all)'
    )

    parser.add_argument(
        '--detect',
        type=str,
        help='Detect language of a specific URL'
    )

    args = parser.parse_args()

    if args.validate:
        validate_start_urls(args.language)
    elif args.research:
        research_urls(args.research)
    elif args.detect:
        print(f"Detecting language for: {args.detect}")
        result = detect_url_language(args.detect)
        if result['success']:
            print(f"Detected language: {result['detected_language']} (confidence: {result['confidence']:.2f})")
        else:
            print(f"Error: {result['error']}")
    else:
        parser.print_help()

    return 0


if __name__ == '__main__':
    sys.exit(main())
