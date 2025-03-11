"""Script generator service for the Crown Nexus deployment system."""
from __future__ import annotations

import os
import jinja2
from pathlib import Path
from typing import Dict, Any, List, Set

import structlog

from models.server import Server, ServerRole
from models.config import ClusterConfig
from models.deployment_strategy import DeploymentStrategyType
from utils.errors import ScriptGenerationError

# Initialize logger
logger = structlog.get_logger()


class ScriptGenerator:
    """Class to generate deployment scripts based on templates."""

    def __init__(self, template_dir: Path, output_dir: Path):
        """Initialize with template and output directories."""
        self.template_dir = template_dir
        self.output_dir = output_dir

        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "common").mkdir(exist_ok=True)
        (self.output_dir / "scripts").mkdir(exist_ok=True)

        # Setup Jinja2 environment
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_dir)),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Add ServerRole to global Jinja environment so it's available in all templates
        self.jinja_env.globals['ServerRole'] = ServerRole

    def generate_all_scripts(self, cluster: ClusterConfig) -> None:
        """Generate all deployment scripts for the cluster."""
        logger.info("Generating deployment scripts")

        # Determine the deployment strategy
        strategy_type = cluster.deployment_config.strategy.type

        # Generate scripts based on deployment strategy
        if strategy_type == DeploymentStrategyType.TRADITIONAL:
            # Traditional deployment (direct to servers)
            self._generate_traditional_deployment(cluster)
        elif strategy_type == DeploymentStrategyType.DOCKER:
            # Docker-based deployment
            self._generate_docker_deployment(cluster)
        elif strategy_type == DeploymentStrategyType.KUBERNETES:
            # Kubernetes-based deployment
            self._generate_kubernetes_deployment(cluster)
        else:
            raise ScriptGenerationError(f"Unknown deployment strategy: {strategy_type}")

        # Set executable permissions on all scripts
        self._set_executable_permissions()

        logger.info("Deployment scripts generated",
                    output_dir=str(self.output_dir),
                    strategy=strategy_type)

    def _generate_traditional_deployment(self, cluster: ClusterConfig) -> None:
        """Generate scripts for traditional direct-to-server deployment."""
        # Generate common environment file
        self._generate_env_file(cluster)

        # Generate server-specific setup scripts
        for i, server in enumerate(cluster.servers, 1):
            server_dir = self.output_dir / f"server{i}"
            server_dir.mkdir(exist_ok=True)
            self._generate_server_setup_script(server, i, cluster)

        # Generate the main deployment script
        self._generate_deployment_script(cluster)

        # Generate rollback scripts
        self._generate_rollback_scripts(cluster)

    def _generate_docker_deployment(self, cluster: ClusterConfig) -> None:
        """Generate scripts for Docker-based deployment."""
        # Create directories
        docker_dir = self.output_dir / "docker"
        docker_dir.mkdir(exist_ok=True)

        # Create subdirectories for components
        for component in ["frontend", "backend", "monitoring"]:
            component_dir = docker_dir / component
            component_dir.mkdir(exist_ok=True)

        # Generate Dockerfiles
        self._generate_docker_files(cluster, docker_dir)

        # Generate docker-compose.yml
        self._generate_docker_compose(cluster, docker_dir)

        # Generate deployment script for Docker
        self._generate_docker_deployment_script(cluster, docker_dir)

        # Generate rollback script for Docker
        self._generate_docker_rollback_script(cluster, docker_dir)

    def _generate_kubernetes_deployment(self, cluster: ClusterConfig) -> None:
        """Generate scripts for Kubernetes-based deployment."""
        # Create directories
        k8s_dir = self.output_dir / "kubernetes"
        k8s_dir.mkdir(exist_ok=True)

        # Generate Kubernetes manifests
        self._generate_kubernetes_manifests(cluster, k8s_dir)

        # Generate Dockerfiles for building images
        docker_dir = self.output_dir / "docker"
        docker_dir.mkdir(exist_ok=True)
        for component in ["frontend", "backend"]:
            component_dir = docker_dir / component
            component_dir.mkdir(exist_ok=True)

        self._generate_docker_files(cluster, docker_dir)

        # Generate deployment script for Kubernetes
        self._generate_kubernetes_deployment_script(cluster, k8s_dir)

        # Generate rollback script for Kubernetes
        self._generate_kubernetes_rollback_script(cluster, k8s_dir)

    def _generate_env_file(self, cluster: ClusterConfig) -> None:
        """Generate the common environment file with deployment variables."""
        template = self.jinja_env.get_template("common/env.sh.j2")

        # Prepare context for template rendering
        context = {
            "config": cluster.deployment_config,
            "servers": cluster.servers,
            "server_roles": [(i, server, server.assigned_roles)
                             for i, server in enumerate(cluster.servers, 1)],
            "roles": ServerRole
        }

        # Create output file
        env_file = self.output_dir / "common" / "env.sh"
        env_file.write_text(template.render(**context))

        logger.info("Generated common environment file", file=str(env_file))

    def _generate_server_setup_script(self, server: Server, server_index: int, cluster: ClusterConfig) -> None:
        """Generate setup script for a specific server based on its roles."""
        template = self.jinja_env.get_template("server_setup.sh.j2")

        # Get role-specific templates
        role_templates = {}
        for role in server.assigned_roles:
            role_template_path = f"roles/{role}.sh.j2"
            try:
                role_templates[role] = self.jinja_env.get_template(role_template_path)
            except jinja2.exceptions.TemplateNotFound:
                logger.warning(f"Template not found for role: {role}",
                               template_path=role_template_path)

        # Prepare context for template rendering
        context = {
            "server": server,
            "server_index": server_index,
            "cluster": cluster,
            "role_templates": role_templates,
            "ServerRole": ServerRole,  # Also add to context for backwards compatibility
        }

        # Create output file
        setup_file = self.output_dir / f"server{server_index}" / "setup.sh"
        setup_file.write_text(template.render(**context), encoding='utf-8')

        logger.info("Generated server setup script",
                    server=server.hostname,
                    file=str(setup_file))

    def _generate_deployment_script(self, cluster: ClusterConfig) -> None:
        """Generate the main deployment script."""
        template = self.jinja_env.get_template("deploy.sh.j2")

        # Prepare context for template rendering
        context = {
            "cluster": cluster,
            "server_count": len(cluster.servers),
        }

        # Create output file
        deploy_file = self.output_dir / "deploy.sh"
        deploy_file.write_text(template.render(**context), encoding='utf-8')

        logger.info("Generated main deployment script", file=str(deploy_file))

    def _generate_rollback_scripts(self, cluster: ClusterConfig) -> None:
        """Generate rollback scripts for each server."""
        # Generate a master rollback script using the template
        template = self.jinja_env.get_template("rollback.sh.j2")

        # Prepare context for template rendering
        context = {
            "cluster": cluster,
            "server_count": len(cluster.servers),
        }

        # Create output file
        rollback_file = self.output_dir / "rollback.sh"
        rollback_file.write_text(template.render(**context), encoding='utf-8')

        # Generate individual server rollback scripts
        for i, server in enumerate(cluster.servers, 1):
            self._generate_server_rollback_script(server, i)

    def _generate_server_rollback_script(self, server: Server, server_index: int) -> None:
        """Generate rollback script for a specific server."""
        # This would ideally use a template, but for simplicity we'll generate directly
        rollback_file = self.output_dir / f"server{server_index}" / "rollback.sh"

        content = "#!/bin/bash\n\n"
        content += f"# Rollback script for {server.hostname}\n\n"
        content += "echo \"=== Rolling back Crown Nexus components ===\"\n\n"

        # Add commands to stop services based on roles
        content += "# Stop services\n"
        if ServerRole.BACKEND in server.assigned_roles:
            content += "sudo systemctl stop crown-nexus 2>/dev/null || true\n"

        if ServerRole.LOAD_BALANCER in server.assigned_roles or ServerRole.FRONTEND in server.assigned_roles:
            content += "sudo systemctl stop nginx 2>/dev/null || true\n"

        if ServerRole.DATABASE in server.assigned_roles:
            content += "sudo systemctl stop postgresql 2>/dev/null || true\n"

        if ServerRole.ELASTICSEARCH in server.assigned_roles:
            content += "sudo systemctl stop elasticsearch 2>/dev/null || true\n"

        if ServerRole.REDIS in server.assigned_roles:
            content += "sudo systemctl stop redis-server 2>/dev/null || true\n"

        # Add commands to remove application files
        content += "\n# Remove application files\n"
        content += "sudo rm -rf /home/crown/crown-nexus 2>/dev/null || true\n"
        content += "sudo rm -rf /opt/crown-nexus 2>/dev/null || true\n\n"

        # Add commands to remove configuration files
        content += "# Remove configuration files\n"
        if ServerRole.LOAD_BALANCER in server.assigned_roles or ServerRole.FRONTEND in server.assigned_roles:
            content += "sudo rm -f /etc/nginx/sites-available/crown-nexus 2>/dev/null || true\n"
            content += "sudo rm -f /etc/nginx/sites-enabled/crown-nexus 2>/dev/null || true\n"

        if ServerRole.BACKEND in server.assigned_roles:
            content += "sudo rm -f /etc/systemd/system/crown-nexus.service 2>/dev/null || true\n"
            content += "sudo systemctl daemon-reload 2>/dev/null || true\n"

        content += "\necho \"Rollback completed for this server.\"\n"

        rollback_file.write_text(content)

    def _generate_docker_files(self, cluster: ClusterConfig, docker_dir: Path) -> None:
        """Generate Dockerfiles for components."""
        # Generate Dockerfile for frontend
        frontend_dockerfile = self.jinja_env.get_template("docker/frontend/Dockerfile.j2")
        (docker_dir / "frontend" / "Dockerfile").write_text(
            frontend_dockerfile.render(cluster=cluster)
        )

        # Create nginx config directory
        nginx_dir = docker_dir / "frontend" / "nginx"
        nginx_dir.mkdir(exist_ok=True)

        # Create basic nginx config
        nginx_config = """
server {
    listen 80;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "public, max-age=3600";
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
        (nginx_dir / "default.conf").write_text(nginx_config)

        # Create docker-entrypoint script
        entrypoint_script = """#!/bin/sh
