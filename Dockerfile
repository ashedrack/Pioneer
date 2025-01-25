# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy Python package files
COPY pyproject.toml setup.py ./
COPY src/ ./src/

# Copy requirements
COPY requirements.txt .

# Install dependencies and the package
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir .

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the application with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
