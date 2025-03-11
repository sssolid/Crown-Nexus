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

# If FULL_DEPLOYMENT is set, test service connectivity
if [ "$FULL_DEPLOYMENT" = "true" ]; then
  echo "=== Testing full deployment ==="
  
  # Check PostgreSQL connection
  echo "Testing PostgreSQL connection..."
  DB_RESULT=$(ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no crown_test@$SERVER1_IP "sudo -u postgres psql -c 'SELECT version();'" 2>&1)
  if echo "$DB_RESULT" | grep -q "PostgreSQL"; then
    echo "✅ PostgreSQL is running on server1"
  else
    echo "❌ PostgreSQL connection failed: $DB_RESULT"
  fi
  
  # Check Redis connection
  echo "Testing Redis connection..."
  REDIS_RESULT=$(ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no crown_test@$SERVER1_IP "redis-cli ping" 2>&1)
  if echo "$REDIS_RESULT" | grep -q "PONG"; then
    echo "✅ Redis is running on server1"
  else
    echo "❌ Redis connection failed: $REDIS_RESULT"
  fi
  
  # Wait for Elasticsearch to start (it takes longer)
  echo "Waiting for Elasticsearch to start..."
  for attempt in $(seq 1 15); do
    ES_RESULT=$(ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no crown_test@$SERVER2_IP "curl -s http://localhost:9200/_cluster/health" 2>&1)
    if echo "$ES_RESULT" | grep -q "status"; then
      echo "✅ Elasticsearch is running on server2"
      break
    else
      echo "Attempt $attempt: Elasticsearch not yet ready..."
      sleep 5
    fi
    
    if [ $attempt -eq 15 ]; then
      echo "❌ Elasticsearch did not start in time"
    fi
  done
  
  # Check FastAPI backend
  echo "Testing FastAPI backend..."
  BACKEND_RESULT=$(ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no crown_test@$SERVER2_IP "curl -s http://localhost:8000/health" 2>&1)
  if echo "$BACKEND_RESULT" | grep -q "healthy"; then
    echo "✅ FastAPI backend is running on server2"
  else
    echo "❌ FastAPI backend not responding properly: $BACKEND_RESULT"
  fi
  
  # Check Nginx on frontend server
  echo "Testing Nginx frontend..."
  NGINX_RESULT=$(ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no crown_test@$SERVER3_IP "curl -s -I http://localhost" 2>&1)
  if echo "$NGINX_RESULT" | grep -q "200 OK"; then
    echo "✅ Nginx is running on server3"
  else
    echo "❌ Nginx not responding properly: $NGINX_RESULT"
  fi
  
  # Test end-to-end connectivity
  echo "Testing end-to-end connectivity..."
  E2E_RESULT=$(curl -s http://$SERVER3_IP/api/health 2>&1)
  if echo "$E2E_RESULT" | grep -q "healthy"; then
    echo "✅ End-to-end API connectivity is working"
  else
    echo "❌ End-to-end API connectivity failed: $E2E_RESULT"
  fi
  
  # Generate a comprehensive test report
  cat > /test-output/deployment-report.md << EOF
# Crown Nexus Full Deployment Test Report
Generated on $(date)

## Infrastructure Status

| Server | Role | Status | Services |
|--------|------|--------|----------|
| server1 | Database | $(if echo "$DB_RESULT" | grep -q "PostgreSQL"; then echo "✅ Online"; else echo "❌ Issue"; fi) | PostgreSQL, Redis |
| server2 | Backend | $(if echo "$BACKEND_RESULT" | grep -q "healthy"; then echo "✅ Online"; else echo "❌ Issue"; fi) | FastAPI, Elasticsearch |  
| server3 | Frontend | $(if echo "$NGINX_RESULT" | grep -q "200 OK"; then echo "✅ Online"; else echo "❌ Issue"; fi) | Nginx, Vue.js |

## Service Checks

- **PostgreSQL**: $(if echo "$DB_RESULT" | grep -q "PostgreSQL"; then echo "✅ Running"; else echo "❌ Not running"; fi)
- **Redis**: $(if echo "$REDIS_RESULT" | grep -q "PONG"; then echo "✅ Running"; else echo "❌ Not running"; fi)
- **Elasticsearch**: $(if echo "$ES_RESULT" | grep -q "status"; then echo "✅ Running"; else echo "❌ Not running"; fi)
- **FastAPI Backend**: $(if echo "$BACKEND_RESULT" | grep -q "healthy"; then echo "✅ Running"; else echo "❌ Not running"; fi)
- **Nginx Frontend**: $(if echo "$NGINX_RESULT" | grep -q "200 OK"; then echo "✅ Running"; else echo "❌ Not running"; fi)
- **End-to-End API**: $(if echo "$E2E_RESULT" | grep -q "healthy"; then echo "✅ Working"; else echo "❌ Not working"; fi)

## Access Information

- Frontend: http://172.28.1.12
- Backend API: http://172.28.1.11:8000
- Database: postgresql://crown_user:crown_password@172.28.1.10:5432/crown_nexus
- Elasticsearch: http://172.28.1.11:9200
- Redis: redis://172.28.1.10:6379

## Next Steps

1. Access the frontend at http://172.28.1.12
2. API documentation is available at http://172.28.1.11:8000/docs
3. Elasticsearch dashboard is at http://172.28.1.11:9200
EOF

  echo "Full deployment test report generated at /test-output/deployment-report.md"
fi

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
- Server 1 (172.28.1.10): Database role (PostgreSQL, Redis)
- Server 2 (172.28.1.11): Backend role (FastAPI, Elasticsearch)
- Server 3 (172.28.1.12): Frontend role (Vue 3, Nginx)

## Deployed Stack
- Backend: FastAPI, SQLAlchemy (async), Pydantic, Alembic
- Databases: PostgreSQL, Elasticsearch, Redis
- Frontend: Vue 3 (Composition API), TypeScript, Vite, Pinia, Vue Router, Vuetify 3, Axios

## How to Use These Scripts
1. Copy the scripts to a deployment machine
2. Run \`./deploy.sh\` to deploy Crown Nexus to the configured servers
3. If needed, run \`./rollback.sh\` to roll back the deployment
EOF

# Show results
if [ $TEST_RESULT -eq 0 ]; then
  echo "=== Test completed successfully ==="
  echo "Deployment scripts and report extracted to ./test-output/"
else
  echo "=== Test failed with code $TEST_RESULT ==="
  echo "Check logs for details"
  echo "Partial deployment scripts extracted to ./test-output/"
fi

exit $TEST_RESULT
