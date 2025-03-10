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
  # Use Docker CLI to execute commands on each server container
  docker exec -u root crown-test-server$i bash -c "mkdir -p /home/crown_test/.ssh && chmod 700 /home/crown_test/.ssh && echo '$PUBLIC_KEY' > /home/crown_test/.ssh/authorized_keys && chmod 600 /home/crown_test/.ssh/authorized_keys && chown -R crown_test:crown_test /home/crown_test/.ssh"
  echo "Copied public key to server$i"
done

# Now run the tests
python -m crown_deploy.tests.docker_test_runner
