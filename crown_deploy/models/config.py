"""Configuration models for the Crown Nexus deployment system."""
from __future__ import annotations

import uuid
from typing import List, Set, Optional, Dict
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, validator

from models.server import Server, ServerRole
from models.deployment_strategy import DeploymentStrategy


class DeploymentConfig(BaseModel):
    """Model representing the overall deployment configuration."""
    app_name: str = "crown-nexus"
    domain: str = ""
    repo_url: str = ""
    git_branch: str = "main"
    admin_email: str = ""
    admin_name: str = "Admin User"
    timezone: str = "UTC"

    # Database settings
    db_name: str = "crown_nexus"
    db_user: str = "crown_user"
    db_password: str = ""

    # Security
    admin_password: str = ""
    redis_password: str = ""
    secret_key: str = ""

    # Deployment strategy
    strategy: DeploymentStrategy = Field(default_factory=DeploymentStrategy)

    # Generated during deployment
    deployment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    deployment_timestamp: str = ""

    class Config:
        extra = "forbid"

    @validator("timezone")
    def validate_timezone(cls, v: str) -> str:
        """Validate that the timezone is valid."""
        try:
            ZoneInfo(v)
            return v
        except Exception as e:
            raise ValueError(f"Invalid timezone: {v}") from e


class ClusterConfig(BaseModel):
    """Model representing the cluster configuration with all servers."""
    servers: List[Server] = Field(default_factory=list)
    deployment_config: DeploymentConfig = Field(default_factory=DeploymentConfig)

    class Config:
        arbitrary_types_allowed = True

    def get_servers_by_role(self, role: ServerRole) -> List[Server]:
        """Get all servers with the specified role."""
        return [s for s in self.servers if role in s.assigned_roles]

    def validate_roles(self) -> List[str]:
        """Validate that all required roles are assigned and compatible."""
        errors: List[str] = []

        # Check if essential roles are assigned
        for essential_role in {ServerRole.DATABASE, ServerRole.BACKEND, ServerRole.FRONTEND}:
            if not self.get_servers_by_role(essential_role):
                errors.append(f"No server assigned the essential role: {essential_role}")

        # Check for role compatibility issues
        for server in self.servers:
            roles = server.assigned_roles

            # Check incompatible role combinations
            if ServerRole.DATABASE in roles and ServerRole.CI_CD in roles:
                errors.append(f"Server {server.hostname}: Database and CI/CD roles might contend for resources")

            # Check if a server has too many roles
            if len(roles) > 3:
                errors.append(f"Server {server.hostname}: Has too many roles ({len(roles)}), which may impact performance")

        return errors

    def get_server_index(self, hostname: str) -> Optional[int]:
        """Get the index of a server by hostname."""
        for i, server in enumerate(self.servers, 1):
            if server.hostname == hostname:
                return i
        return None

    def get_server_by_hostname(self, hostname: str) -> Optional[Server]:
        """Get a server by hostname."""
        for server in self.servers:
            if server.hostname == hostname:
                return server
        return None
