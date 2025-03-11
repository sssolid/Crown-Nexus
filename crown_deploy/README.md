# Crown Nexus Deployment System

A dynamic deployment system for Crown Nexus that can adapt to any number of servers based on hardware specifications and optimal role assignments.

## Overview

This system uses a Python-based server analyzer to:

1. Analyze server hardware specifications
2. Determine optimal role assignments based on hardware
3. Generate deployment scripts for each server
4. Deploy Crown Nexus with proper configurations
5. Support rollback if needed

## Features

- **Dynamic Role Assignment**: Intelligently assigns server roles based on hardware capabilities
- **Multi-Server Support**: Deploys to any number of servers, not just a fixed amount
- **Modular Design**: Separates concerns for easier maintenance and extension
- **Secure Configuration**: Generates secure credentials for database, admin, Redis, etc.
- **Rollback Support**: Provides rollback scripts to undo deployment if needed
- **Detailed Logging**: Structured logging for better monitoring and troubleshooting
- **Docker Testing**: Test deployments in Docker containers before deploying to production

## Prerequisites

- Python 3.11+
- SSH access to the target servers
- Git (for cloning the repository)
- Docker and Docker Compose (for testing)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/crown-deploy.git
cd crown-deploy
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Development Dependencies (optional)

```bash
pip install -r test-requirements.txt
```

## Project Structure

```
crown_deploy/
├── __init__.py                # Package initialization
├── main.py                    # Main entry point
├── models/                    # Data models
│   ├── __init__.py
│   ├── server.py              # Server & role models
│   ├── config.py              # Configuration models
│   └── deployment.py          # Deployment state models
├── services/                  # Business logic
│   ├── __init__.py
│   ├── analyzer.py            # Server analyzer service
│   ├── deployment.py          # Deployment orchestration
│   └── script_generator.py    # Deployment script generation
├── templates/                 # Script templates
│   ├── common/
│   │   ├── env.sh.j2          # Environment variables
│   │   └── harden.sh.j2       # Security hardening
│   ├── roles/                 # Role-specific templates
│   │   ├── load_balancer.sh.j2
│   │   ├── frontend.sh.j2
│   │   ├── backend.sh.j2
│   │   ├── database.sh.j2
│   │   └── ...
│   ├── docker/                # Docker templates
│   ├── kubernetes/            # Kubernetes templates
│   ├── server_setup.sh.j2     # Server-specific setup
│   ├── deploy.sh.j2           # Main deployment script
│   └── rollback.sh.j2         # Rollback script
├── tests/                     # Test code
│   ├── __init__.py
│   ├── docker/                # Docker testing utilities
│   │   ├── server.Dockerfile  # Test server Dockerfile
│   │   ├── test_runner.Dockerfile # Test runner Dockerfile
│   │   ├── docker_entrypoint.sh # Container entrypoint script
│   │   └── test_runner.sh     # Main test script
│   └── docker_test_runner.py  # Python test runner
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── errors.py              # Custom exceptions
│   ├── logging.py             # Logging configuration
│   ├── path.py                # Path utilities
│   └── security.py            # Password generation, etc.
├── docker-compose.yml         # Docker Compose for testing
├── run-tests.sh               # Helper script for running tests
├── requirements.txt           # Project dependencies
└── test-requirements.txt      # Test dependencies
```

## Usage

### 1. Create Server Inventory

Create a CSV file with your server details:

```csv
hostname,ip,username,key_path,description
server1,192.168.1.101,ubuntu,~/.ssh/id_rsa,Primary server
server2,192.168.1.102,ubuntu,~/.ssh/id_rsa,Secondary server
server3,192.168.1.103,ubuntu,~/.ssh/id_rsa,Tertiary server
```

### 2. Analyze Servers

```bash
python -m crown_deploy.main analyze \
  --inventory /path/to/inventory.csv \
  --output analysis-results.txt
```

This will output recommended role assignments for your servers.

### 3. Generate Deployment Scripts

#### Traditional Deployment

```bash
python -m crown_deploy.main generate \
  --inventory /path/to/inventory.csv \
  --templates ./crown_deploy/templates \
  --output /path/to/deployment-scripts \
  --domain example.com \
  --repo https://github.com/your-org/crown-nexus.git \
  --branch main \
  --admin-email admin@example.com \
  --strategy traditional
```