# Replace environment variables in JS files
find /usr/share/nginx/html -type f -name "*.js" -exec sed -i "s|BACKEND_URL_PLACEHOLDER|${BACKEND_URL}|g" {} \\;

# Start nginx
exec "$@"
"""
        (nginx_dir / "docker-entrypoint.sh").write_text(entrypoint_script)

        # Generate Dockerfile for backend
        backend_dockerfile = self.jinja_env.get_template("docker/backend/Dockerfile.j2")
        (docker_dir / "backend" / "Dockerfile").write_text(
            backend_dockerfile.render(cluster=cluster)
        )

    def _generate_docker_compose(self, cluster: ClusterConfig, docker_dir: Path) -> None:
        """Generate docker-compose.yml file."""
        docker_compose = self.jinja_env.get_template("docker/docker-compose.yml.j2")
        (docker_dir / "docker-compose.yml").write_text(
            docker_compose.render(cluster=cluster)
        )

    def _generate_docker_deployment_script(self, cluster: ClusterConfig, docker_dir: Path) -> None:
        """Generate deployment script for Docker."""
        # Create deploy.sh script
        deploy_script = f"""#!/bin/bash
# Docker deployment script for Crown Nexus
# Generated by Crown Nexus Deployment System

set -e  # Exit on any error

