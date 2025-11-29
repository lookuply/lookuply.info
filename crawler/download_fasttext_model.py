#!/usr/bin/env python3
"""
Download fastText language identification model.
This is required for language detection in the crawler.
"""

import os
import sys
import urllib.request
from pathlib import Path

def download_model():
    """Download fastText language identification model"""

    # Model information
    model_url = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz"
    model_name = "lid.176.ftz"  # fastText uses .ftz format (compressed)

    # Default save location
    home = Path.home()
    fasttext_dir = home / '.fasttext'
    fasttext_dir.mkdir(exist_ok=True)

    model_path = fasttext_dir / model_name

    # Check if already downloaded
    if model_path.exists():
        print(f"✓ Model already exists: {model_path}")
        print(f"  Size: {model_path.stat().st_size / 1024 / 1024:.1f} MB")
        return True

    print(f"📥 Downloading fastText language detection model...")
    print(f"   URL: {model_url}")
    print(f"   Save to: {model_path}")
    print(f"   Size: ~155 MB")

    try:
        # Download with progress
        def download_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(downloaded * 100 / total_size, 100)
                mb_done = downloaded / 1024 / 1024
                mb_total = total_size / 1024 / 1024
                print(f"\r   Progress: {percent:.1f}% ({mb_done:.1f}/{mb_total:.1f} MB)", end='')

        urllib.request.urlretrieve(model_url, model_path, download_progress)
        print(f"\n✓ Model downloaded successfully!")
        print(f"  Size: {model_path.stat().st_size / 1024 / 1024:.1f} MB")
        return True

    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        return False

if __name__ == '__main__':
    success = download_model()
    sys.exit(0 if success else 1)
