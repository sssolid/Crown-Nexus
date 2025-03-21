from __future__ import annotations
'Audit service package for application-wide audit logging.\n\nThis package provides services for recording and retrieving audit logs\nfor security, compliance, and troubleshooting purposes.\n'
from app.services.audit.base import AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.services.audit.service import AuditService
def get_audit_service(db=None):
    return AuditService(db)
__all__ = ['get_audit_service', 'AuditService', 'AuditEventType', 'AuditLogLevel', 'AuditContext', 'AuditOptions']