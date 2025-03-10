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
    # Frontend role packages
    nginx nodejs npm \
    # Common services
    redis-server \
    # Monitoring tools
    prometheus-node-exporter \
    && rm -rf /var/lib/apt/lists/*

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

# Configure PostgreSQL to listen on all interfaces for testing
RUN echo "listen_addresses = '*'" >> /etc/postgresql/14/main/postgresql.conf && \
    echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/14/main/pg_hba.conf

# Enable services based on server role
RUN systemctl enable postgresql && \
    systemctl enable redis-server && \
    systemctl enable nginx

# Create Docker entrypoint script to start services based on role
COPY docker_entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose common ports
EXPOSE 22 80 8000 5432 6379

# Use systemd as the entrypoint
ENTRYPOINT ["/lib/systemd/systemd"]
