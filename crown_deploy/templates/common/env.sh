#!/bin/bash

# Crown Nexus deployment environment variables
CROWN_APP_NAME="{{ config.app_name }}"
CROWN_DOMAIN="{{ config.domain }}"
CROWN_REPO_URL="{{ config.repo_url }}"
CROWN_BRANCH="{{ config.git_branch }}"

# Database settings
DB_NAME="{{ config.db_name }}"
DB_USER="{{ config.db_user }}"
DB_PASSWORD="{{ config.db_password }}"

# Admin user settings
ADMIN_EMAIL="{{ config.admin_email }}"
ADMIN_PASSWORD="{{ config.admin_password }}"
ADMIN_NAME="{{ config.admin_name }}"

# Redis password
REDIS_PASSWORD="{{ config.redis_password }}"

# Security
SECRET_KEY="{{ config.secret_key }}"

# Networking
{% for i, server in server_roles %}
SERVER{{ i }}_PUBLIC_IP="{{ server.ip }}"
SERVER{{ i }}_PRIVATE_IP="10.0.0.{{ i }}"  # Using simple private IPs for demonstration
SERVER{{ i }}_ROLES="{{ ','.join(role for role in server.assigned_roles) }}"
SERVER{{ i }}_HOSTNAME="{{ server.hostname }}"
{% endfor %}

# Server indexes
SERVER_COUNT="{{ servers|length }}"
SERVER_INDEXES="{{ range(1, servers|length + 1)|join(' ') }}"

# Role to server mapping
{% for role in roles %}
{{ role|upper }}_SERVERS="{{ [i for i, s, roles in server_roles if role in roles]|join(' ') }}"
{% endfor %}

# Save generated credentials to a secure file
echo "Generated credentials:" > crown-credentials.txt
echo "Database Password: $DB_PASSWORD" >> crown-credentials.txt
echo "Admin Password: $ADMIN_PASSWORD" >> crown-credentials.txt
echo "Redis Password: $REDIS_PASSWORD" >> crown-credentials.txt
echo "Secret Key: $SECRET_KEY" >> crown-credentials.txt

chmod 600 crown-credentials.txt
