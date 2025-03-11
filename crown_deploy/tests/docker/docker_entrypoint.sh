# File: crown_deploy/tests/docker/docker_entrypoint.sh
#!/bin/bash
set -e

# This script is not used with systemd as the entrypoint,
# but is included for reference or for use with non-systemd containers

# Start services based on server role
case "$SERVER_ROLE" in
  database)
    echo "Starting database role services..."
    service postgresql start
    ;;
  backend)
    echo "Starting backend role services..."
    # Start a simple Python HTTP server for testing
    python3 -m http.server 8000 &
    ;;
  frontend)
    echo "Starting frontend role services..."
    service nginx start
    ;;
  *)
    echo "No specific role set, starting SSH only"
    ;;
esac

# Start SSH server
echo "Starting SSH server..."
/usr/sbin/sshd -D
