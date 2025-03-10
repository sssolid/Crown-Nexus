#!/usr/bin/env python3
"""Docker test runner for Crown Nexus deployment system.

This script tests the Crown Nexus deployment system in a Docker environment.
It includes improved error handling and debugging capabilities.
"""
from __future__ import annotations

import os
import time
import asyncio
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any

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

    # Make sure the key has the right permissions
    try:
        os.chmod(key_path, 0o600)
        logger.info(f"Set permissions on SSH key", key_path=key_path)
    except Exception as e:
        logger.error(f"Failed to set permissions on SSH key", key_path=key_path, error=str(e))

    while time.time() - start_time < timeout:
        try:
            # First try a simple ssh command to check connectivity
            cmd = f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -i {key_path} {username}@{ip} echo 'SSH connection successful'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info("SSH connection successful via subprocess", ip=ip, port=port)
                return True

            # If subprocess approach fails, try asyncssh
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
                    logger.info("SSH connection successful via asyncssh", ip=ip, port=port)
                    return True
        except (asyncssh.Error, OSError, subprocess.SubprocessError) as e:
            logger.debug("SSH connection failed, retrying...", ip=ip, error=str(e))

            # Run some diagnostic commands
            try:
                # Try to list the SSH process in the container
                container_name = f"crown-test-server{ip.split('.')[-1] - 9}"
                ps_cmd = f"docker exec {container_name} ps aux | grep sshd"
                ps_result = subprocess.run(ps_cmd, shell=True, capture_output=True, text=True)
                logger.debug("SSH process status",
                             container=container_name,
                             stdout=ps_result.stdout.strip())

                # Check if authorized_keys exists
                key_cmd = f"docker exec {container_name} ls -la /home/crown_test/.ssh"
                key_result = subprocess.run(key_cmd, shell=True, capture_output=True, text=True)
                logger.debug("SSH key status",
                             container=container_name,
                             stdout=key_result.stdout.strip())
            except Exception as e:
                logger.debug("Failed to run diagnostics", error=str(e))

            await asyncio.sleep(2)

    logger.error("Timed out waiting for SSH", ip=ip, timeout=timeout)
    return False


