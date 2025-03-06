#!/bin/bash
# Master deployment script for Crown Nexus
# This script orchestrates the entire two-server deployment process

set -e  # Exit on any error

# Check if correct arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <server1_ip> <server2_ip>"
    echo "  server1_ip: Public IP of the server for load balancer & frontend"
    echo "  server2_ip: Public IP of the server for backend & database"
    exit 1
fi

SERVER1_IP=$1
SERVER2_IP=$2

echo "=== Crown Nexus Deployment ==="
echo "Server 1 (Load Balancer & Frontend): $SERVER1_IP"
echo "Server 2 (Backend & Database): $SERVER2_IP"
echo ""

# Create directory structure
mkdir -p crown-nexus-deployment/{server1,server2,common,scripts}
cd crown-nexus-deployment

# Ask for domain and other key information
read -p "Enter your domain name (e.g., crown-nexus.com): " DOMAIN_NAME
read -p "Enter your Git repository URL: " REPO_URL
read -p "Enter the Git branch to deploy [main]: " GIT_BRANCH
GIT_BRANCH=${GIT_BRANCH:-main}
read -p "Enter admin email: " ADMIN_EMAIL

# Generate secure passwords
DB_PASSWORD=$(openssl rand -base64 24)
ADMIN_PASSWORD=$(openssl rand -base64 12)
REDIS_PASSWORD=$(openssl rand -base64 24)
SECRET_KEY=$(openssl rand -base64 32)

# Set private IPs (assuming 10.0.0.x for internal network)
# In a real deployment, you would use actual private IPs
SERVER1_PRIVATE_IP="10.0.0.1"
SERVER2_PRIVATE_IP="10.0.0.2"

echo "Creating environment file..."
cat > common/env.sh << EOF
#!/bin/bash

# Crown Nexus deployment environment variables
CROWN_APP_NAME="crown-nexus"
CROWN_DOMAIN="$DOMAIN_NAME"
CROWN_REPO_URL="$REPO_URL"
CROWN_BRANCH="$GIT_BRANCH"

# Database settings
DB_NAME="crown_nexus"
DB_USER="crown_user"
DB_PASSWORD="$DB_PASSWORD"

# Admin user settings
ADMIN_EMAIL="$ADMIN_EMAIL"
ADMIN_PASSWORD="$ADMIN_PASSWORD"
ADMIN_NAME="Admin User"

# Redis password
REDIS_PASSWORD="$REDIS_PASSWORD"

# Security
SECRET_KEY="$SECRET_KEY"

# Networking
SERVER1_PRIVATE_IP="$SERVER1_PRIVATE_IP"
SERVER2_PRIVATE_IP="$SERVER2_PRIVATE_IP"
SERVER1_PUBLIC_IP="$SERVER1_IP"
SERVER2_PUBLIC_IP="$SERVER2_IP"

# Save generated credentials to a secure file
echo "Generated credentials:" > crown-credentials.txt
echo "Database Password: $DB_PASSWORD" >> crown-credentials.txt
echo "Admin Password: $ADMIN_PASSWORD" >> crown-credentials.txt
echo "Redis Password: $REDIS_PASSWORD" >> crown-credentials.txt
echo "Secret Key: $SECRET_KEY" >> crown-credentials.txt

chmod 600 crown-credentials.txt
EOF

chmod +x common/env.sh

# Copy environment variables before creating other scripts
source common/env.sh

echo "Creating setup scripts..."

# Create Server 1 setup script
cat > server1/setup.sh << 'EOF'
#!/bin/bash
set -e

# Load environment variables
source ../common/env.sh

echo "=== Setting up Server 1: Load Balancer & Frontend ==="

# Update system
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install necessary packages
echo "Installing required packages..."
sudo apt install -y nginx certbot python3-certbot-nginx fail2ban ufw \
                   git nodejs npm unzip curl wget build-essential

# Setup firewall
echo "Configuring firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Setup application user
echo "Creating application user..."
sudo useradd -m -s /bin/bash crown
sudo usermod -aG sudo crown

# Clone repository
echo "Cloning application repository..."
sudo -u crown git clone $CROWN_REPO_URL -b $CROWN_BRANCH /home/crown/$CROWN_APP_NAME

# Setup Node.js 18
echo "Installing Node.js 18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt update
sudo apt install -y nodejs

# Build frontend
echo "Building frontend application..."
cd /home/crown/$CROWN_APP_NAME/frontend
sudo -u crown npm install
sudo -u crown npm run build

