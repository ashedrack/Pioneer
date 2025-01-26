# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python package files
COPY pyproject.toml setup.py ./
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Install the package
RUN pip install --no-cache-dir .

# Create necessary directories
RUN mkdir -p /app/logs /app/data

# Set permissions
RUN chmod +x /app/scripts/*

# Expose ports
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=src.main
ENV FLASK_ENV=production

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "src.main:app"]
