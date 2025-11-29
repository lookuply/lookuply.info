"""
File Storage Module
Handle local file storage for crawled data.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class FileStorage:
    """
    Local file storage for crawled pages.
    Organizes files by language and date.
    """

    def __init__(self, base_dir='./data/crawled'):
        """
        Initialize file storage.

        Args:
            base_dir: Base directory for storage
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_page(self, page_data, language_code):
        """
        Save page data to file.

        Args:
            page_data: Dictionary containing page data
            language_code: Language code (e.g., 'en', 'de')

        Returns:
            str: Path to saved file
        """
        try:
            # Create language directory
            lang_dir = self.base_dir / language_code
            lang_dir.mkdir(exist_ok=True)

            # Get date for organization
            date_str = datetime.utcnow().strftime('%Y-%m-%d')
            date_dir = lang_dir / date_str
            date_dir.mkdir(exist_ok=True)

            # Generate filename from URL hash
            from ..utils import get_url_hash
            url_hash = get_url_hash(page_data['url'])
            filename = f"{url_hash}.json"
            filepath = date_dir / filename

            # Save as JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(page_data, f, ensure_ascii=False, indent=2)

            logger.debug(f"Saved page to {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Failed to save page {page_data.get('url')}: {e}")
            return None

    def save_batch(self, pages, language_code):
        """
        Save multiple pages at once.

        Args:
            pages: List of page data dictionaries
            language_code: Language code

        Returns:
            int: Number of pages saved successfully
        """
        saved_count = 0
        for page_data in pages:
            if self.save_page(page_data, language_code):
                saved_count += 1
        return saved_count

    def load_page(self, language_code, url_hash):
        """
        Load page data from file.

        Args:
            language_code: Language code
            url_hash: URL hash

        Returns:
            dict: Page data or None if not found
        """
        try:
            # Search for file with this hash
            lang_dir = self.base_dir / language_code

            if not lang_dir.exists():
                return None

            # Search in date directories
            for date_dir in lang_dir.iterdir():
                if date_dir.is_dir():
                    filepath = date_dir / f"{url_hash}.json"
                    if filepath.exists():
                        with open(filepath, 'r', encoding='utf-8') as f:
                            return json.load(f)

            return None

        except Exception as e:
            logger.error(f"Failed to load page {url_hash}: {e}")
            return None

    def get_stats(self):
        """
        Get storage statistics.

        Returns:
            dict: Statistics about stored pages
        """
        stats = {
            'total_pages': 0,
            'by_language': {},
            'total_size_bytes': 0,
        }

        try:
            for lang_dir in self.base_dir.iterdir():
                if lang_dir.is_dir():
                    lang_code = lang_dir.name
                    page_count = 0
                    lang_size = 0

                    # Count files in all date directories
                    for date_dir in lang_dir.iterdir():
                        if date_dir.is_dir():
                            for filepath in date_dir.glob('*.json'):
                                page_count += 1
                                lang_size += filepath.stat().st_size

                    stats['by_language'][lang_code] = {
                        'pages': page_count,
                        'size_bytes': lang_size,
                    }
                    stats['total_pages'] += page_count
                    stats['total_size_bytes'] += lang_size

        except Exception as e:
            logger.error(f"Failed to get storage stats: {e}")

        return stats

    def cleanup_old_files(self, days=30):
        """
        Clean up files older than specified days.

        Args:
            days: Number of days to keep

        Returns:
            int: Number of files deleted
        """
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted_count = 0

        try:
            for lang_dir in self.base_dir.iterdir():
                if lang_dir.is_dir():
                    for date_dir in lang_dir.iterdir():
                        if date_dir.is_dir():
                            # Check if directory is old
                            try:
                                dir_date = datetime.strptime(date_dir.name, '%Y-%m-%d')
                                if dir_date < cutoff_date:
                                    # Delete all files in this directory
                                    for filepath in date_dir.glob('*.json'):
                                        filepath.unlink()
                                        deleted_count += 1
                                    # Remove empty directory
                                    date_dir.rmdir()
                                    logger.info(f"Deleted old directory: {date_dir}")
                            except ValueError:
                                pass  # Skip directories with invalid date format

        except Exception as e:
            logger.error(f"Failed to cleanup old files: {e}")

        return deleted_count

    def export_to_jsonl(self, language_code, output_file):
        """
        Export all pages for a language to JSON Lines format.

        Args:
            language_code: Language code
            output_file: Output file path

        Returns:
            int: Number of pages exported
        """
        exported_count = 0

        try:
            lang_dir = self.base_dir / language_code

            if not lang_dir.exists():
                logger.warning(f"No data found for language: {language_code}")
                return 0

            with open(output_file, 'w', encoding='utf-8') as outfile:
                # Process all date directories
                for date_dir in sorted(lang_dir.iterdir()):
                    if date_dir.is_dir():
                        for filepath in sorted(date_dir.glob('*.json')):
                            try:
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    page_data = json.load(f)
                                    outfile.write(json.dumps(page_data, ensure_ascii=False) + '\n')
                                    exported_count += 1
                            except Exception as e:
                                logger.error(f"Failed to export {filepath}: {e}")

            logger.info(f"Exported {exported_count} pages to {output_file}")
            return exported_count

        except Exception as e:
            logger.error(f"Failed to export to JSONL: {e}")
            return 0
