#!/usr/bin/env python3
"""
Crown Nexus Deployment System
Main entry point for deploying Crown Nexus to any number of servers
based on their hardware specifications and optimal roles.
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import datetime
from pathlib import Path
from typing import List, Optional

import structlog

from models.server import ServerConnection
from models.config import DeploymentConfig, ClusterConfig
from models.deployment import DeploymentState
from models.deployment_strategy import DeploymentStrategy, DeploymentStrategyType
from services.analyzer import PythonServerAnalyzer
from services.script_generator import ScriptGenerator
from utils.security import generate_deployment_credentials
from utils.errors import DeploymentError
from utils.path import normalize_path

# Configure structured logging
logging.basicConfig(level=logging.INFO)
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Initialize logger
logger = structlog.get_logger()


async def analyze_server_cluster(inventory_file: str) -> ClusterConfig:
    """Analyze servers in inventory file and create a cluster configuration."""
    # Read server inventory
    servers = read_server_inventory(inventory_file)
    if not servers:
        raise DeploymentError(f"No servers found in inventory file: {inventory_file}")

    # Analyze servers using Python analyzer
    analyzer = PythonServerAnalyzer()
    cluster = await analyzer.analyze_and_create_cluster(servers)

    return cluster


def read_server_inventory(inventory_file: str) -> List[ServerConnection]:
    """
    Read server inventory from CSV file.

    Args:
        inventory_file: Path to the CSV inventory file

    Returns:
        List of ServerConnection objects

    Raises:
        DeploymentError: If reading the inventory file fails
    """
    import csv

    servers = []
    try:
        with open(inventory_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalize the key path during inventory reading
                normalized_key_path = normalize_path(row['key_path'])
                logger.debug("Normalized SSH key path",
                             original=row['key_path'],
                             normalized=normalized_key_path)

                servers.append(ServerConnection(
                    hostname=row['hostname'],
                    ip=row['ip'],
                    username=row['username'],
                    key_path=normalized_key_path,
                    description=row.get('description', '')
                ))
    except Exception as e:
        logger.error("Error reading inventory file", error=str(e))
        raise DeploymentError(f"Failed to read inventory file: {e}")

    return servers


def generate_deployment_scripts(cluster: ClusterConfig, template_dir: str, output_dir: str) -> None:
    """Generate deployment scripts for the cluster."""
    script_generator = ScriptGenerator(Path(template_dir), Path(output_dir))
    script_generator.generate_all_scripts(cluster)


def setup_arg_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(description='Crown Nexus Deployment System')

    # Define subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze servers and recommend roles')
    analyze_parser.add_argument('--inventory', '-i', required=True, help='Path to server inventory file')
    analyze_parser.add_argument('--output', '-o', help='Path to output analysis file')

    # generate command
    generate_parser = subparsers.add_parser('generate', help='Generate deployment scripts')
    generate_parser.add_argument('--inventory', '-i', required=True, help='Path to server inventory file')
    generate_parser.add_argument('--templates', '-t', required=True, help='Path to template directory')
    generate_parser.add_argument('--output', '-o', required=True, help='Path to output directory')
    generate_parser.add_argument('--domain', '-d', required=True, help='Domain name')
    generate_parser.add_argument('--repo', '-r', required=True, help='Git repository URL')
    generate_parser.add_argument('--branch', '-b', default='main', help='Git branch')
    generate_parser.add_argument('--admin-email', '-e', required=True, help='Admin email')
    generate_parser.add_argument('--strategy', '-s', choices=['traditional', 'docker', 'kubernetes'],
                                 default='traditional', help='Deployment strategy')
    generate_parser.add_argument('--docker-registry', help='Docker registry URL (for container strategies)')
    generate_parser.add_argument('--k8s-namespace', default='crown-nexus',
                                 help='Kubernetes namespace (for kubernetes strategy)')
    generate_parser.add_argument('--storage-class', default='standard',
                                 help='Kubernetes storage class (for kubernetes strategy)')

    # deploy command - placeholder for future implementation
    deploy_parser = subparsers.add_parser('deploy', help='Deploy to servers')
    deploy_parser.add_argument('--scripts', '-s', required=True, help='Path to generated scripts directory')

    return parser


async def main() -> int:
    """Main entry point."""
    parser = setup_arg_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == 'analyze':
            cluster = await analyze_server_cluster(args.inventory)

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

            # Validate roles
            errors = cluster.validate_roles()
            if errors:
                print("\n=== Configuration Warnings ===")
                for error in errors:
                    print(f"- {error}")
                print()

            # Save analysis to file if output specified
            if args.output:
                # Simplified for now - actual implementation would save full analysis
                with open(args.output, 'w') as f:
                    f.write(f"=== Server Analysis Results ===\n")
                    for i, server in enumerate(cluster.servers, 1):
                        roles_str = ", ".join(str(role) for role in server.assigned_roles)
                        f.write(f"Server {i}: {server.hostname} ({server.ip})\n")
                        f.write(f"  - Recommended roles: {roles_str}\n\n")

                print(f"Analysis saved to {args.output}")

            return 0

        elif args.command == 'generate':
            # Analyze servers
            cluster = await analyze_server_cluster(args.inventory)

            # Set up deployment configuration
            deployment_config = DeploymentConfig(
                domain=args.domain,
                repo_url=args.repo,
                git_branch=args.branch,
                admin_email=args.admin_email,
                deployment_timestamp=datetime.datetime.now().isoformat()
            )

            # Configure deployment strategy
            strategy_type = DeploymentStrategyType(args.strategy)
            strategy = DeploymentStrategy(type=strategy_type)

            if strategy_type == DeploymentStrategyType.DOCKER:
                if args.docker_registry:
                    strategy.docker.registry = args.docker_registry

            elif strategy_type == DeploymentStrategyType.KUBERNETES:
                if args.k8s_namespace:
                    strategy.kubernetes.namespace = args.k8s_namespace
                if args.storage_class:
                    strategy.kubernetes.storage_class = args.storage_class
                if args.docker_registry:
                    strategy.docker.registry = args.docker_registry

            deployment_config.strategy = strategy

            # Generate secure credentials
            credentials = generate_deployment_credentials()
            deployment_config.db_password = credentials["db_password"]
            deployment_config.admin_password = credentials["admin_password"]
            deployment_config.redis_password = credentials["redis_password"]
            deployment_config.secret_key = credentials["secret_key"]

            # Update cluster config
            cluster.deployment_config = deployment_config

            # Generate scripts
            generate_deployment_scripts(cluster, args.templates, args.output)

            print(f"\nDeployment scripts generated in {args.output}")
            strategy_name = args.strategy.capitalize()
            print(f"Strategy: {strategy_name}")
            print(f"To deploy, run the deploy.sh script in that directory")

            return 0

        elif args.command == 'deploy':
            # Placeholder for future implementation
            print("Deployment functionality not yet implemented.")
            print(f"Scripts are available in {args.scripts}")
            print("You can run deploy.sh manually to start the deployment")

            return 0

    except DeploymentError as e:
        logger.error("Deployment error", error=str(e))
        print(f"Error: {e}")
        return 1
    except Exception as e:
        logger.exception("Unexpected error", error=str(e))
        print(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
