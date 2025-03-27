# app/domains/audit/service/__init__.py
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.audit.service.service import AuditService

# Singleton instance
_audit_service_instance: Optional[AuditService] = None


def get_audit_service(db: Optional[AsyncSession] = None) -> AuditService:
    """Get or create an AuditService instance.

    Args:
        db: Optional database session

    Returns:
        An AuditService instance
    """
    global _audit_service_instance

    # Create new instance if none exists or if a new DB session is provided
    if _audit_service_instance is None or db is not None:
        _audit_service_instance = AuditService(db)

    return _audit_service_instance
