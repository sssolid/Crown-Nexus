# File: crown_deploy/tests/docker/specialized-test-runner.sh
#!/bin/bash
set -e

# Generate SSH keys
echo "=== Generating SSH keys ==="
mkdir -p /root/.ssh
ssh-keygen -t rsa -b 2048 -f /root/.ssh/id_rsa -N ""
chmod 600 /root/.ssh/id_rsa
chmod 644 /root/.ssh/id_rsa.pub

# Disable strict host key checking
echo "StrictHostKeyChecking no" > /root/.ssh/config
chmod 600 /root/.ssh/config

# Wait for servers to be ready
echo "=== Waiting for servers to be ready ==="
sleep 10

# Copy SSH keys to servers
echo "=== Copying SSH keys to servers ==="
for i in 1 2 3; do
  docker exec -u root crown-test-server$i bash -c "mkdir -p /home/crown_test/.ssh && chmod 700 /home/crown_test/.ssh && echo '$(cat /root/.ssh/id_rsa.pub)' > /home/crown_test/.ssh/authorized_keys && chmod 600 /home/crown_test/.ssh/authorized_keys && chown -R crown_test:crown_test /home/crown_test/.ssh"
  echo "Copied public key to server$i"
done

# Test service connectivity
echo "=== Testing service connectivity ==="

# Test PostgreSQL
if pg_isready -h $SERVER1_IP -p 5432 -U postgres; then
  echo "✅ PostgreSQL is running on server1"
else
  echo "❌ PostgreSQL is NOT running on server1"
fi

# Test backend
if curl -s http://$SERVER2_IP:8000 > /dev/null; then
  echo "✅ Backend service is running on server2"
else
  echo "❌ Backend service is NOT running on server2"
fi

# Test nginx
if curl -s http://$SERVER3_IP:80 > /dev/null; then
  echo "✅ Nginx is running on server3"
else
  echo "❌ Nginx is NOT running on server3"
fi

# Run test
if [ "$GENERATE_ONLY" = "true" ]; then
  echo "=== Running in GENERATE_ONLY mode ==="
  TEST_MODE=generate_only python -m crown_deploy.tests.docker_test_runner
else
  echo "=== Running with full test ==="
  python -m crown_deploy.tests.docker_test_runner
fi
RESULT=$?

# Extract scripts
echo "=== Extracting scripts to test-output ==="
mkdir -p /test-output
cp -r /app/test-deployment/* /test-output/ 2>/dev/null || echo "Nothing to extract"

# Create a helpful README
cat > /test-output/README.md << EOF
# Crown Nexus Deployment Scripts
Generated on $(date)

## Status: $([ $RESULT -eq 0 ] && echo "SUCCESS ✅" || echo "FAILED ❌")

## Server Configuration
- Server 1 (172.28.1.10): PostgreSQL Database
- Server 2 (172.28.1.11): Python Backend
- Server 3 (172.28.1.12): Nginx Frontend

## Assigned Roles
EOF

# Add role details to README
for i in 1 2 3; do
  if [ -d "/app/test-deployment/server$i" ]; then
    echo "### Server $i:" >> /test-output/README.md
    ROLES=$(find /app/test-deployment/server$i -type f -name "*.sh" 2>/dev/null | grep -v "setup\|rollback" | sed 's/.*\/\([^\/]*\)\.sh/\1/' | sort)
    if [ -n "$ROLES" ]; then
      echo "Roles:" >> /test-output/README.md
      for role in $ROLES; do
        echo "- $role" >> /test-output/README.md
      done
    else
      echo "No specific roles assigned" >> /test-output/README.md
    fi
  fi
done

exit $RESULT
