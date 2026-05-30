FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY apps/api/pyproject.toml apps/api/uv.lock* ./
RUN pip install --no-cache-dir -e ".[dev]"

# Copy application code
COPY apps/api .

# Create data directory
RUN mkdir -p /data

CMD ["python", "-m", "app.workers.main"]