# Configure Nginx
echo "Configuring Nginx..."
cat > /tmp/nginx-config << 'NGINXEOF'
server {
    listen 80;
    server_name $CROWN_DOMAIN www.$CROWN_DOMAIN;

    location / {
        root /home/crown/$CROWN_APP_NAME/frontend/dist;
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "public, max-age=3600";
    }

    location /api {
        proxy_pass http://$SERVER2_PRIVATE_IP:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/v1/docs {
        proxy_pass http://$SERVER2_PRIVATE_IP:8000/api/v1/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
NGINXEOF

# Replace environment variables in Nginx config
envsubst < /tmp/nginx-config > /etc/nginx/sites-available/$CROWN_APP_NAME

# Enable the site
sudo ln -s /etc/nginx/sites-available/$CROWN_APP_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Optimize Nginx
cat > /etc/nginx/nginx.conf << 'NGINXCONFEOF'
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 2048;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
NGINXCONFEOF

sudo systemctl restart nginx

# Configure fail2ban
cat > /etc/fail2ban/jail.local << 'FAIL2BANEOF'
[DEFAULT]
bantime = 86400
findtime = 3600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true
FAIL2BANEOF

sudo systemctl restart fail2ban

# Setup SSL with Let's Encrypt
echo "Setting up SSL..."
sudo certbot --nginx -d $CROWN_DOMAIN -d www.$CROWN_DOMAIN --non-interactive --agree-tos --email $ADMIN_EMAIL

# Create monitoring script
cat > /home/crown/monitor.sh << 'MONITOREOF'
#!/bin/bash

echo "System monitoring report for $(hostname) - $(date)"
echo "------------------------------------------------------"
echo "Load average: $(cat /proc/loadavg)"
echo "Memory usage:"
free -h
echo "------------------------------------------------------"
echo "Disk usage:"
df -h
echo "------------------------------------------------------"
echo "Nginx status:"
systemctl status nginx | grep Active
echo "------------------------------------------------------"
echo "Recent errors in Nginx:"
tail -n 50 /var/log/nginx/error.log | grep -i error
echo "------------------------------------------------------"
MONITOREOF

chmod +x /home/crown/monitor.sh

# Set up cron job for monitoring
(crontab -l 2>/dev/null; echo "0 * * * * /home/crown/monitor.sh > /home/crown/monitoring_report.txt") | crontab -

echo "=== Server 1 setup completed successfully ==="
echo "Frontend deployed at: https://$CROWN_DOMAIN"
EOF

chmod +x server1/setup.sh

# Create Server 2 setup script
cat > server2/setup.sh << 'EOF'
#!/bin/bash
set -e

# Load environment variables
source ../common/env.sh

echo "=== Setting up Server 2: Backend & Database ==="

# Update system
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install necessary packages
echo "Installing required packages..."
sudo apt install -y build-essential python3-dev python3-pip python3-venv \
                   git curl wget unzip software-properties-common \
                   apt-transport-https ca-certificates gnupg lsb-release \
                   fail2ban ufw

# Setup firewall
echo "Configuring firewall..."
sudo ufw allow OpenSSH
sudo ufw allow from $SERVER1_PRIVATE_IP to any port 8000 proto tcp
sudo ufw allow from $SERVER1_PRIVATE_IP to any port 5432 proto tcp
sudo ufw allow from $SERVER1_PRIVATE_IP to any port 9200 proto tcp
sudo ufw allow from $SERVER1_PRIVATE_IP to any port 6379 proto tcp
sudo ufw --force enable

# Install PostgreSQL 15
echo "Installing PostgreSQL..."
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update
sudo apt install -y postgresql-15 postgresql-contrib-15

# Configure PostgreSQL
echo "Configuring PostgreSQL..."
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Setup database user and database
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

# Configure PostgreSQL for access from backend
cat > /tmp/pg_hba.conf << 'PGCONFEOF'
# Database administrative login by Unix domain socket
local   all             postgres                                peer

# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     peer
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
host    $DB_NAME        $DB_USER        $SERVER2_PRIVATE_IP/32  md5
PGCONFEOF

envsubst < /tmp/pg_hba.conf | sudo tee /etc/postgresql/15/main/pg_hba.conf > /dev/null

# Update PostgreSQL configuration
cat > /tmp/postgresql.conf << 'PGMAINEOF'
# Default PostgreSQL configuration with optimizations
listen_addresses = 'localhost,$SERVER2_PRIVATE_IP'
max_connections = 100
shared_buffers = 2GB
effective_cache_size = 6GB
work_mem = 32MB
maintenance_work_mem = 256MB
wal_buffers = 16MB
min_wal_size = 1GB
max_wal_size = 4GB
checkpoint_completion_target = 0.9
random_page_cost = 1.1
effective_io_concurrency = 200
PGMAINEOF

envsubst < /tmp/postgresql.conf | sudo tee /etc/postgresql/15/main/postgresql.conf > /dev/null

sudo systemctl restart postgresql

# Install Elasticsearch
echo "Installing Elasticsearch..."
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" > /etc/apt/sources.list.d/elastic-8.x.list'
sudo apt update
sudo apt install -y elasticsearch

# Configure Elasticsearch
echo "Configuring Elasticsearch..."
cat > /tmp/elasticsearch.yml << 'ESCONFEOF'
cluster.name: crown-nexus
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
network.host: [$SERVER2_PRIVATE_IP, localhost]
http.port: 9200
discovery.type: single-node
xpack.security.enabled: false
ESCONFEOF

envsubst < /tmp/elasticsearch.yml | sudo tee /etc/elasticsearch/elasticsearch.yml > /dev/null

sudo systemctl daemon-reload
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch

# Install Redis
echo "Installing Redis..."
sudo apt install -y redis-server

# Configure Redis
echo "Configuring Redis..."
cat > /tmp/redis.conf << 'REDISCONFEOF'
bind 127.0.0.1 $SERVER2_PRIVATE_IP
protected-mode yes
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize yes
supervised systemd
pidfile /var/run/redis/redis-server.pid
loglevel notice
logfile /var/log/redis/redis-server.log
databases 16
always-show-logo yes
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /var/lib/redis
replica-serve-stale-data yes
replica-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
replica-priority 100
requirepass $REDIS_PASSWORD
maxmemory 512mb
maxmemory-policy allkeys-lru
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no
appendonly no
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
aof-use-rdb-preamble yes
REDISCONFEOF

envsubst < /tmp/redis.conf | sudo tee /etc/redis/redis.conf > /dev/null

sudo systemctl restart redis-server

# Setup application user
echo "Creating application user..."
sudo useradd -m -s /bin/bash crown
sudo usermod -aG sudo crown

# Clone repository
echo "Cloning application repository..."
sudo -u crown git clone $CROWN_REPO_URL -b $CROWN_BRANCH /home/crown/$CROWN_APP_NAME

# Setup Python environment for backend
echo "Setting up Python environment..."
cd /home/crown/$CROWN_APP_NAME/backend
sudo -u crown python3 -m venv venv
sudo -u crown /home/crown/$CROWN_APP_NAME/backend/venv/bin/pip install --upgrade pip
sudo -u crown /home/crown/$CROWN_APP_NAME/backend/venv/bin/pip install -r requirements.txt
sudo -u crown /home/crown/$CROWN_APP_NAME/backend/venv/bin/pip install gunicorn uvloop httptools

# Create environment configuration
echo "Creating environment configuration..."
cat > /tmp/.env << 'ENVEOF'
PROJECT_NAME="Crown Nexus"
API_V1_STR="/api/v1"
SECRET_KEY="$SECRET_KEY"
BACKEND_CORS_ORIGINS=["https://$CROWN_DOMAIN", "https://www.$CROWN_DOMAIN"]
POSTGRES_SERVER=$SERVER2_PRIVATE_IP
POSTGRES_USER=$DB_USER
POSTGRES_PASSWORD=$DB_PASSWORD
POSTGRES_DB=$DB_NAME
ELASTICSEARCH_HOST=$SERVER2_PRIVATE_IP
ELASTICSEARCH_PORT=9200
REDIS_HOST=$SERVER2_PRIVATE_IP
REDIS_PORT=6379
REDIS_PASSWORD=$REDIS_PASSWORD
ENVEOF

envsubst < /tmp/.env | sudo tee /home/crown/$CROWN_APP_NAME/backend/.env > /dev/null
sudo chown crown:crown /home/crown/$CROWN_APP_NAME/backend/.env

# Initialize database and run migrations
echo "Initializing database..."
cd /home/crown/$CROWN_APP_NAME/backend
sudo -u crown /home/crown/$CROWN_APP_NAME/backend/venv/bin/python scripts/init_db.py
sudo -u crown /home/crown/$CROWN_APP_NAME/backend/venv/bin/alembic upgrade head

# Create admin user
echo "Creating admin user..."
sudo -u crown /home/crown/$CROWN_APP_NAME/backend/venv/bin/python scripts/create_admin.py "$ADMIN_EMAIL" "$ADMIN_PASSWORD" "$ADMIN_NAME"

# Create media directories
echo "Creating media directories..."
sudo -u crown mkdir -p /home/crown/$CROWN_APP_NAME/backend/media/{image,document,video,other,thumbnails}

# Create gunicorn configuration
echo "Creating Gunicorn configuration..."
sudo -u crown mkdir -p /home/crown/$CROWN_APP_NAME/backend/gunicorn
cat > /tmp/gunicorn_conf.py << 'GUNICORNEOF'
import multiprocessing

workers_per_core_str = "1"
web_concurrency_str = "2"
host = "0.0.0.0"
port = "8000"
bind_env = f"{host}:{port}"
use_loglevel = "info"
workers_per_core = int(workers_per_core_str)
cores = multiprocessing.cpu_count()
workers = max(int(web_concurrency_str), workers_per_core * cores)
accesslog = "/home/crown/$CROWN_APP_NAME/backend/logs/access.log"
errorlog = "/home/crown/$CROWN_APP_NAME/backend/logs/error.log"

# Gunicorn config
bind = bind_env
workers = workers
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = use_loglevel
GUNICORNEOF

envsubst < /tmp/gunicorn_conf.py | sudo tee /home/crown/$CROWN_APP_NAME/backend/gunicorn/gunicorn_conf.py > /dev/null
sudo chown crown:crown /home/crown/$CROWN_APP_NAME/backend/gunicorn/gunicorn_conf.py

# Create logs directory
echo "Creating logs directory..."
sudo -u crown mkdir -p /home/crown/$CROWN_APP_NAME/backend/logs

# Create systemd service
echo "Creating systemd service..."
cat > /tmp/crown-nexus.service << 'SERVICEEOF'
[Unit]
Description=Crown Nexus API service
After=network.target postgresql.service elasticsearch.service redis-server.service

[Service]
User=crown
Group=crown
WorkingDirectory=/home/crown/$CROWN_APP_NAME/backend
Environment="PATH=/home/crown/$CROWN_APP_NAME/backend/venv/bin"
ExecStart=/home/crown/$CROWN_APP_NAME/backend/venv/bin/gunicorn -c gunicorn/gunicorn_conf.py app.main:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEEOF

envsubst < /tmp/crown-nexus.service | sudo tee /etc/systemd/system/$CROWN_APP_NAME.service > /dev/null

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable $CROWN_APP_NAME
sudo systemctl start $CROWN_APP_NAME

# Configure log rotation
echo "Configuring log rotation..."
cat > /tmp/logrotate-config << 'LOGROTATEEOF'
/home/crown/$CROWN_APP_NAME/backend/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 crown crown
    sharedscripts
    postrotate
        systemctl reload $CROWN_APP_NAME
    endscript
}
LOGROTATEEOF

envsubst < /tmp/logrotate-config | sudo tee /etc/logrotate.d/$CROWN_APP_NAME > /dev/null

# Create backup script
echo "Setting up backup script..."
sudo mkdir -p /opt/$CROWN_APP_NAME/scripts
sudo mkdir -p /opt/$CROWN_APP_NAME/backups

cat > /tmp/backup_db.sh << 'BACKUPEOF'
#!/bin/bash
BACKUP_DIR="/opt/$CROWN_APP_NAME/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/$CROWN_APP_NAME_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

# Export DB credentials
export PGPASSWORD=$DB_PASSWORD

# Backup database
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_FILE

# Compress backup
gzip $BACKUP_FILE

# Rotate backups (keep last 30 days)
find $BACKUP_DIR -name "$CROWN_APP_NAME_*.sql.gz" -type f -mtime +30 -delete

# Unset password
unset PGPASSWORD
BACKUPEOF

envsubst < /tmp/backup_db.sh | sudo tee /opt/$CROWN_APP_NAME/scripts/backup_db.sh > /dev/null
sudo chmod +x /opt/$CROWN_APP_NAME/scripts/backup_db.sh
sudo chown -R crown:crown /opt/$CROWN_APP_NAME

# Add backup to crontab
(sudo crontab -u crown -l 2>/dev/null; echo "0 2 * * * /opt/$CROWN_APP_NAME/scripts/backup_db.sh") | sudo crontab -u crown -

# Create monitoring script
cat > /tmp/monitor.sh << 'MONITOREOF'
#!/bin/bash

echo "System monitoring report for $(hostname) - $(date)"
echo "------------------------------------------------------"
echo "Load average: $(cat /proc/loadavg)"
echo "Memory usage:"
free -h
echo "------------------------------------------------------"
echo "Disk usage:"
df -h
echo "------------------------------------------------------"
echo "Crown Nexus service status:"
systemctl status $CROWN_APP_NAME | grep Active
echo "------------------------------------------------------"
echo "PostgreSQL status:"
systemctl status postgresql | grep Active
echo "------------------------------------------------------"
echo "Elasticsearch status:"
systemctl status elasticsearch | grep Active
echo "------------------------------------------------------"
echo "Redis status:"
systemctl status redis-server | grep Active
echo "------------------------------------------------------"
echo "Recent backend errors:"
tail -n 50 /home/crown/$CROWN_APP_NAME/backend/logs/error.log | grep -i error
echo "------------------------------------------------------"
MONITOREOF

envsubst < /tmp/monitor.sh | sudo tee /home/crown/monitor.sh > /dev/null
sudo chmod +x /home/crown/monitor.sh
sudo chown crown:crown /home/crown/monitor.sh

# Set up cron job for monitoring
(sudo crontab -u crown -l 2>/dev/null; echo "0 * * * * /home/crown/monitor.sh > /home/crown/monitoring_report.txt") | sudo crontab -u crown -

echo "=== Server 2 setup completed successfully ==="
echo "Backend running at: http://$SERVER2_PRIVATE_IP:8000"
echo "API documentation available at: https://$CROWN_DOMAIN/api/v1/docs"
EOF

chmod +x server2/setup.sh

# Create security hardening script
cat > common/harden.sh << 'EOF'
#!/bin/bash
set -e

echo "=== Hardening security settings ==="

# Configure SSH
echo "Configuring secure SSH..."
sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart ssh

# Setup automatic security updates
echo "Setting up automatic security updates..."
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# Configure fail2ban
echo "Configuring fail2ban..."
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Setup firewall basic rules
echo "Configuring basic firewall rules..."
sudo ufw allow OpenSSH
sudo ufw --force enable

# Secure shared memory
echo "Securing shared memory..."
echo "tmpfs /run/shm tmpfs defaults,noexec,nosuid 0 0" | sudo tee -a /etc/fstab

# Configure system security settings
echo "Configuring system security settings..."
sudo bash -c "cat > /etc/sysctl.d/99-security.conf" << 'SYSCTLEOF'
# IP Spoofing protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignore ICMP broadcast requests
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Disable source packet routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0

# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Block SYN attacks
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 5

# Log Martians
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1

# Disable IP forwarding
net.ipv4.ip_forward = 0
SYSCTLEOF

sudo sysctl -p /etc/sysctl.d/99-security.conf

echo "=== Security hardening completed ==="
EOF

chmod +x common/harden.sh

# Create advanced monitoring script
cat > common/monitoring.sh << 'EOF'
#!/bin/bash
set -e

# Load environment variables
source ../common/env.sh

echo "=== Setting up advanced monitoring ==="

# Install monitoring tools
echo "Installing monitoring tools..."
sudo apt install -y prometheus prometheus-node-exporter

# Configure Prometheus
echo "Configuring Prometheus..."
sudo cat > /etc/prometheus/prometheus.yml << 'PROMETHEUSEOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node"
    static_configs:
      - targets: ["localhost:9100", "$SERVER1_PRIVATE_IP:9100", "$SERVER2_PRIVATE_IP:9100"]
PROMETHEUSEOF

sudo systemctl restart prometheus
sudo systemctl enable prometheus

# Create basic system health check script
echo "Creating health check script..."
cat > /home/crown/health_check.sh << 'HEALTHEOF'
#!/bin/bash

# System health check script
REPORT_FILE="/home/crown/health_report.txt"
ALERT_EMAIL="$ADMIN_EMAIL"

# Start fresh report
echo "System Health Report - $(date)" > $REPORT_FILE
echo "=======================================" >> $REPORT_FILE

# Check disk space
echo -e "\n== Disk Space ==" >> $REPORT_FILE
df -h / | grep -v Filesystem >> $REPORT_FILE

# Check memory
echo -e "\n== Memory Usage ==" >> $REPORT_FILE
free -h >> $REPORT_FILE

# Check load average
echo -e "\n== Load Average ==" >> $REPORT_FILE
uptime >> $REPORT_FILE

# Check for failed services
echo -e "\n== Failed Services ==" >> $REPORT_FILE
systemctl --failed >> $REPORT_FILE

# Check system logs for errors
echo -e "\n== Recent System Errors ==" >> $REPORT_FILE
journalctl -p err..emerg --since "1 hour ago" | tail -n 20 >> $REPORT_FILE

# Check application specific logs
if [ -f /home/crown/$CROWN_APP_NAME/backend/logs/error.log ]; then
    echo -e "\n== Application Errors ==" >> $REPORT_FILE
    tail -n 50 /home/crown/$CROWN_APP_NAME/backend/logs/error.log | grep -i error >> $REPORT_FILE
fi

# Check if we need to send alerts
DISK_USAGE=$(df -h / | grep / | awk '{print $5}' | sed 's/%//')
MEMORY_USAGE=$(free | grep Mem | awk '{print $3/$2 * 100.0}' | cut -d. -f1)
LOAD=$(uptime | awk '{print $(NF-2)}' | sed 's/,//')

# Send email alert if thresholds exceeded
if [ $DISK_USAGE -gt 85 ] || [ $MEMORY_USAGE -gt 90 ] || [ $(echo "$LOAD > 5" | bc) -eq 1 ]; then
    # Install mailutils if not present
    if ! command -v mail &> /dev/null; then
        sudo apt-get install -y mailutils
    fi

    echo "ALERT: System resources critical on $(hostname) at $(date)" | mail -s "System Alert: $(hostname)" $ALERT_EMAIL
fi
HEALTHEOF

chmod +x /home/crown/health_check.sh
chown crown:crown /home/crown/health_check.sh

# Set up cron job for health checks
(crontab -l 2>/dev/null; echo "*/15 * * * * /home/crown/health_check.sh") | crontab -

echo "=== Monitoring setup completed ==="
EOF

chmod +x common/monitoring.sh

# Create troubleshooting script
cat > scripts/troubleshoot.sh << 'EOF'
#!/bin/bash

# Load environment variables
source ../common/env.sh

echo "=== Crown Nexus Troubleshooting Tool ==="
echo "Running diagnostics..."

# Check system resources
echo -e "\n== System Resources =="
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}'
echo "Memory Usage:"
free -h | awk '/^Mem:/ {print $3 "/" $2 " (" int($3/$2*100)")%"}'
echo "Disk Space:"
df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}'

