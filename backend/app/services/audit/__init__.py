# /app/services/audit/__init__.py
from __future__ import annotations

"""Audit service package for application-wide audit logging.

This package provides services for recording and retrieving audit logs
for security, compliance, and troubleshooting purposes.
"""

from app.services.audit.base import (
    AuditContext,
    AuditEventType,
    AuditLogLevel,
    AuditOptions,
)
from app.services.audit.service import AuditService


# Factory function for dependency injection
def get_audit_service(db=None):
    """Factory function to get AuditService

    Args:
        db: Optional database session

    Returns:
        AuditService instance
    """
    return AuditService(db)


__all__ = [
    "get_audit_service",
    "AuditService",
    "AuditEventType",
    "AuditLogLevel",
    "AuditContext",
    "AuditOptions",
]