async def ensure_ssh_access(containers: List[str], username: str, key_path: str) -> bool:
    """
    Ensure SSH access to each container.

    Args:
        containers: List of container names
        username: SSH username
        key_path: Path to SSH private key

    Returns:
        True if all servers are accessible, False otherwise
    """
    logger.info("Ensuring SSH access to containers")

    # Make sure the key exists and has correct permissions
    if not os.path.exists(key_path):
        logger.error("SSH key not found", key_path=key_path)

        # Generate a new key
        key_dir = os.path.dirname(key_path)
        os.makedirs(key_dir, exist_ok=True)

        ssh_keygen_cmd = f"ssh-keygen -t rsa -b 2048 -f {key_path} -N ''"
        result = subprocess.run(ssh_keygen_cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error("Failed to generate SSH key", error=result.stderr)
            return False

        logger.info("Generated new SSH key", key_path=key_path)

    # Ensure key has correct permissions
    os.chmod(key_path, 0o600)

    # Get the public key
    public_key = ""
    with open(f"{key_path}.pub", "r") as f:
        public_key = f.read().strip()

    all_ok = True

    # Ensure each container has the key
    for container in containers:
        try:
            # Create .ssh directory if needed
            mkdir_cmd = f"docker exec {container} bash -c 'mkdir -p /home/{username}/.ssh && chmod 700 /home/{username}/.ssh'"
            subprocess.run(mkdir_cmd, shell=True, check=True)

            # Add the key
            key_cmd = f"docker exec {container} bash -c 'echo \"{public_key}\" > /home/{username}/.ssh/authorized_keys && chmod 600 /home/{username}/.ssh/authorized_keys && chown -R {username}:{username} /home/{username}/.ssh'"
            subprocess.run(key_cmd, shell=True, check=True)

            logger.info("Added SSH key to container", container=container)
        except subprocess.SubprocessError as e:
            logger.error("Failed to add SSH key to container", container=container, error=str(e))
            all_ok = False

    return all_ok


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

    # Add debugging info to the function logs
    logger.info("SSH configuration",
                user=ssh_user,
                key_path=ssh_key_path,
                key_exists=os.path.exists(ssh_key_path),
                key_perms=oct(os.stat(ssh_key_path).st_mode)[-3:] if os.path.exists(ssh_key_path) else "N/A")

    # Ensure SSH access to all containers
    containers = [f"crown-test-server{i}" for i in range(1, server_count + 1)]
    ssh_ok = await ensure_ssh_access(containers, ssh_user, ssh_key_path)

    if not ssh_ok:
        logger.warning("Failed to ensure SSH access to all containers")

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


async def run_with_retries(cmd: str, cwd: str = None, max_retries: int = 3) -> Tuple[int, str, str]:
    """
    Run a command with retries.

    Args:
        cmd: Command to run
        cwd: Working directory
        max_retries: Maximum number of retries

    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    for attempt in range(max_retries):
        try:
            logger.info(f"Running command (attempt {attempt+1}/{max_retries})", cmd=cmd, cwd=cwd)
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )

            stdout, stderr = await process.communicate()

            stdout_str = stdout.decode() if stdout else ""
            stderr_str = stderr.decode() if stderr else ""

            logger.info(f"Command completed",
                        cmd=cmd,
                        return_code=process.returncode,
                        stdout_preview=stdout_str[:200] + "..." if len(stdout_str) > 200 else stdout_str)

            if process.returncode == 0:
                return process.returncode, stdout_str, stderr_str

            logger.warning(f"Command failed, retrying...",
                           cmd=cmd,
                           return_code=process.returncode,
                           stderr=stderr_str)
        except Exception as e:
            logger.error(f"Exception running command", cmd=cmd, error=str(e))

        # Only retry if not the last attempt
        if attempt < max_retries - 1:
            # Exponential backoff
            await asyncio.sleep(2 ** attempt)

    # If we get here, all attempts failed
    return 1, "", f"Failed after {max_retries} attempts"


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
            repo_url="https://github.com/example/crown-nexus.git",
            git_branch="main",
            admin_email="admin@example.com"
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

        # Clean output directory if it exists
        if output_dir.exists():
            shutil.rmtree(output_dir)

        output_dir.mkdir(exist_ok=True, parents=True)

        script_generator = ScriptGenerator(template_dir, output_dir)
        script_generator.generate_all_scripts(cluster)

        logger.info("Deployment scripts generated", output_dir=str(output_dir))

        # Fix permissions on deploy.sh
        deploy_script = output_dir / "deploy.sh"
        os.chmod(deploy_script, 0o755)

        # Fix permissions on all .sh files
        for script in output_dir.glob("**/*.sh"):
            os.chmod(script, 0o755)
            logger.debug(f"Set executable permissions on {script}")

        # Run deployment script if TEST_MODE is not "generate_only"
        if os.environ.get("TEST_MODE", "").lower() != "generate_only":
            # Create a simple helper script to see what's happening
            helper_script = output_dir / "run_deploy.sh"
            with open(helper_script, "w") as f:
                f.write("""#!/bin/bash
set -x  # Enable command echo
cd $(dirname $0)
./deploy.sh
""")
            os.chmod(helper_script, 0o755)

            # Run deployment with advanced error handling
            logger.info("Starting deployment")

            # First try the helper script
            return_code, stdout, stderr = await run_with_retries(
                str(helper_script),
                cwd=str(output_dir)
            )

            if return_code == 0:
                logger.info("Deployment successful")

                # Verify deployment
                deployment_verified = await verify_deployment(cluster)

                if deployment_verified:
                    logger.info("Deployment verification passed")
                    return 0
                else:
                    logger.error("Deployment verification failed")
                    return 1
            else:
                logger.error("Deployment failed",
                             returncode=return_code,
                             stdout=stdout,
                             stderr=stderr)
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