# Check key services
echo -e "\n== Service Status =="
for SERVICE in nginx postgresql elasticsearch redis-server crown-nexus; do
    if systemctl is-active --quiet $SERVICE 2>/dev/null; then
        echo "$SERVICE: ✅ Running"
    else
        echo "$SERVICE: ❌ Not running"
        echo "  - Checking logs: "
        journalctl -u $SERVICE --no-pager -n 20 | grep -i "error\|failed\|warn" | tail -5
    fi
done

# Check network connectivity
echo -e "\n== Network Connectivity =="

# Check if server can reach other server
if [ "$(hostname -I | awk '{print $1}')" = "$SERVER1_PRIVATE_IP" ]; then
    if ping -c 1 $SERVER2_PRIVATE_IP &> /dev/null; then
        echo "Server 1 -> Server 2: ✅ Connected"
    else
        echo "Server 1 -> Server 2: ❌ Connection failed"
    fi
else
    if ping -c 1 $SERVER1_PRIVATE_IP &> /dev/null; then
        echo "Server 2 -> Server 1: ✅ Connected"
    else
        echo "Server 2 -> Server 1: ❌ Connection failed"
    fi
fi

# Check database connectivity
echo -e "\n== Database Connectivity =="
if command -v psql &> /dev/null; then
    if [ -z "$DB_PASSWORD" ] || [ -z "$DB_USER" ] || [ -z "$DB_NAME" ]; then
        echo "Database credentials not found in environment"
    else
        export PGPASSWORD=$DB_PASSWORD
        if psql -U $DB_USER -h $SERVER2_PRIVATE_IP -d $DB_NAME -c "SELECT 1" &> /dev/null; then
            echo "Database connection: ✅ Successful"
        else
            echo "Database connection: ❌ Failed"
            echo "  - Checking PostgreSQL logs:"
            sudo tail -5 /var/log/postgresql/postgresql-15-main.log
        fi
        unset PGPASSWORD
    fi
