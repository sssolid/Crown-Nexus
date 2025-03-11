FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install common packages for all server roles
RUN apt-get update && apt-get install -y \
    systemd systemd-sysv \
    openssh-server \
    sudo \
    python3 python3-pip python3-venv \
    curl wget vim git \
    apt-transport-https ca-certificates \
    lsb-release gnupg software-properties-common \
    iproute2 iputils-ping \
    # Database role packages
    postgresql postgresql-contrib \
    # Backend role packages
    build-essential \
    python3-dev \
    # Frontend role packages (minus nodejs for now)
    nginx \
    # Common services
    redis-server \
    # Monitoring tools
    prometheus-node-exporter \
    # Dependencies for Elasticsearch
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Remove existing Node.js packages to avoid conflicts
RUN apt-get update && apt-get remove -y nodejs nodejs-doc libnode-dev libnode72 && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js 18 properly
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs && \
    npm install -g yarn && \
    rm -rf /var/lib/apt/lists/*

# Install Elasticsearch
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-8.x.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends elasticsearch \
    && rm -rf /var/lib/apt/lists/*

# Configure Elasticsearch
RUN mkdir -p /etc/elasticsearch && echo "xpack.security.enabled: false" >> /etc/elasticsearch/elasticsearch.yml \
    && echo "network.host: 0.0.0.0" >> /etc/elasticsearch/elasticsearch.yml \
    && echo "discovery.type: single-node" >> /etc/elasticsearch/elasticsearch.yml

# Configure systemd
RUN cd /lib/systemd/system/sysinit.target.wants/ && \
    ls | grep -v systemd-tmpfiles-setup | xargs rm -f && \
    rm -f /lib/systemd/system/multi-user.target.wants/* && \
    rm -f /etc/systemd/system/*.wants/* && \
    rm -f /lib/systemd/system/local-fs.target.wants/* && \
    rm -f /lib/systemd/system/sockets.target.wants/*udev* && \
    rm -f /lib/systemd/system/sockets.target.wants/*initctl* && \
    rm -f /lib/systemd/system/basic.target.wants/* && \
    echo "ReadKernelModules=no" >> /etc/systemd/system.conf && \
    echo "ReadKernelMessageLog=no" >> /etc/systemd/system.conf

# Set up SSH
RUN mkdir -p /var/run/sshd && \
    echo 'PermitRootLogin no' >> /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config && \
    systemctl enable ssh

# Create test user
RUN useradd -m -s /bin/bash crown_test && \
    echo "crown_test ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/crown_test && \
    mkdir -p /home/crown_test/.ssh && \
    chmod 700 /home/crown_test/.ssh && \
    chown -R crown_test:crown_test /home/crown_test/.ssh

# Create crown user for testing deployment
RUN useradd -m -s /bin/bash crown && \
    echo "crown ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/crown && \
    mkdir -p /home/crown/crown-nexus && \
    chown -R crown:crown /home/crown

# Create application directories
RUN mkdir -p /app/backend /app/frontend && \
    chown -R crown:crown /app

# Configure PostgreSQL to listen on all interfaces for testing
RUN echo "listen_addresses = '*'" >> /etc/postgresql/14/main/postgresql.conf && \
    echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/14/main/pg_hba.conf

# Configure Redis to accept remote connections
RUN sed -i 's/bind 127.0.0.1 ::1/bind 0.0.0.0/g' /etc/redis/redis.conf && \
    sed -i 's/protected-mode yes/protected-mode no/g' /etc/redis/redis.conf

# Enable services based on server role
RUN systemctl enable postgresql && \
    systemctl enable redis-server && \
    systemctl enable nginx && \
    systemctl enable elasticsearch

# Create Docker entrypoint script to start services based on role
COPY docker_entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose common ports
EXPOSE 22 80 8000 5432 6379 9200 9300

# Use systemd as the entrypoint
ENTRYPOINT ["/lib/systemd/systemd"]
