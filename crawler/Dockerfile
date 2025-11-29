FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy crawler code
COPY config_languages.py .
COPY language_detector.py .
COPY content_extractor.py .
COPY web_spider.py .
COPY download_fasttext_model.py .

# Create directories
RUN mkdir -p /app/data /app/logs

# Download fastText model
RUN python download_fasttext_model.py || true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from language_detector import LanguageDetector; LanguageDetector()" || exit 1

# Default command
CMD ["python", "-m", "scrapy", "crawl", "web_spider", "-a", "language=en"]