echo "=== Crown Nexus Docker Deployment ==="
echo "Started at: $(date)"
echo ""

# Build Docker images
echo "Building Docker images..."
cd {docker_dir.relative_to(self.output_dir)}

# Build frontend image
echo "Building frontend image..."
docker build -t crown-nexus-frontend:latest ./frontend

# Build backend image
echo "Building backend image..."
docker build -t crown-nexus-backend:latest ./backend

# Push images if registry is configured
"""

        # Add registry push if configured
        if cluster.deployment_config.strategy.docker.registry:
            registry = cluster.deployment_config.strategy.docker.registry
            deploy_script += f"""
echo "Pushing images to registry: {registry}..."
docker tag crown-nexus-frontend:latest {registry}/crown-nexus-frontend:latest
docker tag crown-nexus-backend:latest {registry}/crown-nexus-backend:latest
docker push {registry}/crown-nexus-frontend:latest
docker push {registry}/crown-nexus-backend:latest

"""

        # Add docker-compose up command
        deploy_script += """
# Start the application
echo "Starting Crown Nexus with Docker Compose..."
docker compose up -d

echo ""
echo "=== Deployment completed successfully ==="
echo "Crown Nexus should now be available at:"
echo "  Frontend: http://localhost (configure Nginx or DNS as needed)"
echo "  Backend API: http://localhost:8000/api/v1"
echo ""
echo "To check logs, run: docker compose logs -f"
echo "To stop the application, run: docker compose down"
"""

        # Write the script
        deploy_file = self.output_dir / "deploy.sh"
        deploy_file.write_text(deploy_script)

    def _generate_docker_rollback_script(self, cluster: ClusterConfig, docker_dir: Path) -> None:
        """Generate rollback script for Docker."""
        # Create rollback.sh script
        rollback_script = f"""#!/bin/bash
