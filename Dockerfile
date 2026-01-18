# Multi-stage build for optimized image
FROM python:3.12-alpine as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
RUN apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    python3-dev

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Runtime stage
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Install runtime system dependencies
RUN apk add --no-cache \
    ffmpeg \
    nodejs \
    npm \
    curl \
    unzip \
    bash

# Note: Using Node.js (already installed) as JavaScript runtime for yt-dlp

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create app directory and non-root user
RUN addgroup -S appuser && adduser -S -G appuser appuser
WORKDIR /app

# Create downloads directory with proper permissions
RUN mkdir -p /app/downloads && chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port for web GUI
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Start web interface (directories will be created by the app)
CMD ["python", "gui.py"]
