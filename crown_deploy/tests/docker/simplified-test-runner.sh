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

# Wait for servers
echo "=== Waiting for servers to be ready ==="
sleep 5

# Copy SSH keys to servers
echo "=== Copying SSH keys to servers ==="
for i in 1 2 3; do
  docker exec -u root crown-test-server$i bash -c "mkdir -p /home/crown_test/.ssh && chmod 700 /home/crown_test/.ssh && echo '$(cat /root/.ssh/id_rsa.pub)' > /home/crown_test/.ssh/authorized_keys && chmod 600 /home/crown_test/.ssh/authorized_keys && chown -R crown_test:crown_test /home/crown_test/.ssh"
  echo "Copied public key to server$i"
done

# Run the test - check if GENERATE_ONLY is set
if [ "$GENERATE_ONLY" = "true" ]; then
  echo "=== Running in GENERATE_ONLY mode ==="
  TEST_MODE=generate_only python -m crown_deploy.tests.docker_test_runner
else
  echo "=== Running with full verification ==="
  python -m crown_deploy.tests.docker_test_runner
fi
RESULT=$?

# Extract scripts to mounted volume
echo "=== Extracting deployment scripts ==="
mkdir -p /test-output
cp -r /app/test-deployment/* /test-output/ 2>/dev/null || echo "Nothing to extract"

# Create a helpful README
cat > /test-output/README.md << EOF
# Crown Nexus Deployment Scripts
Generated on $(date)

## Status: $([ $RESULT -eq 0 ] && echo "SUCCESS ✅" || echo "FAILED ❌")

## Server Roles
EOF

# Add server role details
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

echo "Script extraction completed"
exit $RESULT
