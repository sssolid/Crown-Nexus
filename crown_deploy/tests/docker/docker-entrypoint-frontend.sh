# File: crown_deploy/tests/docker/docker-entrypoint-frontend.sh
#!/bin/bash
set -e

# Start nginx
service nginx start

# Start SSH
/usr/sbin/sshd -D
