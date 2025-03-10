# File: crown_deploy/tests/docker/enhanced-test-runner.sh
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

# Get public key content
PUBLIC_KEY=$(cat /root/.ssh/id_rsa.pub)

# Copy public key to servers
echo "=== Copying SSH keys to servers ==="
for i in 1 2 3; do
  docker exec -u root crown-test-server$i bash -c "mkdir -p /home/crown_test/.ssh && chmod 700 /home/crown_test/.ssh && echo '$PUBLIC_KEY' > /home/crown_test/.ssh/authorized_keys && chmod 600 /home/crown_test/.ssh/authorized_keys && chown -R crown_test:crown_test /home/crown_test/.ssh"
  echo "Copied public key to server$i"
done

# Wait for servers to be fully ready
echo "=== Waiting for servers to be ready ==="
for i in 1 2 3; do
  SERVER_IP="SERVER${i}_IP"
  echo "Waiting for server${i} (${!SERVER_IP})..."

  # Wait until SSH is available
  until ssh -o ConnectTimeout=2 -o StrictHostKeyChecking=no crown_test@${!SERVER_IP} "echo Server $i is ready"; do
    echo "Waiting for SSH on server${i}..."
    sleep 2
  done

  # Test if systemd is working
  if ssh crown_test@${!SERVER_IP} "systemctl is-system-running" >/dev/null 2>&1; then
    echo "Systemd is running on server${i}"
  else
    echo "Warning: Systemd may not be fully operational on server${i}"
  fi
done

# Run the deployment test
echo "=== Running deployment test ==="
python -m crown_deploy.tests.docker_test_runner
TEST_RESULT=$?

# Extract deployment scripts to mounted volume if requested
if [ "$EXTRACT_SCRIPTS" = "true" ]; then
  echo "=== Extracting deployment scripts ==="
  mkdir -p /test-output
  cp -r /app/test-deployment/* /test-output/
  echo "Deployment scripts extracted to ./test-output/"

  # Create a summary file
  echo "# Crown Nexus Deployment Scripts" > /test-output/README.md
  echo "Generated on $(date)" >> /test-output/README.md
  echo "" >> /test-output/README.md
  echo "## Server Roles" >> /test-output/README.md

  # Add server role information
  for i in 1 2 3; do
    SERVER_ROLES=$(find /app/test-deployment/server$i -name "*.sh" | grep -v "setup\|rollback" | sed 's/.*\/\([^\/]*\)\.sh/\1/' | tr '\n' ',' | sed 's/,$//')
    echo "- Server $i: $SERVER_ROLES" >> /test-output/README.md
  done

  # Add deployment instructions
  echo "" >> /test-output/README.md
  echo "## Deployment Instructions" >> /test-output/README.md
  echo "1. Copy these scripts to your deployment machine" >> /test-output/README.md
  echo "2. Run \`./deploy.sh\` to deploy to all servers" >> /test-output/README.md
  echo "3. If needed, run \`./rollback.sh\` to revert changes" >> /test-output/README.md
fi

# Show results
if [ $TEST_RESULT -eq 0 ]; then
  echo "=== Test completed successfully ==="
  echo "Deployment scripts are available in ./test-output/"
else
  echo "=== Test failed with code $TEST_RESULT ==="
  echo "Check logs for details"
fi

exit $TEST_RESULT
