FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src ./src

# Make "src" a discoverable Python package directory
ENV PYTHONPATH="/app/src"

# Expose API port
EXPOSE 8000

# Health checks
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Run FastAPI app
CMD ["uvicorn", "chiron.app:app", "--host", "0.0.0.0", "--port", "8000"]