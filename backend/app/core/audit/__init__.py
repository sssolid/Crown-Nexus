from __future__ import annotations

"""
Audit package for logging and tracking system activity.

This package provides functionality for auditing and tracking system activity:
- Logging of user actions and system events
- Query capabilities for retrieving audit logs
- Multiple backend implementations for storing audit logs
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

# Import base types and enums
from app.core.audit.base import (
    AuditBackend,
    AuditContext,
    AuditEventType,
    AuditLogLevel,
    AuditOptions,
)

# Import service
from app.core.audit.service import AuditService

# Import exceptions
from app.core.audit.exceptions import (
    AuditBackendException,
    AuditConfigurationException,
    AuditException,
    AuditManagerException,
)

# Singleton service instance
_audit_service_instance: Optional[AuditService] = None


def get_audit_service(db: Optional[AsyncSession] = None) -> AuditService:
    """Get the audit service instance.

    Args:
        db: Database session for database operations.

    Returns:
        The audit service instance.
    """
    global _audit_service_instance

    # Create new instance if none exists or if db is provided
    if _audit_service_instance is None or db is not None:
        _audit_service_instance = AuditService(db)

    return _audit_service_instance


# Export public API
__all__ = [
    # Service
    "AuditService",
    "get_audit_service",
    # Base types
    "AuditBackend",
    "AuditContext",
    "AuditEventType",
    "AuditLogLevel",
    "AuditOptions",
    # Exceptions
    "AuditException",
    "AuditBackendException",
    "AuditManagerException",
    "AuditConfigurationException",
]
