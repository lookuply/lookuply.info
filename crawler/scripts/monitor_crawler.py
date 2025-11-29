#!/usr/bin/env python3
"""
Lookuply Crawler Monitor

Monitor crawl progress and statistics.
"""

import sys
import os
import argparse
import json
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lookuply_crawler.config import LANGUAGES
from lookuply_crawler.storage import FileStorage
from lookuply_crawler.utils import format_bytes, format_duration


def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def count_pages_in_jsonl(jsonl_file):
    """Count pages in a JSONL file."""
    if not os.path.exists(jsonl_file):
        return 0

    count = 0
    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    count += 1
    except Exception:
        pass
    return count


def monitor_jsonl(output_dir, watch=False, interval=5):
    """Monitor JSONL output files."""
    output_path = Path(output_dir)

    if not output_path.exists():
        print(f"Output directory not found: {output_dir}")
        return

    while True:
        if watch:
            clear_screen()

        print("=" * 70)
        print(f"LOOKUPLY CRAWLER MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()

        # Collect statistics
        total_pages = 0
        lang_stats = []

        for lang_code in LANGUAGES.keys():
            jsonl_file = output_path / f"{lang_code}.jsonl"
            page_count = count_pages_in_jsonl(jsonl_file)

            if page_count > 0:
                file_size = jsonl_file.stat().st_size if jsonl_file.exists() else 0
                lang_stats.append({
                    'code': lang_code,
                    'name': LANGUAGES[lang_code]['name'],
                    'pages': page_count,
                    'size': file_size
                })
                total_pages += page_count

        # Sort by page count
        lang_stats.sort(key=lambda x: x['pages'], reverse=True)

        # Display statistics
        print(f"Total Pages Crawled: {total_pages:,}")
        print()
        print(f"{'Lang':<6} {'Language':<20} {'Pages':<12} {'Size':<12}")
        print("-" * 70)

        for stat in lang_stats:
            print(f"{stat['code']:<6} {stat['name']:<20} {stat['pages']:<12,} {format_bytes(stat['size']):<12}")

        if not lang_stats:
            print("No data found yet. Crawler may still be starting...")

        print("=" * 70)

        if watch:
            print(f"\nRefreshing every {interval} seconds. Press Ctrl+C to stop.")
            try:
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\nMonitoring stopped.")
                break
        else:
            break


def monitor_storage(base_dir):
    """Monitor file storage."""
    storage = FileStorage(base_dir)
    stats = storage.get_stats()

    print("=" * 70)
    print("STORAGE STATISTICS")
    print("=" * 70)
    print()
    print(f"Total Pages: {stats['total_pages']:,}")
    print(f"Total Size: {format_bytes(stats['total_size_bytes'])}")
    print()
    print(f"{'Language':<20} {'Pages':<12} {'Size':<12}")
    print("-" * 70)

    for lang_code, lang_stats in sorted(stats['by_language'].items(), key=lambda x: x[1]['pages'], reverse=True):
        lang_name = LANGUAGES.get(lang_code, {}).get('name', lang_code)
        print(f"{lang_name:<20} {lang_stats['pages']:<12,} {format_bytes(lang_stats['size_bytes']):<12}")

    print("=" * 70)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Monitor Lookuply crawler progress')

    parser.add_argument(
        '--output-dir',
        type=str,
        help='Output directory to monitor',
        default='./data/crawled'
    )

    parser.add_argument(
        '--watch',
        action='store_true',
        help='Watch mode: continuously update statistics'
    )

    parser.add_argument(
        '--interval',
        type=int,
        help='Update interval in seconds (for watch mode)',
        default=5
    )

    parser.add_argument(
        '--storage',
        action='store_true',
        help='Monitor file storage instead of JSONL files'
    )

    args = parser.parse_args()

    try:
        if args.storage:
            monitor_storage(args.output_dir)
        else:
            monitor_jsonl(args.output_dir, args.watch, args.interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        return 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
