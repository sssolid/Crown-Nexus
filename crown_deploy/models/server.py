"""Server and role models for the Crown Nexus deployment system."""
from __future__ import annotations

from enum import Enum
from typing import Literal, Optional, Set, List
from pydantic import BaseModel, Field


class ServerRole(str, Enum):
    """Possible roles a server can have in the cluster."""
    LOAD_BALANCER = "load_balancer"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    ELASTICSEARCH = "elasticsearch"
    REDIS = "redis"
    MONITORING = "monitoring"
    CI_CD = "ci_cd"
    STORAGE = "storage"

    def __str__(self) -> str:
        """Return the string representation of the role."""
        return self.value

    @classmethod
    def all_roles(cls) -> Set[ServerRole]:
        """Return all available roles."""
        return set(cls)


class ServerSpecs(BaseModel):
    """Model representing server hardware specifications."""
    hostname: str
    ip: str
    cpu_cores: int
    cpu_model: str = ""
    memory_gb: int
    disk_gb: int
    disk_type: Literal["SSD", "HDD", "NVMe", "Unknown"] = "Unknown"
    os_info: str = ""

    class Config:
        extra = "forbid"


class ServerConnection(BaseModel):
    """Model representing server connection details."""
    hostname: str
    ip: str
    username: str
    key_path: str
    description: str = ""

    class Config:
        extra = "forbid"


class Server(BaseModel):
    """Model representing a server with its specs and assigned roles."""
    connection: ServerConnection
    specs: Optional[ServerSpecs] = None
    assigned_roles: Set[ServerRole] = Field(default_factory=set)
    installed_packages: Set[str] = Field(default_factory=set)

    class Config:
        arbitrary_types_allowed = True

    @property
    def hostname(self) -> str:
        """Return the server hostname."""
        return self.connection.hostname

    @property
    def ip(self) -> str:
        """Return the server IP address."""
        return self.connection.ip


def get_role_dependencies(role: ServerRole) -> List[ServerRole]:
    """Return the list of roles that the given role depends on."""
    dependencies = {
        ServerRole.FRONTEND: [ServerRole.BACKEND],
        ServerRole.BACKEND: [ServerRole.DATABASE],
        # Add other dependencies as needed
    }

    return dependencies.get(role, [])


def get_incompatible_roles(role: ServerRole) -> List[ServerRole]:
    """Return the list of roles that are incompatible with the given role."""
    incompatible = {
        ServerRole.DATABASE: [ServerRole.CI_CD],  # Database and CI/CD might contend for resources
        # Add other incompatibilities as needed
    }

    return incompatible.get(role, [])
