# Crown Nexus Deployment System

A dynamic deployment system for Crown Nexus that can adapt to any number of servers based on hardware specifications and optimal role assignments.

## Overview

This system integrates with the existing `server-analyzer.sh` script to:

1. Analyze server hardware specifications
2. Determine optimal role assignments based on hardware
3. Generate deployment scripts for each server
4. Deploy Crown Nexus with proper configurations
5. Support rollback if needed

## Features

- **Dynamic Role Assignment**: Intelligently assigns server roles based on hardware capabilities
- **Multi-Server Support**: Deploys to any number of servers, not just two
- **Modular Design**: Separates concerns for easier maintenance and extension
- **Secure Configuration**: Generates secure credentials for database, admin, Redis, etc.
- **Rollback Support**: Provides rollback scripts to undo deployment if needed
- **Detailed Logging**: Structured logging for better monitoring and troubleshooting

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
│   │   ├── redis.sh.j2
│   │   ├── elasticsearch.sh.j2
│   │   ├── monitoring.sh.j2
│   │   ├── cicd.sh.j2
│   │   └── storage.sh.j2
│   ├── server_setup.sh.j2     # Server-specific setup
│   └── deploy.sh.j2           # Main deployment script
└── utils/                     # Utility functions
    ├── __init__.py
    ├── errors.py              # Custom exceptions
    ├── logging.py             # Logging configuration
    └── security.py            # Password generation, etc.
```

## Prerequisites

- Python 3.11+
- Jinja2 for templating
- Pydantic for data validation
- Structlog for structured logging
- Access to the `server-analyzer.sh` script

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-org/crown-deploy.git
   cd crown-deploy
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
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
  --analyzer /path/to/server-analyzer.sh \
  --inventory /path/to/inventory.csv \
  --output analysis-results.txt
```

This will output recommended role assignments for your servers.

### 3. Generate Deployment Scripts

```bash
python -m crown_deploy.main generate \
  --analyzer /path/to/server-analyzer.sh \
  --inventory /path/to/inventory.csv \
  --templates /path/to/crown_deploy/templates \
  --output /path/to/deployment-scripts \
  --domain example.com \
  --repo https://github.com/your-org/crown-nexus.git \
  --branch main \
  --admin-email admin@example.com
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

## Customizing Roles

You can customize the role assignments by editing the deployment scripts before running them. The system generates sensible defaults based on server hardware.

## Adding New Role Templates

To add support for a new role:

1. Create a new template file in `templates/roles/`
2. Add the new role to the `ServerRole` enum in `models/server.py`
3. Update the analyzer to detect and recommend the new role

## License

This project is licensed under the MIT License - see the LICENSE file for details.
