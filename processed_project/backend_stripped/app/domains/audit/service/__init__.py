from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.audit.service.service import AuditService
_audit_service_instance: Optional[AuditService] = None
def get_audit_service(db: Optional[AsyncSession]=None) -> AuditService:
    global _audit_service_instance
    if _audit_service_instance is None or db is not None:
        _audit_service_instance = AuditService(db)
    return _audit_service_instance