## Database Role Configuration
echo "Setting up Database role on {{ server.hostname }}..."

# Install PostgreSQL
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y postgresql-15 postgresql-contrib-15
echo "database: postgresql-15 postgresql-contrib-15" >> /tmp/crown-nexus-installed/packages.txt

# Open database port to backend servers
{% for backend_server in cluster.get_servers_by_role(ServerRole.BACKEND) %}
sudo ufw allow from {{ backend_server.ip }} to any port 5432 proto tcp
{% endfor %}

# Configure PostgreSQL
echo "Configuring PostgreSQL..."
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Setup database user and database
echo "Setting up database and user..."
sudo -u postgres psql -c "SELECT 1 FROM pg_roles WHERE rolname='{{ cluster.deployment_config.db_user }}'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE USER {{ cluster.deployment_config.db_user }} WITH PASSWORD '{{ cluster.deployment_config.db_password }}';"
sudo -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname='{{ cluster.deployment_config.db_name }}'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE DATABASE {{ cluster.deployment_config.db_name }} OWNER {{ cluster.deployment_config.db_user }};"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE {{ cluster.deployment_config.db_name }} TO {{ cluster.deployment_config.db_user }};"

# Configure PostgreSQL for access from backend servers
cat > /tmp/pg_hba.conf << 'EOF'
# Database administrative login by Unix domain socket
local   all             postgres                                peer

# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     peer
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
{% for backend_server in cluster.get_servers_by_role(ServerRole.BACKEND) %}
host    {{ cluster.deployment_config.db_name }}    {{ cluster.deployment_config.db_user }}    {{ backend_server.ip }}/32    md5
{% endfor %}
EOF

sudo cp /tmp/pg_hba.conf /etc/postgresql/15/main/pg_hba.conf
sudo chown postgres:postgres /etc/postgresql/15/main/pg_hba.conf

# Update PostgreSQL configuration
cat > /tmp/postgresql.conf << 'EOF'
# Default PostgreSQL configuration with optimizations
listen_addresses = 'localhost,{{ server.ip }}'
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
EOF

sudo cp /tmp/postgresql.conf /etc/postgresql/15/main/postgresql.conf
sudo chown postgres:postgres /etc/postgresql/15/main/postgresql.conf
sudo systemctl restart postgresql

# Create backup script
echo "Setting up backup script..."
sudo mkdir -p /opt/{{ cluster.deployment_config.app_name }}/scripts
sudo mkdir -p /opt/{{ cluster.deployment_config.app_name }}/backups

cat > /tmp/backup_db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/{{ cluster.deployment_config.app_name }}/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/{{ cluster.deployment_config.app_name }}_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

# Export DB credentials
export PGPASSWORD="{{ cluster.deployment_config.db_password }}"

# Backup database
pg_dump -U {{ cluster.deployment_config.db_user }} -h localhost {{ cluster.deployment_config.db_name }} > $BACKUP_FILE

# Compress backup
gzip $BACKUP_FILE

# Rotate backups (keep last 30 days)
find $BACKUP_DIR -name "{{ cluster.deployment_config.app_name }}_*.sql.gz" -type f -mtime +30 -delete

# Unset password
unset PGPASSWORD
EOF

sudo mv /tmp/backup_db.sh /opt/{{ cluster.deployment_config.app_name }}/scripts/
sudo chmod +x /opt/{{ cluster.deployment_config.app_name }}/scripts/backup_db.sh
sudo chown -R crown:crown /opt/{{ cluster.deployment_config.app_name }}

# Add backup to crontab
(sudo crontab -u crown -l 2>/dev/null || echo "") | grep -v "backup_db.sh" | \
    { cat; echo "0 2 * * * /opt/{{ cluster.deployment_config.app_name }}/scripts/backup_db.sh"; } | \
    sudo crontab -u crown -

echo "Database setup completed on {{ server.hostname }}"
