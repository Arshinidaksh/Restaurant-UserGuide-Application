FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    WORKER_CONCURRENCY=4 \
    PORT=8000 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Install required system dependencies for Playwright headless Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install --with-deps chromium

COPY server.py .

EXPOSE 8000

CMD ["python", "server.py"]
