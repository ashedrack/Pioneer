# Base image
FROM python:3.9

# Set work directory
WORKDIR /app

# Install system dependencies

RUN apt-get update && apt-get install -y --no-install-recommends \

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy dependency files first (to leverage Docker cache)
COPY requirements.txt pyproject.toml setup.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir .

# Copy the rest of the application code

# Copy Python package files
COPY pyproject.toml setup.py ./

# Copy application source code
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Create necessary directories and set permissions
RUN mkdir -p /app/logs /app/data \
    && chmod +x /app/scripts/*

# Install the package
RUN pip install --no-cache-dir .

# Create necessary directories
RUN mkdir -p /app/logs /app/data


# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies and the package
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir .

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

# Run the application using Gunicorn with Uvicorn workers
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "src.main:app"]
