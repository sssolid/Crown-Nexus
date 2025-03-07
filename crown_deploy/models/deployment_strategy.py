"""Deployment strategy models for the Crown Nexus deployment system."""
from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional, Set, Literal, Any
from pydantic import BaseModel, Field, validator


class DeploymentStrategyType(str, Enum):
    """Available deployment strategies."""
    TRADITIONAL = "traditional"  # Direct installation on servers
    DOCKER = "docker"            # Docker and docker-compose
    KUBERNETES = "kubernetes"    # Kubernetes cluster


class DockerConfig(BaseModel):
    """Docker-specific deployment configuration."""
    compose_version: str = "3.8"
    registry: Optional[str] = None  # Docker registry URL (if used)
    use_volumes: bool = True        # Use Docker volumes for persistence
    network_mode: Literal["bridge", "host", "none"] = "bridge"
    restart_policy: Literal["no", "always", "on-failure", "unless-stopped"] = "unless-stopped"

    # Docker Swarm options
    use_swarm: bool = False
    replicas: Dict[str, int] = Field(default_factory=lambda: {
        "frontend": 2,
        "backend": 2,
        "database": 1,
        "redis": 1,
        "elasticsearch": 1
    })

    class Config:
        extra = "forbid"


class KubernetesConfig(BaseModel):
    """Kubernetes-specific deployment configuration."""
    namespace: str = "crown-nexus"
    storage_class: str = "standard"
    ingress_class: str = "nginx"
    use_service_mesh: bool = False  # Whether to use service mesh (e.g., Istio)

    # Resources for each component
    resources: Dict[str, Dict[str, Dict[str, str]]] = Field(default_factory=lambda: {
        "frontend": {
            "requests": {"cpu": "100m", "memory": "128Mi"},
            "limits": {"cpu": "300m", "memory": "256Mi"}
        },
        "backend": {
            "requests": {"cpu": "200m", "memory": "256Mi"},
            "limits": {"cpu": "500m", "memory": "512Mi"}
        },
        "database": {
            "requests": {"cpu": "500m", "memory": "1Gi"},
            "limits": {"cpu": "1", "memory": "2Gi"}
        },
        "redis": {
            "requests": {"cpu": "100m", "memory": "128Mi"},
            "limits": {"cpu": "300m", "memory": "256Mi"}
        },
        "elasticsearch": {
            "requests": {"cpu": "500m", "memory": "1Gi"},
            "limits": {"cpu": "1", "memory": "2Gi"}
        }
    })

    # Replicas for each component
    replicas: Dict[str, int] = Field(default_factory=lambda: {
        "frontend": 2,
        "backend": 2,
        "database": 1,
        "redis": 1,
        "elasticsearch": 1
    })

    # Use StatefulSets for stateful components
    use_stateful_sets: bool = True

    # Use cert-manager for SSL
    use_cert_manager: bool = True

    class Config:
        extra = "forbid"


class DeploymentStrategy(BaseModel):
    """Configuration for the deployment strategy."""
    type: DeploymentStrategyType = DeploymentStrategyType.TRADITIONAL

    # Container base images
    base_images: Dict[str, str] = Field(default_factory=lambda: {
        "frontend": "node:18-alpine",
        "backend": "python:3.11-slim",
        "database": "postgres:15-alpine",
        "redis": "redis:7-alpine",
        "elasticsearch": "elasticsearch:8.6.2"
    })

    # Docker-specific configuration
    docker: DockerConfig = Field(default_factory=DockerConfig)

    # Kubernetes-specific configuration
    kubernetes: KubernetesConfig = Field(default_factory=KubernetesConfig)

    # Custom Dockerfiles (optional)
    custom_dockerfiles: Dict[str, str] = Field(default_factory=dict)

    class Config:
        extra = "forbid"

    @validator("custom_dockerfiles")
    def validate_custom_dockerfiles(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Validate that custom Dockerfiles are for valid components."""
        valid_components = ["frontend", "backend", "database", "redis", "elasticsearch", "monitoring", "ci_cd"]
        for component in v.keys():
            if component not in valid_components:
                raise ValueError(f"Invalid component for custom Dockerfile: {component}")
        return v