else
    echo "psql command not found. Install postgresql-client package."
fi

# Check application logs for errors
echo -e "\n== Recent Application Errors =="
if [ -f /home/crown/$CROWN_APP_NAME/backend/logs/error.log ]; then
    grep -i "error\|exception\|fail" /home/crown/$CROWN_APP_NAME/backend/logs/error.log | tail -10
else
    echo "No application logs found at expected location."
fi

# Check for common issues
echo -e "\n== Common Issues Check =="

# Check permissions
echo "Directory Permissions:"
ls -ld /home/crown/$CROWN_APP_NAME/backend/media /home/crown/$CROWN_APP_NAME/backend/logs 2>/dev/null || echo "Directories not found"

# Check environment file
echo "Environment File:"
if [ -f /home/crown/$CROWN_APP_NAME/backend/.env ]; then
    echo "  ✅ .env file exists"
else
    echo "  ❌ .env file missing"
fi

echo -e "\n== Troubleshooting Recommendations =="

# Based on checks, provide recommendations
if ! systemctl is-active --quiet nginx 2>/dev/null; then
    echo "- Start/restart Nginx: sudo systemctl restart nginx"
fi

if ! systemctl is-active --quiet postgresql 2>/dev/null; then
    echo "- Start/restart PostgreSQL: sudo systemctl restart postgresql"
