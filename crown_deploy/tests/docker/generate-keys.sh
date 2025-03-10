# File: crown_deploy/tests/docker/generate-keys.sh

#!/bin/bash
# Generate new SSH keys and copy to server containers

# Generate a new SSH key pair
mkdir -p /root/.ssh
ssh-keygen -t rsa -b 2048 -f /root/.ssh/id_rsa -N ""
chmod 600 /root/.ssh/id_rsa
chmod 644 /root/.ssh/id_rsa.pub

# Disable strict host key checking
echo "StrictHostKeyChecking no" > /root/.ssh/config
chmod 600 /root/.ssh/config

# Get the public key content
PUBLIC_KEY=$(cat /root/.ssh/id_rsa.pub)

# Copy the public key to each server container
for i in 1 2 3; do
  docker exec -u root crown-test-server$i bash -c "mkdir -p /home/crown_test/.ssh && chmod 700 /home/crown_test/.ssh && echo '$PUBLIC_KEY' > /home/crown_test/.ssh/authorized_keys && chmod 600 /home/crown_test/.ssh/authorized_keys && chown -R crown_test:crown_test /home/crown_test/.ssh"
  echo "Copied public key to server$i"
done

# Run only the test runner and skip the debugger
echo "Running docker test runner..."
# Run the test runner with error handling
python -m crown_deploy.tests.docker_test_runner
TEST_RESULT=$?

# Show deployment script contents if successful
if [ $TEST_RESULT -eq 0 ]; then
  echo "==== Generated Deployment Script (first 20 lines) ===="
  sed -n '1,20p' /app/test-deployment/deploy.sh
  echo "========= (end of preview) ========="
else
  echo "Test runner failed with error code $TEST_RESULT"
fi

exit $TEST_RESULT

# Only run debugger if specifically requested with DEBUG=true
if [ "$DEBUG" = "true" ]; then
  echo "Running deployment debugger..."
  python -m crown_deploy.tests.deployment_debugger
fi
