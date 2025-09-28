# Multi-stage Dockerfile for Fetch.ai agents
FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent files
COPY . .

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Starting Fetch.ai agents..."\n\
python deployment/start_agents.py\n\
' > start.sh && chmod +x start.sh

# Expose all agent ports
EXPOSE 8001 8002 8003 8004 8005 8006 8007 8008

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8001/health', timeout=5)" || exit 1

# Start all agents
CMD ["./start.sh"]
