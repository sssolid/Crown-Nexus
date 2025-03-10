"""Docker test runner for Crown Nexus deployment system."""
from __future__ import annotations

import os
import time
import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

import structlog
import asyncssh

from crown_deploy.models.server import ServerConnection
from crown_deploy.models.config import DeploymentConfig
from crown_deploy.services.analyzer import PythonServerAnalyzer
from crown_deploy.services.script_generator import ScriptGenerator
from crown_deploy.utils.security import generate_deployment_credentials

# Initialize logger
logger = structlog.get_logger()


async def wait_for_ssh(ip: str, port: int = 22, username: str = "crown_test",
                       key_path: str = "/root/.ssh/id_rsa", timeout: int = 60) -> bool:
    """
    Wait for SSH to become available on a server.

    Args:
        ip: IP address of the server
        port: SSH port
        username: SSH username
        key_path: Path to SSH private key
        timeout: Maximum time to wait in seconds

    Returns:
        True if SSH is available, False otherwise
    """
    logger.info("Waiting for SSH", ip=ip, port=port)
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            async with asyncssh.connect(
                ip,
                port=port,
                username=username,
                client_keys=[key_path],
                known_hosts=None,
                connect_timeout=5
            ) as conn:
                result = await conn.run("echo 'SSH connection successful'")
                if result.exit_status == 0:
                    logger.info("SSH connection successful", ip=ip, port=port)
                    return True
        except (asyncssh.Error, OSError) as e:
            logger.debug("SSH connection failed, retrying...", ip=ip, error=str(e))
            await asyncio.sleep(2)

    logger.error("Timed out waiting for SSH", ip=ip, timeout=timeout)
    return False


async def get_server_connections() -> List[ServerConnection]:
    """
    Get server connections from environment variables or defaults.

    Returns:
        List of ServerConnection objects
    """
    servers = []

    # Get server info from environment or use defaults
    server_count = int(os.environ.get("SERVER_COUNT", "3"))
    ssh_user = os.environ.get("SSH_USER", "crown_test")
    ssh_key_path = os.environ.get("SSH_KEY_PATH", "/root/.ssh/id_rsa")

    for i in range(1, server_count + 1):
        ip_env_var = f"SERVER{i}_IP"
        port_env_var = f"SERVER{i}_PORT"
        hostname_env_var = f"SERVER{i}_HOSTNAME"

        ip = os.environ.get(ip_env_var, f"172.28.1.{9+i}")
        port = int(os.environ.get(port_env_var, "22"))
        hostname = os.environ.get(hostname_env_var, f"server{i}")

        # Wait for SSH to be available
        if await wait_for_ssh(ip, port, ssh_user, ssh_key_path):
            servers.append(
                ServerConnection(
                    hostname=hostname,
                    ip=ip,
                    username=ssh_user,
                    key_path=ssh_key_path,
                    description=f"Docker test server {i}"
                )
            )
        else:
            logger.error("Could not connect to server", hostname=hostname, ip=ip)

    return servers


