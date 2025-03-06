"""Custom exceptions for the Crown Nexus deployment system."""
from __future__ import annotations


class DeploymentError(Exception):
    """Base class for deployment-related exceptions."""
    pass


class ServerConnectionError(DeploymentError):
    """Raised when a connection to a server fails."""
    pass


class RoleConfigurationError(DeploymentError):
    """Raised when there's an issue with role configuration."""
    pass


class ValidationError(DeploymentError):
    """Raised when validation fails."""
    pass


class RollbackError(DeploymentError):
    """Raised when rollback fails."""
    pass


class AnalyzerError(DeploymentError):
    """Raised when server analysis fails."""
    pass


class ScriptGenerationError(DeploymentError):
    """Raised when script generation fails."""
    pass
