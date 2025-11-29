"""
Language Detection Module
Uses fastText for accurate language detection of web content.
"""

import os
import logging
from typing import Optional, Tuple, List
import tempfile
import urllib.request

logger = logging.getLogger(__name__)


class LanguageDetector:
    """
    Language detector using fastText.
    Supports all 24 EU languages.
    """

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize language detector.

        Args:
            model_path: Path to fastText language model. If None, downloads automatically.
        """
        self.model = None
        self.model_path = model_path or self._get_default_model_path()
        self._load_model()

    def _get_default_model_path(self) -> str:
        """Get or download the default fastText language model."""
        model_dir = os.path.join(tempfile.gettempdir(), 'lookuply_models')
        os.makedirs(model_dir, exist_ok=True)

        model_path = os.path.join(model_dir, 'lid.176.bin')

        if not os.path.exists(model_path):
            logger.info("Downloading fastText language identification model...")
            try:
                url = 'https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin'
                urllib.request.urlretrieve(url, model_path)
                logger.info(f"Model downloaded to {model_path}")
            except Exception as e:
                logger.error(f"Failed to download model: {e}")
                raise

        return model_path

    def _load_model(self):
        """Load the fastText model."""
        try:
            import fasttext
            # Suppress fastText warnings
            fasttext.FastText.eprint = lambda x: None
            self.model = fasttext.load_model(self.model_path)
            logger.info("Language detection model loaded successfully")
        except ImportError:
            logger.error("fasttext-wheel not installed. Run: pip install fasttext-wheel")
            raise
        except Exception as e:
            logger.error(f"Failed to load language model: {e}")
            raise

    def detect(self, text: str, k: int = 1) -> Tuple[str, float]:
        """
        Detect the language of given text.

        Args:
            text: Text to detect language for
            k: Number of top predictions to return

        Returns:
            Tuple of (language_code, confidence_score)
        """
        if not text or not text.strip():
            return ('unknown', 0.0)

        try:
            # Clean text - remove extra whitespace
            text = ' '.join(text.split())

            # Limit text length for performance (first 1000 chars usually sufficient)
            if len(text) > 1000:
                text = text[:1000]

            predictions = self.model.predict(text, k=k)
            labels = predictions[0]
            scores = predictions[1]

            if not labels:
                return ('unknown', 0.0)

            # Extract language code from label (format: __label__xx)
            lang_code = labels[0].replace('__label__', '')
            confidence = float(scores[0])

            return (lang_code, confidence)

        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return ('unknown', 0.0)

    def detect_multiple(self, text: str, k: int = 3) -> List[Tuple[str, float]]:
        """
        Detect multiple possible languages for text.

        Args:
            text: Text to detect languages for
            k: Number of top predictions to return

        Returns:
            List of (language_code, confidence_score) tuples
        """
        if not text or not text.strip():
            return [('unknown', 0.0)]

        try:
            text = ' '.join(text.split())
            if len(text) > 1000:
                text = text[:1000]

            predictions = self.model.predict(text, k=k)
            labels = predictions[0]
            scores = predictions[1]

            results = []
            for label, score in zip(labels, scores):
                lang_code = label.replace('__label__', '')
                results.append((lang_code, float(score)))

            return results

        except Exception as e:
            logger.error(f"Multiple language detection failed: {e}")
            return [('unknown', 0.0)]

    def is_eu_language(self, text: str, threshold: float = 0.5) -> Tuple[bool, str, float]:
        """
        Check if text is in one of the 24 EU languages.

        Args:
            text: Text to check
            threshold: Minimum confidence threshold

        Returns:
            Tuple of (is_eu_language, language_code, confidence)
        """
        from ..config import LANGUAGE_CODES

        lang_code, confidence = self.detect(text)

        if confidence >= threshold and lang_code in LANGUAGE_CODES:
            return (True, lang_code, confidence)

        return (False, lang_code, confidence)

    def detect_from_html(self, html: str) -> Tuple[str, float]:
        """
        Detect language from HTML content by extracting text first.

        Args:
            html: HTML content

        Returns:
            Tuple of (language_code, confidence_score)
        """
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html, 'lxml')

            # Remove script and style elements
            for script in soup(['script', 'style', 'noscript']):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            return self.detect(text)

        except Exception as e:
            logger.error(f"Language detection from HTML failed: {e}")
            return ('unknown', 0.0)


# Global instance for reuse
_detector_instance = None


def get_detector() -> LanguageDetector:
    """Get or create global language detector instance."""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = LanguageDetector()
    return _detector_instance
