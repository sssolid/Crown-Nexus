from __future__ import annotations
'\nAudit package for logging and tracking system activity.\n\nThis package provides functionality for auditing and tracking system activity:\n- Logging of user actions and system events\n- Query capabilities for retrieving audit logs\n- Multiple backend implementations for storing audit logs\n'
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit.base import AuditBackend, AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.core.audit.service import AuditService
from app.core.audit.exceptions import AuditBackendException, AuditConfigurationException, AuditException, AuditManagerException
_audit_service_instance: Optional[AuditService] = None
def get_audit_service(db: Optional[AsyncSession]=None) -> AuditService:
    global _audit_service_instance
    if _audit_service_instance is None or db is not None:
        _audit_service_instance = AuditService(db)
    return _audit_service_instance
__all__ = ['AuditService', 'get_audit_service', 'AuditBackend', 'AuditContext', 'AuditEventType', 'AuditLogLevel', 'AuditOptions', 'AuditException', 'AuditBackendException', 'AuditManagerException', 'AuditConfigurationException']