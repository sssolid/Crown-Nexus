#!/bin/bash
# Simplified Docker test runner for Crown Nexus
# This approach focuses on script generation and basic service testing
# without requiring SSH connectivity

set -e  # Exit on error

echo "=== Crown Nexus Testing Framework ==="

# Create necessary directories
mkdir -p backend frontend test-output

# Clean up existing containers if requested
if [ "$1" == "--clean" ]; then
  echo "=== Cleaning up existing containers ==="
  docker rm -f crown-test-server1 crown-test-server2 crown-test-server3 crown-test-redis 2>/dev/null || true
  docker volume rm -f crown-data-postgres crown-data-redis crown-data-elasticsearch 2>/dev/null || true
  docker network rm crown-test-network 2>/dev/null || true
fi

# Create Docker network
echo "=== Setting up Docker network ==="
docker network create --subnet=172.28.1.0/24 crown-test-network 2>/dev/null || true

# Start containers using basic images instead of systemd
echo "=== Starting test containers ==="

# Database server (PostgreSQL + Redis)
echo "Starting database server..."
docker run -d --name crown-test-server1 \
  --hostname server1 \
  --network crown-test-network \
  --ip 172.28.1.10 \
  -e POSTGRES_USER=crown_user \
  -e POSTGRES_PASSWORD=crown_password \
  -e POSTGRES_DB=crown_nexus \
  -p 5432:5432 \
  postgres:14-alpine

# Redis server
echo "Starting Redis server..."
docker run -d --name crown-test-redis \
  --hostname redis \
  --network crown-test-network \
  --ip 172.28.1.13 \
  -p 6379:6379 \
  redis:alpine

# Backend server (Python)
echo "Starting backend server..."
docker run -d --name crown-test-server2 \
  --hostname server2 \
  --network crown-test-network \
  --ip 172.28.1.11 \
  -p 8000:8000 \
  -v "$(pwd)/backend:/app" \
  -w /app \
  python:3.11-slim \
  bash -c "pip install -q fastapi uvicorn && python -m http.server 8000"

# Frontend server (Nginx)
echo "Starting frontend server..."
docker run -d --name crown-test-server3 \
  --hostname server3 \
  --network crown-test-network \
  --ip 172.28.1.12 \
  -p 80:80 \
  -v "$(pwd)/frontend:/usr/share/nginx/html" \
  nginx:alpine

# Wait for containers to be ready
echo "=== Waiting for containers to be ready ==="
sleep 5

# Create minimal backend application
echo "=== Creating minimal backend app ==="
mkdir -p backend
cat > backend/main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Crown Nexus API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
EOF

# Create minimal frontend application
echo "=== Creating minimal frontend app ==="
mkdir -p frontend
cat > frontend/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Crown Nexus</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Crown Nexus Frontend</h1>
    <p>This is a simplified test version of the Crown Nexus frontend.</p>
    <div id="status">Checking backend status...</div>

    <script>
        fetch('/api/health')
            .then(response => response.json())
            .then(data => {
                document.getElementById('status').textContent =
                    `Backend status: ${data.status || 'unknown'}`;
            })
            .catch(error => {
                document.getElementById('status').textContent =
                    `Error connecting to backend: ${error}`;
            });
    </script>
</body>
</html>
EOF

# Create test inventory file if it doesn't exist
if [ ! -f "test_inventory.csv" ]; then
  echo "Creating test inventory file..."
  echo "hostname,ip,username,key_path,description" > test_inventory.csv
  echo "server1,172.28.1.10,crown,~/.ssh/id_rsa,Database server" >> test_inventory.csv
  echo "server2,172.28.1.11,crown,~/.ssh/id_rsa,Backend server" >> test_inventory.csv
  echo "server3,172.28.1.12,crown,~/.ssh/id_rsa,Frontend server" >> test_inventory.csv
fi

# Run the script generator with predefined test values
echo "=== Generating deployment scripts ==="
python -m main generate \
  --inventory test_inventory.csv \
  --templates ./templates \
  --output ./test-output \
  --domain crown-test.local \
  --repo https://github.com/sssolid/crown-nexus.git \
  --branch main \
  --admin-email admin@example.com \
  --strategy traditional

# Test if the services are running
echo "=== Testing services ==="

# Test PostgreSQL
echo "Testing PostgreSQL..."
if docker exec crown-test-server1 pg_isready -h localhost; then
  echo "✅ PostgreSQL is running"
else
  echo "❌ PostgreSQL is not running"
fi

# Test Redis
echo "Testing Redis..."
if docker exec crown-test-redis redis-cli ping | grep -q PONG; then
  echo "✅ Redis is running"
else
  echo "❌ Redis is not running"
fi

# Test Backend HTTP Server
echo "Testing backend server..."
if curl -s http://localhost:8000 > /dev/null; then
  echo "✅ Backend server is running"
else
  echo "❌ Backend server is not running"
fi

# Test Frontend Nginx server
echo "Testing frontend server..."
if curl -s -I http://localhost | grep -q "200 OK"; then
  echo "✅ Frontend server is running"
else
  echo "❌ Frontend server is not running"
fi

# Generate report
echo "=== Generating report ==="
cat > test-output/deployment-report.md << EOF
# Crown Nexus Simplified Test Report
Generated on $(date)

## Container Status

| Server | Role | Status | Container |
|--------|------|--------|-----------|
| server1 | Database | $(docker inspect -f '{{.State.Status}}' crown-test-server1 2>/dev/null || echo "Not running") | crown-test-server1 |
| redis | Redis | $(docker inspect -f '{{.State.Status}}' crown-test-redis 2>/dev/null || echo "Not running") | crown-test-redis |
| server2 | Backend | $(docker inspect -f '{{.State.Status}}' crown-test-server2 2>/dev/null || echo "Not running") | crown-test-server2 |
| server3 | Frontend | $(docker inspect -f '{{.State.Status}}' crown-test-server3 2>/dev/null || echo "Not running") | crown-test-server3 |

## Service Status

- **PostgreSQL**: $(docker exec crown-test-server1 pg_isready -h localhost 2>/dev/null && echo "✅ Running" || echo "❌ Not running")
- **Redis**: $(docker exec crown-test-redis redis-cli ping 2>/dev/null | grep -q PONG && echo "✅ Running" || echo "❌ Not running")
- **Backend Server**: $(curl -s http://localhost:8000 > /dev/null 2>&1 && echo "✅ Running" || echo "❌ Not running")
- **Frontend Server**: $(curl -s -I http://localhost 2>/dev/null | grep -q "200 OK" && echo "✅ Running" || echo "❌ Not running")

## Deployment Scripts Generated

- \`deploy.sh\`: Main deployment script
- \`rollback.sh\`: Rollback script
- Server-specific scripts for each server

## Testing Environment

- Frontend URL: http://localhost:80
- Backend URL: http://localhost:8000
- PostgreSQL: postgresql://crown_user:crown_password@localhost:5432/crown_nexus
- Redis: redis://localhost:6379

## How to Use the Scripts

The generated deployment scripts can be used to deploy Crown Nexus to your actual servers.
They have been generated based on a simplified test environment and should be reviewed
before deploying to production.
EOF

echo "=== Test completed ==="
echo "Generated scripts are in the ./test-output directory"
echo "Report is available at ./test-output/deployment-report.md"

# Show the files that were generated
echo "=== Generated files ==="
find test-output -type f | sort
