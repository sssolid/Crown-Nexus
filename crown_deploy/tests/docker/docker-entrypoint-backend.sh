# File: crown_deploy/tests/docker/docker-entrypoint-backend.sh
#!/bin/bash
set -e

# Create a simple Python HTTP server for testing
python3 -m http.server 8000 &

# Start SSH
/usr/sbin/sshd -D
