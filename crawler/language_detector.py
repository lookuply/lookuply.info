"""
Language Detection Module for Lookuply Crawler

Detects the language of web content using fastText language identification model.
Supports all 24 EU official languages.
"""

import logging
from typing import Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class LanguageDetector:
    """Detects language of text content using fastText"""

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize language detector

        Args:
            model_path: Path to fastText model (optional, auto-downloads if not provided)
        """
        try:
            import fasttext
            self.ft = fasttext
            self.model = None
            self.model_path = model_path or self._get_default_model()
            self._load_model()
        except ImportError:
            logger.error("fasttext not installed. Install with: pip install fasttext-wheel")
            raise

    def _get_default_model(self) -> str:
        """Get path to default fastText model"""
        home = Path.home()
        model_path = home / '.fasttext' / 'lid.176.ftz'

        # If model doesn't exist, download it
        if not model_path.exists():
            try:
                model_path.parent.mkdir(parents=True, exist_ok=True)
                import urllib.request
                url = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz"
                logger.info(f"Downloading language model from {url}...")
                urllib.request.urlretrieve(url, model_path)
                logger.info(f"Model downloaded to {model_path}")
            except Exception as e:
                logger.error(f"Failed to auto-download model: {e}")
                raise

        return str(model_path)

    def _load_model(self):
        """Load fastText language identification model"""
        try:
            self.model = self.ft.load_model(self.model_path)
            logger.info(f"Language detection model loaded: {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load language model: {e}")
            raise

    def detect(self, text: str, k: int = 1) -> Tuple[str, float]:
        """
        Detect language of given text

        Args:
            text: Text to detect language for
            k: Number of top predictions to return

        Returns:
            Tuple of (language_code, confidence_score)
            Examples: ('en', 0.98), ('de', 0.95), ('fr', 0.87)
        """
        if not text or not isinstance(text, str):
            return ('unknown', 0.0)

        # Clean and normalize text
        text = text.strip()[:500]  # Limit to 500 chars for efficiency
        if len(text) < 10:
            return ('unknown', 0.0)

        try:
            predictions = self.model.predict(text, k=k)
            if predictions and len(predictions) >= 2:
                lang_code = predictions[0][0].replace('__label__', '')
                confidence = predictions[1][0]

                # Map fastText codes to ISO 639-1 codes
                lang_code = self._normalize_language_code(lang_code)

                return (lang_code, confidence)
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")

        return ('unknown', 0.0)

    def detect_with_confidence(self, text: str, min_confidence: float = 0.8) -> Optional[str]:
        """
        Detect language only if confidence is above threshold

        Args:
            text: Text to detect
            min_confidence: Minimum confidence score (0.0-1.0)

        Returns:
            Language code or None if confidence too low
        """
        lang_code, confidence = self.detect(text)

        if confidence >= min_confidence and lang_code != 'unknown':
            return lang_code

        return None

    def detect_multiple(self, text: str, k: int = 3) -> list:
        """
        Get top k language predictions

        Args:
            text: Text to detect
            k: Number of predictions to return

        Returns:
            List of (language_code, confidence) tuples
        """
        try:
            predictions = self.model.predict(text[:500], k=k)
            if predictions and len(predictions) >= 2:
                results = []
                for i, lang in enumerate(predictions[0]):
                    code = lang.replace('__label__', '')
                    code = self._normalize_language_code(code)
                    confidence = predictions[1][i]
                    results.append((code, confidence))
                return results
        except Exception as e:
            logger.warning(f"Multi-language detection failed: {e}")

        return [('unknown', 0.0)]

    @staticmethod
    def _normalize_language_code(code: str) -> str:
        """
        Normalize fastText language code to ISO 639-1

        Maps fastText labels (__label__en, __label__de) to standard codes (en, de)
        """
        code = code.replace('__label__', '').lower()

        # Map common variants
        mapping = {
            'zh': 'zh',  # Chinese
            'pt': 'pt',  # Portuguese
            'es': 'es',  # Spanish
            'fr': 'fr',  # French
            'de': 'de',  # German
            'ja': 'ja',  # Japanese
            'ru': 'ru',  # Russian
            'ko': 'ko',  # Korean
            'tr': 'tr',  # Turkish
            'ar': 'ar',  # Arabic
        }

        return mapping.get(code, code)

    # EU Language codes
    EU_LANGUAGES = {
        'bg', 'hr', 'cs', 'da', 'nl', 'en', 'et', 'fi',
        'fr', 'de', 'el', 'hu', 'ga', 'it', 'lv', 'lt',
        'mt', 'pl', 'pt', 'ro', 'sk', 'sl', 'es', 'sv'
    }

    def is_eu_language(self, lang_code: str) -> bool:
        """Check if language code is one of 24 EU official languages"""
        return lang_code in self.EU_LANGUAGES
