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

# Wait for servers to be ready
echo "=== Waiting for servers to initialize ==="
sleep 10  # Allow systemd to initialize

# Copy public key to servers
echo "=== Copying SSH keys to servers ==="
for i in 1 2 3; do
  # Check if container is running
  if docker ps | grep -q "crown-test-server$i"; then
    docker exec -u root crown-test-server$i bash -c "mkdir -p /home/crown_test/.ssh && chmod 700 /home/crown_test/.ssh && echo '$PUBLIC_KEY' > /home/crown_test/.ssh/authorized_keys && chmod 600 /home/crown_test/.ssh/authorized_keys && chown -R crown_test:crown_test /home/crown_test/.ssh"
    echo "Copied public key to server$i"
  else
    echo "Warning: crown-test-server$i is not running, trying IP-based connection"
    SERVER_IP="SERVER${i}_IP"
    # Create an alternative approach using sshpass or wait for SSH to be available
    echo "Server $i (${!SERVER_IP}) not ready yet. Will try SSH connection later."
  fi
done

# Wait for servers to be fully ready
echo "=== Waiting for SSH services to start ==="
for i in 1 2 3; do
  SERVER_IP="SERVER${i}_IP"
  echo "Waiting for server${i} (${!SERVER_IP})..."

  # Try for up to 60 seconds (20 attempts, 3 seconds apart)
  for attempt in $(seq 1 20); do
    if ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no -o BatchMode=yes crown_test@${!SERVER_IP} "echo Server $i is ready" 2>/dev/null; then
      echo "Server $i is ready (SSH access successful)"
      break
    fi

    if [ $attempt -eq 20 ]; then
      echo "Warning: Could not connect to server $i after 60 seconds"
    else
      echo "Attempt $attempt: Waiting for SSH on server${i}..."
      sleep 3
    fi
  done
done

# Set up test directories and prepare environment
echo "=== Preparing test environment ==="
for i in 1 2 3; do
  SERVER_IP="SERVER${i}_IP"
  if ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no crown_test@${!SERVER_IP} "sudo mkdir -p /home/crown/crown-nexus && sudo chown -R crown:crown /home/crown/crown-nexus" 2>/dev/null; then
    echo "Test directories prepared on server $i"
  else
    echo "Warning: Could not prepare test directories on server $i"
  fi
done

# Run the deployment test
echo "=== Running deployment test ==="
python -m crown_deploy.tests.docker_test_runner
TEST_RESULT=$?

# Extract deployment scripts to mounted volume
echo "=== Extracting deployment scripts ==="
mkdir -p /test-output
cp -r /app/test-deployment/* /test-output/ 2>/dev/null || echo "No deployment scripts to extract"

# Create a summary file
echo "# Crown Nexus Deployment Scripts" > /test-output/README.md
echo "Generated on $(date)" >> /test-output/README.md
echo "" >> /test-output/README.md
echo "## Test Result: $([ $TEST_RESULT -eq 0 ] && echo 'SUCCESS' || echo 'FAILED')" >> /test-output/README.md
echo "" >> /test-output/README.md
echo "## Server Roles" >> /test-output/README.md

# Add server role information if available
for i in 1 2 3; do
  SERVER_ROLES=$(find /app/test-deployment/server$i -name "*.sh" 2>/dev/null | grep -v "setup\|rollback" | sed 's/.*\/\([^\/]*\)\.sh/\1/' | tr '\n' ',' | sed 's/,$//' || echo "unknown")
  echo "- Server $i: $SERVER_ROLES" >> /test-output/README.md
done

# Show results
if [ $TEST_RESULT -eq 0 ]; then
  echo "=== Test completed successfully ==="
  echo "Deployment scripts extracted to ./test-output/"
else
  echo "=== Test failed with code $TEST_RESULT ==="
  echo "Check logs for details"
  echo "Partial deployment scripts extracted to ./test-output/"
fi

exit $TEST_RESULT
