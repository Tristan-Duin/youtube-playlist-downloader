FROM python:3.12-alpine as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    python3-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN apk add --no-cache \
    ffmpeg \
    nodejs \
    npm \
    curl \
    unzip \
    bash

# Note: Using Node.js (already installed) as JavaScript runtime for yt-dlp

COPY --from=builder /opt/venv /opt/venv

RUN addgroup -S appuser && adduser -S -G appuser appuser
WORKDIR /app
RUN mkdir -p /app/downloads && chown -R appuser:appuser /app
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

CMD ["python", "gui.py"]
