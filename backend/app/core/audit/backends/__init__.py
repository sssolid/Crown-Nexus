from __future__ import annotations

"""
Factory for creating audit backends.

This module provides a factory for creating different audit backend instances
based on configuration settings.
"""

from typing import Any, Dict, List, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit.base import AuditBackend
from app.core.config import settings
from app.logging import get_logger

logger = get_logger("app.core.audit.backends")

# Backend registry
_backends: Dict[str, Type[AuditBackend]] = {}


def register_backend(name: str, backend_class: Type[AuditBackend]) -> None:
    """Register an audit backend.

    Args:
        name: Name of the backend.
        backend_class: Backend class to register.

    Raises:
        ValueError: If a backend with the given name is already registered.
    """
    if name in _backends:
        raise ValueError(f"Audit backend '{name}' is already registered")

    _backends[name] = backend_class
    logger.debug(f"Registered audit backend: {name}")


def get_backend(name: str, **kwargs: Any) -> AuditBackend:
    """Get an audit backend by name.

    Args:
        name: Name of the backend to get.
        **kwargs: Additional arguments for the backend.

    Returns:
        The backend instance.

    Raises:
        ValueError: If the backend is not registered.
    """
    if name not in _backends:
        valid_backends = ", ".join(_backends.keys())
        raise ValueError(
            f"Unknown audit backend: {name}. Valid backends: {valid_backends}"
        )

    backend_class = _backends[name]
    return backend_class(**kwargs)


def create_default_backends(db: Optional[AsyncSession] = None) -> List[AuditBackend]:
    """Create the default set of audit backends based on configuration.

    Args:
        db: Database session for database operations.

    Returns:
        List of created backend instances.
    """
    backends: List[AuditBackend] = []

    # Always add logging backend
    backends.append(get_backend("logging"))

    # Add file backend if configured
    if getattr(settings, "AUDIT_LOG_TO_FILE", False):
        file_path = getattr(settings, "AUDIT_LOG_FILE", "/var/log/app/audit.log")
        backends.append(get_backend("file", file_path=file_path))

    # Add database backend if configured and DB session provided
    if db and getattr(settings, "AUDIT_LOG_TO_DB", False):
        backends.append(get_backend("database", db=db))

    return backends


# Import backend implementations after defining the factory functions
# to avoid circular imports
from app.core.audit.backends.database import DatabaseAuditBackend
from app.core.audit.backends.file import FileAuditBackend
from app.core.audit.backends.logging import LoggingAuditBackend

# Register backend implementations
register_backend("logging", LoggingAuditBackend)
register_backend("file", FileAuditBackend)
register_backend("database", DatabaseAuditBackend)

__all__ = [
    "get_backend",
    "create_default_backends",
    "register_backend",
    "LoggingAuditBackend",
    "FileAuditBackend",
    "DatabaseAuditBackend",
]