fi

if ! systemctl is-active --quiet crown-nexus 2>/dev/null; then
    echo "- Start/restart Crown Nexus: sudo systemctl restart crown-nexus"
    echo "- Check logs: sudo journalctl -u crown-nexus -n 50"
fi

if [ ! -f /home/crown/$CROWN_APP_NAME/backend/.env ]; then
    echo "- Create missing .env file from example"
fi

echo -e "\nFor more detailed troubleshooting, check the full logs or run specific diagnoses."
EOF

chmod +x scripts/troubleshoot.sh

# Create backup script
cat > server2/backup.sh << 'EOF'
#!/bin/bash
set -e

# Load environment variables
source ../common/env.sh

echo "=== Setting up backup strategy ==="

# Create backup directories
sudo mkdir -p /opt/$CROWN_APP_NAME/backups/{database,media,config}
sudo chown -R crown:crown /opt/$CROWN_APP_NAME/backups

# Create database backup script
cat > /opt/$CROWN_APP_NAME/scripts/backup_db.sh << 'BACKUPSCRIPTEOF'
#!/bin/bash
BACKUP_DIR="/opt/$CROWN_APP_NAME/backups/database"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/$DB_NAME-$TIMESTAMP.sql"

# Make sure backup directory exists
mkdir -p $BACKUP_DIR

