FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    WORKER_CONCURRENCY=8 \
    PORT=8000 \
    ASSETS_DIR=/app/assets

# Install system libraries needed for Pillow image operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY assets/ ./assets/
COPY server.py .

EXPOSE 8000

CMD ["python", "server.py"]