#### Docker Deployment

```bash
python -m crown_deploy.main generate \
  --inventory inventory.csv \
  --templates ./crown_deploy/templates \
  --output ./deployment \
  --domain example.com \
  --repo https://github.com/your-org/crown-nexus.git \
  --admin-email admin@example.com \
  --strategy docker \
  --docker-registry registry.example.com
```

#### Kubernetes Deployment

```bash
python -m crown_deploy.main generate \
  --inventory inventory.csv \
  --templates ./crown_deploy/templates \
  --output ./deployment \
  --domain example.com \
  --repo https://github.com/your-org/crown-nexus.git \
  --admin-email admin@example.com \
  --strategy kubernetes \
  --docker-registry registry.example.com \
  --k8s-namespace crown-nexus-prod \
  --storage-class fast-ssd
```

### 4. Deploy Crown Nexus

```bash
cd /path/to/deployment-scripts
./deploy.sh
```

### 5. Rollback if Needed

```bash
cd /path/to/deployment-scripts
./rollback.sh
```

## Docker Testing Framework

The Docker testing framework allows you to test your deployment scripts in Docker containers before deploying to actual servers.

### Running Docker Tests

1. Use the included script to run tests:

```bash
# Run full tests with deployment
./run-tests.sh

# Generate scripts only
./run-tests.sh --generate-only

# Clean up before running
./run-tests.sh --clean

# Enable debug mode
./run-tests.sh --debug
```

2. Alternatively, use Docker Compose directly:

```bash
# Build the test environment
docker-compose build

# Run tests with script generation only
docker-compose run -e GENERATE_ONLY=true test-runner

# Run full tests with deployment
docker-compose run test-runner

# Clean up after testing
docker-compose down -v
```

### Docker Test Process

1. **Set up containers**: Creates 3 Docker containers that simulate your servers
2. **Server analysis**: Runs the analyzer to evaluate container specs and assign roles
3. **Script generation**: Generates deployment scripts
4. **Test deployment**: Executes the deployment against the containers (unless in generate-only mode)
5. **Verification**: Verifies the deployment succeeded

### Test Output

The testing framework creates a `test-output` directory containing:
- Generated deployment scripts
- A README with test results
- Role assignments for each server

## Troubleshooting

### Common Issues

#### 1. Path Issues on Windows

If you're using Windows and see path-related errors, ensure you're using the correct path format:

```python
# In your code
from crown_deploy.utils.path import normalize_path

# Use the normalize_path function for all paths
normalized_path = normalize_path(path)
```

#### 2. SSH Connection Issues

If you encounter SSH connection issues during testing:

```bash
# Run tests in debug mode
./run-tests.sh --debug

# Check Docker logs for SSH service
docker logs crown-test-server1
```

#### 3. Template Syntax Errors

If you see Jinja2 template syntax errors:

- Avoid using Python-style list comprehensions in templates
- Use Jinja2 filters (e.g., `{{ items|join(',') }}`) instead of Python methods
- Make sure `ServerRole` is passed to all templates

#### 4. Docker Test Failures

If the Docker tests fail:

```bash
# Clean up existing containers and volumes
./run-tests.sh --clean

# Check if Docker containers are running
docker ps | grep crown-test
```

## Development Workflow

### 1. Set Up Development Environment

```bash
git clone https://github.com/your-org/crown-deploy.git
cd crown-deploy
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r test-requirements.txt
```

### 2. Make Changes

1. Modify code as needed
2. Update tests if necessary

### 3. Test Changes Locally

```bash
# Run unit tests
pytest

# Test with Docker
./run-tests.sh
```

### 4. Commit Changes

```bash
git add .
git commit -m "Your commit message"
git push
```

## Best Practices

1. **Test before deploying**: Always test your deployment scripts in Docker before deploying to actual servers.
2. **Version control**: Keep track of your deployment scripts and states.
3. **Secure credentials**: Store generated credentials in a secure location.
4. **Backup data**: Always back up critical data before deployment or rollback.
5. **Follow template syntax**: Use Jinja2-compatible syntax in templates.
6. **Explicit encoding**: Always specify UTF-8 encoding when writing files.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
