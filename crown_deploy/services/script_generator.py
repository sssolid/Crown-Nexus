"""Script generator service for the Crown Nexus deployment system."""
from __future__ import annotations

import os
import jinja2
from pathlib import Path
from typing import Dict, Any, List, Set

import structlog

from crown_deploy.models.server import Server, ServerRole
from crown_deploy.models.config import ClusterConfig
from crown_deploy.utils.errors import ScriptGenerationError

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

    def generate_all_scripts(self, cluster: ClusterConfig) -> None:
        """Generate all deployment scripts for the cluster."""
        logger.info("Generating deployment scripts")

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

        # Set executable permissions
        self._set_executable_permissions()

        logger.info("Deployment scripts generated",
                    output_dir=str(self.output_dir))

    def _generate_env_file(self, cluster: ClusterConfig) -> None:
        """Generate the common environment file with deployment variables."""
        template = self.jinja_env.get_template("common/env.sh.j2")

        # Prepare context for template rendering
        context = {
            "config": cluster.deployment_config,
            "servers": cluster.servers,
            "server_roles": [(i, server, server.assigned_roles)
                             for i, server in enumerate(cluster.servers, 1)]
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
        }

        # Create output file
        setup_file = self.output_dir / f"server{server_index}" / "setup.sh"
        setup_file.write_text(template.render(**context))

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
        deploy_file.write_text(template.render(**context))

        logger.info("Generated main deployment script", file=str(deploy_file))

    def _generate_rollback_scripts(self, cluster: ClusterConfig) -> None:
        """Generate rollback scripts for each server."""
        # Generate a master rollback script that calls individual server rollbacks
        rollback_file = self.output_dir / "rollback.sh"

        content = "#!/bin/bash\n\n"
        content += "# Master rollback script for Crown Nexus deployment\n\n"
        content += "echo \"=== Rolling back Crown Nexus deployment ===\"\n\n"

        for i, server in enumerate(cluster.servers, 1):
            content += f"echo \"Rolling back server {i}: {server.hostname}\"\n"
            content += f"ssh ubuntu@{server.ip} 'bash -s' < server{i}/rollback.sh\n\n"

        content += "echo \"=== Rollback completed ===\"\n"

        rollback_file.write_text(content)

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

    def _set_executable_permissions(self) -> None:
        """Set executable permissions on all generated scripts."""
        for root, _, files in os.walk(self.output_dir):
            for file in files:
                if file.endswith(".sh"):
                    script_path = Path(root) / file
                    script_path.chmod(0o755)
