# File: crown_deploy/tests/docker/test_runner.sh
#!/bin/bash
set -e

# Crown Nexus Deployment System - Test Runner Script
# This script handles SSH key setup and runs the deployment tests

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
  SERVER_NAME="crown-test-server$i"
  echo "Setting up SSH key for $SERVER_NAME..."
  
  # Ensure the container is running
  if docker ps | grep -q "$SERVER_NAME"; then
    docker exec -u root "$SERVER_NAME" bash -c "mkdir -p /home/crown_test/.ssh && chmod 700 /home/crown_test/.ssh && echo '$PUBLIC_KEY' > /home/crown_test/.ssh/authorized_keys && chmod 600 /home/crown_test/.ssh/authorized_keys && chown -R crown_test:crown_test /home/crown_test/.ssh"
    echo "✅ SSH key copied to $SERVER_NAME"
  else
    echo "⚠️ Container $SERVER_NAME is not running"
  fi
done

# Test SSH connectivity and wait for services
echo "=== Testing SSH connectivity ==="
for i in 1 2 3; do
  SERVER_IP_VAR="SERVER${i}_IP"
  SERVER_IP="${!SERVER_IP_VAR}"
  
  echo "Testing connection to server$i ($SERVER_IP)..."
  
  # Try SSH connection with timeout (20 attempts, 3s each)
  for attempt in $(seq 1 20); do
    if ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no -o BatchMode=yes crown_test@$SERVER_IP "echo Server $i is ready" 2>/dev/null; then
      echo "✅ SSH connection to server$i successful"
      break
    fi
    
    if [ $attempt -eq 20 ]; then
      echo "❌ Could not connect to server$i after 20 attempts"
    else
      echo "Attempt $attempt: Waiting for SSH on server$i..."
      sleep 3
    fi
  done
done

# Set up test directories
echo "=== Preparing test environment ==="
for i in 1 2 3; do
  SERVER_IP_VAR="SERVER${i}_IP"
  SERVER_IP="${!SERVER_IP_VAR}"
  
  ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no crown_test@$SERVER_IP "sudo mkdir -p /home/crown/crown-nexus && sudo chown -R crown:crown /home/crown/crown-nexus" || echo "⚠️ Could not prepare directories on server$i"
done

# Run the test based on mode
if [ "$GENERATE_ONLY" = "true" ]; then
  echo "=== Running in GENERATE_ONLY mode ==="
  TEST_MODE=generate_only python -m crown_deploy.tests.docker_test_runner
else
  echo "=== Running with full deployment test ==="
  python -m crown_deploy.tests.docker_test_runner
fi
TEST_RESULT=$?

# Extract deployment scripts to mounted volume
echo "=== Extracting deployment scripts ==="
mkdir -p /test-output
cp -r /app/test-deployment/* /test-output/ 2>/dev/null || echo "No deployment scripts to extract"

# Create a summary file
cat > /test-output/README.md << EOF
# Crown Nexus Deployment Scripts
Generated on $(date)

## Test Result: $([ $TEST_RESULT -eq 0 ] && echo "SUCCESS ✅" || echo "FAILED ❌")

## Server Configuration
- Server 1 (172.28.1.10): Database role
- Server 2 (172.28.1.11): Backend role
- Server 3 (172.28.1.12): Frontend role

## Assigned Roles
$(for i in 1 2 3; do
  if [ -d "/app/test-deployment/server$i" ]; then
    echo "### Server $i:"
    ROLES=$(find /app/test-deployment/server$i -name "*.sh" 2>/dev/null | grep -v "setup\|rollback" | sed 's/.*\/\([^\/]*\)\.sh/\1/' | sort)
    if [ -n "$ROLES" ]; then
      echo "Roles:"
      for role in $ROLES; do
        echo "- $role"
      done
    else
      echo "No specific roles assigned"
    fi
  fi
done)

## How to Use These Scripts
1. Copy the scripts to a deployment machine
2. Run \`./deploy.sh\` to deploy Crown Nexus to the configured servers
3. If needed, run \`./rollback.sh\` to roll back the deployment
EOF

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