# Export DB credentials (only for the duration of this script)
export PGPASSWORD=$DB_PASSWORD

# Backup database
echo "Creating database backup: $BACKUP_FILE"
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_FILE

# Compress backup
echo "Compressing database backup..."
gzip $BACKUP_FILE

# Create backup metadata
echo "Backup created on $(date)" > "$BACKUP_DIR/$DB_NAME-$TIMESTAMP.meta"
echo "From host: $(hostname)" >> "$BACKUP_DIR/$DB_NAME-$TIMESTAMP.meta"
echo "Database: $DB_NAME" >> "$BACKUP_DIR/$DB_NAME-$TIMESTAMP.meta"

# Rotate backups (keep last 30 days)
echo "Cleaning old backups..."
find $BACKUP_DIR -name "$DB_NAME-*.sql.gz" -type f -mtime +30 -delete
find $BACKUP_DIR -name "$DB_NAME-*.meta" -type f -mtime +30 -delete

# Unset password
unset PGPASSWORD

echo "Database backup completed: $BACKUP_FILE.gz"
BACKUPSCRIPTEOF

chmod +x /opt/$CROWN_APP_NAME/scripts/backup_db.sh

# Create media backup script
cat > /opt/$CROWN_APP_NAME/scripts/backup_media.sh << 'MEDIASCRIPTEOF'
#!/bin/bash
BACKUP_DIR="/opt/$CROWN_APP_NAME/backups/media"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/media-$TIMESTAMP.tar.gz"
MEDIA_DIR="/home/crown/$CROWN_APP_NAME/backend/media"

