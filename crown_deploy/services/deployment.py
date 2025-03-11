"""Deployment service for the Crown Nexus deployment system."""
from __future__ import annotations

import asyncio
import subprocess
import shlex
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set, Any

import structlog
import asyncssh
from pydantic import BaseModel

from models.server import Server, ServerConnection, ServerRole
from models.config import ClusterConfig
from models.deployment import DeploymentState, ServerDeploymentStatus
from utils.errors import DeploymentError, RollbackError
from utils.path import normalize_path, get_ssh_key_path

# Initialize logger
logger = structlog.get_logger()


class DeploymentService:
    """Service to handle deployment and rollback operations."""

    def __init__(self, scripts_dir: Path, state_dir: Optional[Path] = None):
        """
        Initialize the deployment service.

        Args:
            scripts_dir: Directory containing the generated deployment scripts
            state_dir: Directory to store deployment state (defaults to scripts_dir/state)
        """
        self.scripts_dir = Path(scripts_dir)
        self.state_dir = Path(state_dir) if state_dir else self.scripts_dir / "state"
        self.state_dir.mkdir(parents=True, exist_ok=True)

    async def deploy(self, cluster: ClusterConfig) -> DeploymentState:
        """
        Deploy Crown Nexus to the cluster.

        Args:
            cluster: The cluster configuration

        Returns:
            The final deployment state

        Raises:
            DeploymentError: If deployment fails
        """
        # Create deployment state
        state = DeploymentState(
            deployment_id=cluster.deployment_config.deployment_id,
            cluster_config=cluster,
            status="in_progress",
            start_time=datetime.now().isoformat(),
            server_statuses={
                server.hostname: ServerDeploymentStatus(hostname=server.hostname)
                for server in cluster.servers
            }
        )

        # Save initial state
        state.save(self.state_dir)

        try:
            # Run the deployment script
            deploy_script = self.scripts_dir / "deploy.sh"
            if not deploy_script.exists():
                raise DeploymentError(f"Deployment script not found: {deploy_script}")

            logger.info("Starting deployment", script=str(deploy_script))

            # Make sure the script is executable
            deploy_script.chmod(0o755)

            # Run the deployment script
            process = subprocess.Popen(
                [str(deploy_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.scripts_dir)
            )

            # Process output in real-time
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                logger.error("Deployment failed",
                             return_code=process.returncode,
                             stderr=stderr)

                # Update state
                state.status = "failed"
                state.error_message = f"Deployment script failed with code {process.returncode}: {stderr}"
                state.end_time = datetime.now().isoformat()
                state.save(self.state_dir)

                raise DeploymentError(
                    f"Deployment script failed with code {process.returncode}: {stderr}"
                )

            # Update state
            state.status = "completed"
            state.end_time = datetime.now().isoformat()
            state.save(self.state_dir)

            logger.info("Deployment completed successfully")
            return state

        except Exception as e:
            logger.exception("Deployment failed", error=str(e))

            # Update state
            state.status = "failed"
            state.error_message = str(e)
            state.end_time = datetime.now().isoformat()
            state.save(self.state_dir)

            raise DeploymentError(f"Deployment failed: {e}")

    async def rollback(self, deployment_id: str) -> DeploymentState:
        """
        Rollback a deployment.

        Args:
            deployment_id: The ID of the deployment to roll back

        Returns:
            The updated deployment state

        Raises:
            RollbackError: If rollback fails
        """
        # Load deployment state
        state = DeploymentState.load(deployment_id, self.state_dir)
        if not state:
            raise RollbackError(f"Deployment state not found: {deployment_id}")

        try:
            # Run the rollback script
            rollback_script = self.scripts_dir / "rollback.sh"
            if not rollback_script.exists():
                raise RollbackError(f"Rollback script not found: {rollback_script}")

            logger.info("Starting rollback",
                        deployment_id=deployment_id,
                        script=str(rollback_script))

            # Make sure the script is executable
            rollback_script.chmod(0o755)

            # Run the rollback script
            process = subprocess.Popen(
                [str(rollback_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.scripts_dir)
            )

            # Process output in real-time
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                logger.error("Rollback failed",
                             return_code=process.returncode,
                             stderr=stderr)

                # Update state
                state.error_message = f"Rollback script failed with code {process.returncode}: {stderr}"
                state.save(self.state_dir)

                raise RollbackError(
                    f"Rollback script failed with code {process.returncode}: {stderr}"
                )

            # Update state
            state.status = "rolled_back"
            state.end_time = datetime.now().isoformat()
            state.save(self.state_dir)

            logger.info("Rollback completed successfully")
            return state

        except Exception as e:
            logger.exception("Rollback failed", error=str(e))

            # Update state if possible
            if state:
                state.error_message = f"Rollback failed: {e}"
                state.save(self.state_dir)

            raise RollbackError(f"Rollback failed: {e}")

    @staticmethod
    async def check_server_status(connection: ServerConnection) -> Dict[str, Any]:
        """
        Check the status of a server.

        Args:
            connection: Connection details for the server

        Returns:
            Server status information

        Raises:
            ServerConnectionError: If connection fails
        """
        try:
            # Normalize SSH key path
            normalized_key_path = get_ssh_key_path(connection.key_path)

            # Connect to the server
            async with asyncssh.connect(
                connection.ip,
                username=connection.username,
                client_keys=[normalized_key_path],
                known_hosts=None
            ) as ssh:
                # Run status command
                status_cmd = "if [ -f /home/crown/monitor.sh ]; then /home/crown/monitor.sh; else echo 'Monitoring script not found'; fi"
                result = await ssh.run(status_cmd)

                # Get installed services
                services_cmd = "systemctl list-units --type=service --state=running | grep -E 'crown|nginx|postgresql|redis|elasticsearch'"
                services_result = await ssh.run(services_cmd)

                return {
                    "hostname": connection.hostname,
                    "ip": connection.ip,
                    "status": "online",
                    "monitoring_output": result.stdout,
                    "services": services_result.stdout.splitlines() if services_result.exit_status == 0 else []
                }

        except Exception as e:
            logger.error("Server status check failed",
                         hostname=connection.hostname,
                         error=str(e))

            return {
                "hostname": connection.hostname,
                "ip": connection.ip,
                "status": "offline",
                "error": str(e)
            }