async def main() -> int:
    """
    Main test runner function.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        logger.info("Starting Docker test runner")

        # Get server connections
        servers = await get_server_connections()
        if not servers:
            logger.error("No servers available")
            return 1

        logger.info("Connected to servers", count=len(servers))

        # Create deployment config
        deployment_config = DeploymentConfig(
            domain="crown-test.local",
            repo_url="https://github.com/sssolid/crown-nexus.git",
            git_branch="main",
            admin_email="ryans@crownautomotive.net"
        )

        # Generate secure credentials
        credentials = generate_deployment_credentials()
        deployment_config.db_password = credentials["db_password"]
        deployment_config.admin_password = credentials["admin_password"]
        deployment_config.redis_password = credentials["redis_password"]
        deployment_config.secret_key = credentials["secret_key"]

        # Analyze servers
        analyzer = PythonServerAnalyzer()
        cluster = await analyzer.analyze_and_create_cluster(servers)

        # Update cluster config
        cluster.deployment_config = deployment_config

        # Print analysis results
        logger.info("Server analysis complete")
        for i, server in enumerate(cluster.servers, 1):
            roles_str = ", ".join(str(role) for role in server.assigned_roles)
            logger.info(f"Server {i}: {server.hostname} ({server.ip})",
                        roles=roles_str)

        # Generate deployment scripts
        output_dir = Path("/app/test-deployment")
        template_dir = Path("/app/crown_deploy/templates")

        output_dir.mkdir(exist_ok=True, parents=True)

        script_generator = ScriptGenerator(template_dir, output_dir)
        script_generator.generate_all_scripts(cluster)

        logger.info("Deployment scripts generated", output_dir=str(output_dir))

        # Run deployment script if TEST_MODE is not "generate_only"
        if os.environ.get("TEST_MODE", "").lower() != "generate_only":
            deploy_script = output_dir / "deploy.sh"

            # Make deploy script executable
            os.chmod(deploy_script, 0o755)

            # Run deployment
            logger.info("Starting deployment")
            result = subprocess.run(
                [str(deploy_script)],
                cwd=str(output_dir),
                text=True,
                capture_output=True
            )

            if result.returncode == 0:
                logger.info("Deployment successful")

                # Verify deployment
                await verify_deployment(cluster)

                return 0
            else:
                logger.error("Deployment failed",
                             returncode=result.returncode,
                             stdout=result.stdout,
                             stderr=result.stderr)
                return 1
        else:
            logger.info("Skipping deployment execution (generate_only mode)")
            return 0

    except Exception as e:
        logger.exception("Test runner failed", error=str(e))
        return 1


async def verify_deployment(cluster) -> bool:
    """
    Verify that the deployment was successful.

    Args:
        cluster: The cluster configuration

    Returns:
        True if verification passed, False otherwise
    """
    logger.info("Verifying deployment")

    # Check each server for expected services
    all_passed = True

    for server in cluster.servers:
        logger.info("Checking server", hostname=server.hostname, ip=server.ip)

        try:
            async with asyncssh.connect(
                server.ip,
                username=server.connection.username,
                client_keys=[server.connection.key_path],
                known_hosts=None
            ) as conn:
                # Check if crown-nexus directory exists
                result = await conn.run("test -d /home/crown/crown-nexus && echo 'exists'")
                if result.stdout.strip() != 'exists':
                    logger.error("Crown Nexus directory not found", hostname=server.hostname)
                    all_passed = False

                # Check services based on server roles
                for role in server.assigned_roles:
                    logger.info("Checking role", hostname=server.hostname, role=str(role))

                    # Define commands to check for each role
                    role_checks = {
                        'frontend': "systemctl is-active nginx",
                        'backend': "systemctl is-active crown-nexus",
                        'database': "systemctl is-active postgresql",
                        'redis': "systemctl is-active redis-server",
                        'elasticsearch': "systemctl is-active elasticsearch",
                        'load_balancer': "systemctl is-active nginx",
                        'monitoring': "systemctl is-active prometheus",
                    }

                    if str(role) in role_checks:
                        try:
                            result = await conn.run(role_checks[str(role)])
                            if result.exit_status != 0:
                                logger.error("Service check failed",
                                             hostname=server.hostname,
                                             role=str(role),
                                             output=result.stdout)
                                all_passed = False
                        except Exception as e:
                            logger.error("Service check error",
                                         hostname=server.hostname,
                                         role=str(role),
                                         error=str(e))
                            all_passed = False

        except Exception as e:
            logger.error("Failed to connect to server",
                         hostname=server.hostname,
                         error=str(e))
            all_passed = False

    if all_passed:
        logger.info("Deployment verification passed")
    else:
        logger.error("Deployment verification failed")

    return all_passed


if __name__ == "__main__":
    asyncio.run(main())
