from __future__ import annotations
'\nDatabase backend for audit events.\n\nThis module provides a backend that logs audit events to the database.\n'
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit.base import AuditBackend, AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.core.audit.exceptions import AuditBackendException
from app.core.audit.models import AuditLog
from app.core.audit.utils import anonymize_data
from app.core.base import InitializableComponent
from app.logging import get_logger
logger = get_logger('app.core.audit.backends.database')
class DatabaseAuditBackend(AuditBackend, InitializableComponent):
    __backend_name__ = 'database'
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    async def initialize(self) -> None:
        logger.info('Database audit backend initialized')
    async def shutdown(self) -> None:
        logger.info('Database audit backend shut down')
    async def log_event(self, event_type: AuditEventType, level: AuditLogLevel, context: AuditContext, details: Optional[Dict[str, Any]]=None, options: Optional[AuditOptions]=None) -> str:
        if not self.db:
            logger.warning('No database session provided')
            event_id = str(uuid.uuid4())
            return event_id
        options = options or AuditOptions()
        event_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc)
        processed_details = details or {}
        if options.anonymize_data:
            processed_details = anonymize_data(processed_details, options.sensitive_fields)
        try:
            context_dict = context.model_dump(exclude_none=True)
            user_id = uuid.UUID(context_dict['user_id']) if context_dict.get('user_id') else None
            resource_id = uuid.UUID(context_dict['resource_id']) if context_dict.get('resource_id') else None
            company_id = uuid.UUID(context_dict['company_id']) if context_dict.get('company_id') else None
            audit_log = AuditLog(id=uuid.UUID(event_id), timestamp=timestamp, event_type=event_type, level=level, user_id=user_id, ip_address=context_dict.get('ip_address'), resource_id=resource_id, resource_type=context_dict.get('resource_type'), details=processed_details, request_id=context_dict.get('request_id'), user_agent=context_dict.get('user_agent'), session_id=context_dict.get('session_id'), company_id=company_id)
            self.db.add(audit_log)
            await self.db.commit()
            logger.debug(f'Audit event {event_id} saved to database')
        except Exception as e:
            logger.error(f'Failed to save audit event to database: {str(e)}')
            await self.db.rollback()
            raise AuditBackendException(backend_name='database', message='Failed to save audit event to database', details={'event_id': event_id}, original_exception=e)
        return event_id
    async def health_check(self) -> Dict[str, Any]:
        if not self.db:
            return {'status': 'unhealthy', 'backend': 'database', 'error': 'No database session', 'timestamp': datetime.now(timezone.utc).isoformat()}
        try:
            from sqlalchemy import text
            result = await self.db.execute(text('SELECT 1'))
            if result.scalar() == 1:
                return {'status': 'healthy', 'backend': 'database', 'timestamp': datetime.now(timezone.utc).isoformat()}
            else:
                return {'status': 'unhealthy', 'backend': 'database', 'error': 'Database check failed', 'timestamp': datetime.now(timezone.utc).isoformat()}
        except Exception as e:
            return {'status': 'unhealthy', 'backend': 'database', 'error': str(e), 'timestamp': datetime.now(timezone.utc).isoformat()}