FROM ubuntu:22.04

# Set non-interactive frontend to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install SSH server and essential tools
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    python3 \
    python3-pip \
    curl \
    wget \
    vim \
    git \
    apt-transport-https \
    ca-certificates \
    lsb-release \
    gnupg \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Setup SSH
RUN mkdir /var/run/sshd
RUN echo 'PermitRootLogin prohibit-password' >> /etc/ssh/sshd_config
RUN echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config

# Create test user
RUN useradd -m -s /bin/bash crown_test && \
    echo "crown_test ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/crown_test

## Setup SSH keys directory
#RUN mkdir -p /home/crown_test/.ssh
#RUN chown -R crown_test:crown_test /home/crown_test/.ssh && \
#    chmod 700 /home/crown_test/.ssh \
## This line is critical - SSH is very strict about permissions
#RUN chmod 600 /home/crown_test/.ssh/authorized_keys || true

# Start SSH server
CMD ["/usr/sbin/sshd", "-D"]