# Make sure backup directory exists
mkdir -p $BACKUP_DIR

# Backup media files
echo "Creating media backup: $BACKUP_FILE"
tar -czf $BACKUP_FILE -C $(dirname $MEDIA_DIR) $(basename $MEDIA_DIR)

# Create backup metadata
echo "Backup created on $(date)" > "$BACKUP_DIR/media-$TIMESTAMP.meta"
echo "From host: $(hostname)" >> "$BACKUP_DIR/media-$TIMESTAMP.meta"
echo "Media directory: $MEDIA_DIR" >> "$BACKUP_DIR/media-$TIMESTAMP.meta"

# Keep only weekly backups after 60 days
find $BACKUP_DIR -name "media-*.tar.gz" -type f -mtime +60 -not -mtime +7 -delete
find $BACKUP_DIR -name "media-*.meta" -type f -mtime +60 -not -mtime +7 -delete

# Keep only monthly backups after 180 days
find $BACKUP_DIR -name "media-*.tar.gz" -type f -mtime +180 -not -mtime +30 -delete
find $BACKUP_DIR -name "media-*.meta" -type f -mtime +180 -not -mtime +30 -delete

echo "Media backup completed: $BACKUP_FILE"
MEDIASCRIPTEOF

chmod +x /opt/$CROWN_APP_NAME/scripts/backup_media.sh

# Create configuration backup script
cat > /opt/$CROWN_APP_NAME/scripts/backup_config.sh << 'CONFIGSCRIPTEOF'
#!/bin/bash
BACKUP_DIR="/opt/$CROWN_APP_NAME/backups/config"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/config-$TIMESTAMP.tar.gz"

# Make sure backup directory exists
mkdir -p $BACKUP_DIR

# Files to back up
CONFIG_FILES=(
  "/home/crown/$CROWN_APP_NAME/backend/.env"
  "/etc/nginx/sites-available/$CROWN_APP_NAME"
  "/etc/systemd/system/$CROWN_APP_NAME.service"
  "/etc/postgresql/15/main/postgresql.conf"
  "/etc/postgresql/15/main/pg_hba.conf"
  "/etc/elasticsearch/elasticsearch.yml"
  "/etc/redis/redis.conf"
)

# Create a temporary directory
TEMP_DIR=$(mktemp -d)