# Docker rollback script for Crown Nexus
# Generated by Crown Nexus Deployment System

set -e  # Exit on any error

echo "=== Crown Nexus Docker Rollback ==="
echo "Started at: $(date)"
echo ""

# Confirm rollback
read -p "WARNING: This will remove all Crown Nexus containers and volumes. Continue? [y/N] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Rollback aborted."
    exit 1
fi

# Stop and remove containers
cd {docker_dir.relative_to(self.output_dir)}
echo "Stopping and removing containers..."
docker compose down

# Remove volumes if requested
read -p "Do you want to remove persistent volumes (data will be lost)? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing volumes..."
    docker compose down -v
fi

# Remove images
read -p "Do you want to remove Docker images? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing images..."
    docker rmi crown-nexus-frontend:latest crown-nexus-backend:latest
"""

        # Add registry image removal if configured
        if cluster.deployment_config.strategy.docker.registry:
            registry = cluster.deployment_config.strategy.docker.registry
            rollback_script += f"""
    docker rmi {registry}/crown-nexus-frontend:latest {registry}/crown-nexus-backend:latest
"""

        rollback_script += """
fi

echo ""
echo "=== Rollback completed successfully ==="
"""

        # Write the script
        rollback_file = self.output_dir / "rollback.sh"
        rollback_file.write_text(rollback_script)

    def _generate_kubernetes_manifests(self, cluster: ClusterConfig, k8s_dir: Path) -> None:
        """Generate Kubernetes manifest files."""
        # Generate deployment.yaml
        deployment = self.jinja_env.get_template("kubernetes/deployment.yaml.j2")
        (k8s_dir / "deployment.yaml").write_text(
            deployment.render(cluster=cluster)
        )

    def _generate_kubernetes_deployment_script(self, cluster: ClusterConfig, k8s_dir: Path) -> None:
        """Generate deployment script for Kubernetes."""
        namespace = cluster.deployment_config.strategy.kubernetes.namespace

        # Create deploy.sh script
        deploy_script = f"""#!/bin/bash
# Kubernetes deployment script for Crown Nexus
# Generated by Crown Nexus Deployment System

