# File: crown_deploy/tests/docker/docker-entrypoint-database.sh
#!/bin/bash
set -e

# Start PostgreSQL service
service postgresql start

# Start SSH
/usr/sbin/sshd -D
