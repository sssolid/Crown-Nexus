# File: crown_deploy/tests/docker/enhanced-server.Dockerfile
FROM ubuntu:22.04

# Prevent apt from prompting for input
ENV DEBIAN_FRONTEND=noninteractive

# Install essential packages including systemd
RUN apt-get update && apt-get install -y --no-install-recommends \
    systemd systemd-sysv \
    openssh-server \
    sudo \
    python3 python3-pip \
    curl wget vim git \
    apt-transport-https ca-certificates \
    lsb-release gnupg software-properties-common \
    # Basic role requirements
    nginx \
    postgresql \
    redis-server \
    # Test environment tools
    iproute2 iputils-ping \
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
    chown -R crown_test:crown_test /home/crown_test

# Pre-create crown directory for deployment
RUN useradd -m -s /bin/bash crown && \
    echo "crown ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/crown && \
    mkdir -p /home/crown/crown-nexus && \
    chown -R crown:crown /home/crown

# Configure services to start
RUN systemctl enable postgresql && \
    systemctl enable redis-server && \
    systemctl enable nginx

# Use systemd as the entrypoint
ENTRYPOINT ["/lib/systemd/systemd"]
