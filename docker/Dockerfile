# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY polymarket_monitor.py .
COPY example_usage.py .

# Create directories for logs and data
RUN mkdir -p /app/logs /app/data

# Set Python to run in unbuffered mode for real-time logging
ENV PYTHONUNBUFFERED=1

# Run the monitor
CMD ["python", "-u", "polymarket_monitor.py"]

