"""Deployment state models for the Crown Nexus deployment system."""
from __future__ import annotations

import json
import os
from typing import Dict, List, Literal, Optional, Any
from pathlib import Path
from pydantic import BaseModel, Field

from models.config import ClusterConfig


class ServerDeploymentStatus(BaseModel):
    """Status of deployment for a single server."""
    hostname: str
    status: Literal["pending", "in_progress", "completed", "failed"] = "pending"
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    error_message: Optional[str] = None
    installed_packages: List[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


class DeploymentState(BaseModel):
    """Model representing the state of a deployment."""
    deployment_id: str
    cluster_config: ClusterConfig
    status: Literal["pending", "in_progress", "completed", "failed", "rolled_back"] = "pending"
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    error_message: Optional[str] = None
    server_statuses: Dict[str, ServerDeploymentStatus] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    def save(self, state_dir: Path) -> None:
        """Save the deployment state to a file."""
        state_dir.mkdir(parents=True, exist_ok=True)
        state_file = state_dir / f"{self.deployment_id}.json"

        # Convert to dict and handle non-serializable types
        state_dict = self.dict(exclude={"cluster_config"})

        # Save cluster config separately (simpler version)
        cluster_dict = {
            "servers": [
                {
                    "hostname": server.hostname,
                    "ip": server.ip,
                    "roles": [str(role) for role in server.assigned_roles]
                }
                for server in self.cluster_config.servers
            ],
            "deployment_config": self.cluster_config.deployment_config.dict(
                exclude={"db_password", "admin_password", "redis_password", "secret_key"}
            )
        }

        state_dict["cluster_config"] = cluster_dict

        with open(state_file, "w") as f:
            json.dump(state_dict, f, indent=2)

    @classmethod
    def load(cls, deployment_id: str, state_dir: Path) -> Optional[DeploymentState]:
        """Load a deployment state from a file."""
        state_file = state_dir / f"{deployment_id}.json"
        if not state_file.exists():
            return None

        with open(state_file, "r") as f:
            state_dict = json.load(f)

        # This is a simplified version - in a real implementation you would
        # need to convert the loaded data back to proper model instances
        return cls(**state_dict)
