# Self-Hosted Deployment Guide

This guide covers deploying Crown Nexus on your own infrastructure.

## System Requirements

- Linux server (Ubuntu 22.04 LTS recommended)
- Python 3.11+
- Node.js 18+
- PostgreSQL 15
- Elasticsearch 8
- Redis 7
- Nginx or similar web server

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/crown-nexus.git
cd crown-nexus
```

### 2. Set Up the Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your production settings

# Run database migrations
alembic upgrade head
```

### 3. Build the Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### 4. Configure Nginx

Create an Nginx configuration file for Crown Nexus:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    # SSL configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Frontend files
    location / {
        root /path/to/crown-nexus/frontend/dist;
        try_files  / /index.html;
    }
    
    # API requests
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host ;
        proxy_set_header X-Real-IP ;
        proxy_set_header X-Forwarded-For ;
        proxy_set_header X-Forwarded-Proto ;
    }
}
```

### 5. Set Up Systemd Service

Create a systemd service file for the backend API:

```ini
[Unit]
Description=Crown Nexus API
After=network.target

[Service]
User=crown-nexus
WorkingDirectory=/path/to/crown-nexus/backend
ExecStart=/path/to/crown-nexus/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=on-failure
Environment="PYTHONPATH=/path/to/crown-nexus/backend"
EnvironmentFile=/path/to/crown-nexus/backend/.env

[Install]
WantedBy=multi-user.target
```

### 6. Start Services

```bash
# Enable and start the API service
sudo systemctl enable crown-nexus-api
sudo systemctl start crown-nexus-api

# Check status
sudo systemctl status crown-nexus-api

# Restart Nginx
sudo systemctl restart nginx
```

## Backup and Maintenance

### Database Backup

Set up regular PostgreSQL backups:

```bash
pg_dump -U postgres crown_nexus > crown_nexus_backup_20250305.sql
```

### Log Rotation

Configure log rotation for the application logs:

```
/var/log/crown-nexus/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 crown-nexus crown-nexus
}
```

### Updates

To update the application:

```bash
cd /path/to/crown-nexus
git pull

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head

# Update frontend
cd ../frontend
npm install
npm run build

# Restart services
sudo systemctl restart crown-nexus-api
```

## Monitoring

Set up monitoring using Prometheus and Grafana to track:

- System resources (CPU, memory, disk)
- Application metrics
- Database performance
- API response times

## Security Considerations

- Keep all software up to date
- Use strong passwords and key-based authentication
- Configure a firewall to restrict access
- Set up fail2ban to prevent brute force attacks
- Enable regular security audits
