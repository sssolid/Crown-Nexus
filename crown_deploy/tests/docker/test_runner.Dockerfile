# File: crown_deploy/tests/docker/test_runner.Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    openssh-client \
    git \
    gcc \
    python3-dev \
    build-essential \
    libpq-dev \
    docker.io \
    iputils-ping \
    iproute2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up SSH directory
RUN mkdir -p /root/.ssh && \
    chmod 700 /root/.ssh

# Create Python environment
RUN pip install --no-cache-dir pytest pytest-asyncio pytest-cov docker

# Copy requirements
COPY requirements.txt test-requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r test-requirements.txt

# Environment will be set up by docker-compose
ENV PYTHONPATH=/app
ENV TEST_MODE=true

# The actual command will be provided by docker-compose
CMD ["bash"]
