#!/usr/bin/env python3
"""
Quick start script for Crown Nexus deployment.

This script demonstrates how to use the Crown Nexus Deployment System
to quickly analyze your servers and deploy Crown Nexus.
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the crown_deploy package
sys.path.insert(0, str(Path(__file__).parent.parent))

from crown_deploy.models.server import ServerConnection
from crown_deploy.models.config import DeploymentConfig
from crown_deploy.services.analyzer import PythonServerAnalyzer
from crown_deploy.services.script_generator import ScriptGenerator
from crown_deploy.utils.security import generate_deployment_credentials


async def main():
    """Run a quick deployment of Crown Nexus."""
    # Configuration
    domain = input("Enter your domain name (e.g., crown-nexus.com): ")
    repo_url = input("Enter the Git repository URL: ")
    git_branch = input("Enter the Git branch [main]: ") or "main"
    admin_email = input("Enter admin email: ")

    # Define your servers
    print("\nEnter details for your servers:")
    servers = []
    add_more = True

    while add_more:
        hostname = input("Server hostname: ")
        ip = input(f"IP for {hostname}: ")
        username = input(f"SSH username for {hostname} [ubuntu]: ") or "ubuntu"
        key_path = input(f"SSH key path for {hostname} [~/.ssh/id_rsa]: ") or "~/.ssh/id_rsa"
        description = input(f"Description for {hostname} []: ") or ""

        servers.append(ServerConnection(
            hostname=hostname,
            ip=ip,
            username=username,
            key_path=os.path.expanduser(key_path),
            description=description
        ))

        more = input("Add another server? [y/N]: ")
        add_more = more.lower() == 'y'

    # Analyze servers
    print("\nAnalyzing servers...")
    analyzer = PythonServerAnalyzer()
    cluster = await analyzer.analyze_and_create_cluster(servers)

    # Print analysis results
    print("\n=== Server Analysis Results ===")
    for i, server in enumerate(cluster.servers, 1):
        roles_str = ", ".join(str(role) for role in server.assigned_roles)
        print(f"Server {i}: {server.hostname} ({server.ip})")
        if server.specs:
            print(f"  - CPU: {server.specs.cpu_cores} cores, {server.specs.cpu_model}")
            print(f"  - Memory: {server.specs.memory_gb} GB")
            print(f"  - Disk: {server.specs.disk_gb} GB, {server.specs.disk_type}")
            print(f"  - OS: {server.specs.os_info}")
        print(f"  - Recommended roles: {roles_str}")
        print()

    # Check for any role assignment issues
    errors = cluster.validate_roles()
    if errors:
        print("\n=== Configuration Warnings ===")
        for error in errors:
            print(f"- {error}")
        print()

    # Confirm deployment
    proceed = input("\nProceed with deployment using these role assignments? [y/N]: ")
    if proceed.lower() != 'y':
        print("Deployment canceled.")
        return

    # Set up deployment configuration
    deployment_config = DeploymentConfig(
        domain=domain,
        repo_url=repo_url,
        git_branch=git_branch,
        admin_email=admin_email
    )

    # Generate secure credentials
    print("Generating secure credentials...")
    credentials = generate_deployment_credentials()
    deployment_config.db_password = credentials["db_password"]
    deployment_config.admin_password = credentials["admin_password"]
    deployment_config.redis_password = credentials["redis_password"]
    deployment_config.secret_key = credentials["secret_key"]

    # Update cluster config
    cluster.deployment_config = deployment_config

    # Generate deployment scripts
    output_dir = input("\nEnter path for deployment scripts [./deployment]: ") or "./deployment"
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "crown_deploy/templates")

    print(f"\nGenerating deployment scripts in {output_dir}...")
    script_generator = ScriptGenerator(Path(template_dir), Path(output_dir))
    script_generator.generate_all_scripts(cluster)

    print(f"\nDeployment scripts generated in {output_dir}")
    print("To deploy, run the following command:")
    print(f"  cd {output_dir} && ./deploy.sh")

    # Print credentials
    print("\nCredentials (saved in crown-credentials.txt):")
    print(f"  Admin Email: {admin_email}")
    print(f"  Admin Password: {deployment_config.admin_password}")
    print("  Database Password: ********")
    print("  Redis Password: ********")
    print("  Secret Key: ********")


if __name__ == "__main__":
    asyncio.run(main())