set -e  # Exit on any error

echo "=== Crown Nexus Kubernetes Deployment ==="
echo "Started at: $(date)"
echo ""

# Build Docker images
echo "Building Docker images..."
cd {(self.output_dir / "docker").relative_to(self.output_dir)}

# Build frontend image
echo "Building frontend image..."
docker build -t crown-nexus-frontend:latest ./frontend

# Build backend image
echo "Building backend image..."
docker build -t crown-nexus-backend:latest ./backend

# Push images if registry is configured
"""

        # Add registry push if configured
        if cluster.deployment_config.strategy.docker.registry:
            registry = cluster.deployment_config.strategy.docker.registry
            deploy_script += f"""
echo "Pushing images to registry: {registry}..."
docker tag crown-nexus-frontend:latest {registry}/crown-nexus-frontend:latest
docker tag crown-nexus-backend:latest {registry}/crown-nexus-backend:latest
docker push {registry}/crown-nexus-frontend:latest
docker push {registry}/crown-nexus-backend:latest

"""
        else:
            deploy_script += """
echo "Warning: No Docker registry configured. For a multi-node Kubernetes cluster, you need to push images to a registry."
echo "Configure a registry with --docker-registry option and run again."
echo ""

"""

        # Add Kubernetes deployment
        deploy_script += f"""
# Deploy to Kubernetes
echo "Deploying to Kubernetes..."
cd {(self.output_dir).relative_to(self.output_dir)}
kubectl apply -f {k8s_dir.relative_to(self.output_dir)}/deployment.yaml

# Wait for deployment to complete
echo "Waiting for deployment to complete..."
kubectl -n {namespace} rollout status deployment/frontend
kubectl -n {namespace} rollout status deployment/backend

echo ""
echo "=== Deployment completed successfully ==="
echo "Crown Nexus should now be available at:"
echo "  https://{cluster.deployment_config.domain} (if Ingress and DNS are properly configured)"
echo ""
echo "To check the deployment status, run: kubectl -n {namespace} get pods"
echo "To check logs, run: kubectl -n {namespace} logs -l app=backend"
"""

        # Write the script
        deploy_file = self.output_dir / "deploy.sh"
        deploy_file.write_text(deploy_script)

    def _generate_kubernetes_rollback_script(self, cluster: ClusterConfig, k8s_dir: Path) -> None:
        """Generate rollback script for Kubernetes."""
        namespace = cluster.deployment_config.strategy.kubernetes.namespace

        # Create rollback.sh script
        rollback_script = f"""#!/bin/bash
# Kubernetes rollback script for Crown Nexus
# Generated by Crown Nexus Deployment System

set -e  # Exit on any error

echo "=== Crown Nexus Kubernetes Rollback ==="
echo "Started at: $(date)"
echo ""

# Confirm rollback
read -p "WARNING: This will remove all Crown Nexus resources from the Kubernetes cluster. Continue? [y/N] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Rollback aborted."
    exit 1
fi

# Remove Kubernetes resources
echo "Removing Kubernetes resources..."
kubectl delete -f {k8s_dir.relative_to(self.output_dir)}/deployment.yaml

# Ask about namespace
read -p "Do you want to completely remove the '{namespace}' namespace? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing namespace..."
    kubectl delete namespace {namespace}
fi

# Ask about PVCs
read -p "Do you want to delete persistent volume claims (data will be lost)? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing persistent volume claims..."
    kubectl delete pvc --all -n {namespace}
fi

echo ""
echo "=== Rollback completed successfully ==="
"""

        # Write the script
        rollback_file = self.output_dir / "rollback.sh"
        rollback_file.write_text(rollback_script)

    def _set_executable_permissions(self) -> None:
        """Set executable permissions on all generated scripts."""
        for root, _, files in os.walk(self.output_dir):
            for file in files:
                if file.endswith(".sh"):
                    script_path = Path(root) / file
                    script_path.chmod(0o755)
