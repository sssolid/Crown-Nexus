FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including build tools and Docker CLI
RUN apt-get update && apt-get install -y \
    openssh-client \
    git \
    gcc \
    python3-dev \
    build-essential \
    libpq-dev \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY test-requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r test-requirements.txt

# Set up SSH directory
RUN mkdir -p /root/.ssh && \
    chmod 700 /root/.ssh

# Copy source code
COPY . .

# Command will be provided by docker-compose
CMD ["bash"]