# Copy files to temporary directory
for FILE in "${CONFIG_FILES[@]}"; do
  if [ -f "$FILE" ]; then
    DIR_NAME=$(dirname "$FILE" | sed 's/^\///')
    mkdir -p "$TEMP_DIR/$DIR_NAME"
    cp "$FILE" "$TEMP_DIR/$FILE"
  fi
done

# Backup configuration files
echo "Creating configuration backup: $BACKUP_FILE"
tar -czf $BACKUP_FILE -C $TEMP_DIR .

# Remove temporary directory
rm -rf $TEMP_DIR

# Create backup metadata
echo "Backup created on $(date)" > "$BACKUP_DIR/config-$TIMESTAMP.meta"
echo "From host: $(hostname)" >> "$BACKUP_DIR/config-$TIMESTAMP.meta"
echo "Configuration files:" >> "$BACKUP_DIR/config-$TIMESTAMP.meta"
printf "  %s\n" "${CONFIG_FILES[@]}" >> "$BACKUP_DIR/config-$TIMESTAMP.meta"

# Rotate backups (keep last 30 versions)
ls -t $BACKUP_DIR/config-*.tar.gz | tail -n +31 | xargs rm -f 2>/dev/null || true
ls -t $BACKUP_DIR/config-*.meta | tail -n +31 | xargs rm -f 2>/dev/null || true

echo "Configuration backup completed: $BACKUP_FILE"
CONFIGSCRIPTEOF

chmod +x /opt/$CROWN_APP_NAME/scripts/backup_config.sh

# Set correct ownership for all scripts
sudo chown -R crown:crown /opt/$CROWN_APP_NAME/scripts/

# Add to crontab for automatic backups
(sudo crontab -u crown -l 2>/dev/null; echo "0 2 * * * /opt/$CROWN_APP_NAME/scripts/backup_db.sh") | sudo crontab -u crown -
(sudo crontab -u crown -l 2>/dev/null; echo "0 3 * * 0 /opt/$CROWN_APP_NAME/scripts/backup_media.sh") | sudo crontab -u crown -
(sudo crontab -u crown -l 2>/dev/null; echo "0 4 * * 0 /opt/$CROWN_APP_NAME/scripts/backup_config.sh") | sudo crontab -u crown -

echo "=== Backup strategy setup completed ==="
EOF

chmod +x server2/backup.sh

# Create deployment script
cat > deploy.sh << 'EOF'
#!/bin/bash
set -e

# Load environment variables
source common/env.sh

echo "=== Starting Crown Nexus Deployment ==="

# Setup ssh keys if not already done
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "SSH key not found. Creating new SSH key..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
    echo "Please ensure this SSH key is added to both servers."
    echo "Run: ssh-copy-id ubuntu@$SERVER1_PUBLIC_IP"
    echo "Run: ssh-copy-id ubuntu@$SERVER2_PUBLIC_IP"
    read -p "Press Enter once SSH keys are set up..."
fi

# Prepare servers - copy setup scripts to servers
echo "Copying setup scripts to servers..."

# Server 1 setup
echo "Setting up Server 1 (Load Balancer & Frontend)..."
ssh-keyscan -H $SERVER1_PUBLIC_IP >> ~/.ssh/known_hosts 2>/dev/null
scp -r server1 common ubuntu@$SERVER1_PUBLIC_IP:~/
ssh ubuntu@$SERVER1_PUBLIC_IP "cd server1 && bash setup.sh && cd .. && cd common && bash harden.sh && bash monitoring.sh"

# Server 2 setup
echo "Setting up Server 2 (Backend & Database)..."
ssh-keyscan -H $SERVER2_PUBLIC_IP >> ~/.ssh/known_hosts 2>/dev/null
scp -r server2 common scripts ubuntu@$SERVER2_PUBLIC_IP:~/
ssh ubuntu@$SERVER2_PUBLIC_IP "cd server2 && bash setup.sh && bash backup.sh && cd .. && cd common && bash harden.sh && bash monitoring.sh"

echo "=== Deployment completed successfully ==="
echo ""
echo "Frontend URL: https://$CROWN_DOMAIN"
echo "API Documentation: https://$CROWN_DOMAIN/api/v1/docs"
echo ""
echo "Admin login:"
echo "  Email: $ADMIN_EMAIL"
echo "  Password: $ADMIN_PASSWORD"
echo ""
echo "Please save your credentials file (crown-credentials.txt) in a secure location."
echo "You will need these credentials for maintenance and administration."
EOF

chmod +x deploy.sh

echo "=== Deployment scripts created successfully ==="
echo "To deploy Crown Nexus, run: ./deploy.sh"
echo "Make sure you have SSH access to both servers."
echo "Credentials will be saved in crown-credentials.txt"
