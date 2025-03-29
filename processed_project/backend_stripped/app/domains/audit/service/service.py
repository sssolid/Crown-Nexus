from __future__ import annotations
'Main audit service implementation.\n\nThis module provides the primary AuditService that coordinates audit logging\nand querying operations.\n'
import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.logging import get_logger
from app.domains.audit.service.base import AuditContext, AuditEventType, AuditLogLevel, AuditLogger, AuditOptions
from app.domains.audit.service.factory import AuditLoggerFactory
from app.domains.audit.service.query import AuditQuery
from app.services.interfaces import ServiceInterface
logger = get_logger('app.domains.audit.service.service')
class AuditService(ServiceInterface):
    def __init__(self, db: Optional[AsyncSession]=None) -> None:
        self.db = db
        self.enabled = getattr(settings, 'AUDIT_LOGGING_ENABLED', True)
        self.loggers: List[AuditLogger] = []
        self.sensitive_fields: List[str] = ['password', 'token', 'secret', 'credit_card', 'ssn', 'social_security', 'api_key']
        self.anonymize_events: List[AuditEventType] = [AuditEventType.GDPR_DATA_EXPORT, AuditEventType.GDPR_DATA_DELETED]
        self.event_level_mapping: Dict[AuditEventType, AuditLogLevel] = {AuditEventType.ACCESS_DENIED: AuditLogLevel.WARNING, AuditEventType.LOGIN_FAILED: AuditLogLevel.WARNING, AuditEventType.USER_DELETED: AuditLogLevel.WARNING, AuditEventType.API_KEY_REVOKED: AuditLogLevel.WARNING, AuditEventType.PAYMENT_REFUNDED: AuditLogLevel.WARNING, AuditEventType.DATA_DELETED: AuditLogLevel.WARNING, AuditEventType.CHAT_MESSAGE_DELETED: AuditLogLevel.INFO, AuditEventType.GDPR_DATA_DELETED: AuditLogLevel.WARNING, AuditEventType.SYSTEM_STOPPED: AuditLogLevel.WARNING, AuditEventType.MAINTENANCE_MODE_ENABLED: AuditLogLevel.WARNING}
        self.query = AuditQuery(db) if db else None
        logger.info('AuditService initialized')
    async def initialize(self) -> None:
        logger.debug('Initializing audit service')
        self.loggers = AuditLoggerFactory.create_default_loggers(self.db)
        if self.enabled:
            await self.log_event(event_type=AuditEventType.SYSTEM_STARTED, details={'service': 'AuditService', 'action': 'initialize'})
    async def shutdown(self) -> None:
        logger.debug('Shutting down audit service')
        if self.enabled:
            await self.log_event(event_type=AuditEventType.SYSTEM_STOPPED, details={'service': 'AuditService', 'action': 'shutdown'})
    def add_logger(self, logger: AuditLogger) -> None:
        self.loggers.append(logger)
        logger.debug(f'Added audit logger: {logger.__class__.__name__}')
    async def log_event(self, event_type: AuditEventType, user_id: Optional[str]=None, ip_address: Optional[str]=None, resource_id: Optional[str]=None, resource_type: Optional[str]=None, details: Optional[Dict[str, Any]]=None, context: Optional[AuditContext]=None, level: Optional[AuditLogLevel]=None, options: Optional[AuditOptions]=None) -> str:
        if not self.enabled:
            return 'disabled'
        if not self.loggers:
            logger.warning('No audit loggers configured')
            return 'no-loggers'
        if level is None:
            level = self.event_level_mapping.get(event_type, AuditLogLevel.INFO)
        if options is None:
            options = AuditOptions(sensitive_fields=self.sensitive_fields, anonymize_data=event_type in self.anonymize_events)
        event_id = None
        for audit_logger in self.loggers:
            try:
                logger_event_id = await audit_logger.log_event(event_type=event_type, user_id=user_id, ip_address=ip_address, resource_id=resource_id, resource_type=resource_type, details=details, context=context, level=level, options=options)
                if event_id is None:
                    event_id = logger_event_id
            except Exception as e:
                logger.error(f'Error in audit logger: {str(e)}')
        return event_id or 'error'
    async def get_events(self, user_id: Optional[str]=None, event_type: Optional[AuditEventType]=None, resource_id: Optional[str]=None, resource_type: Optional[str]=None, start_time: Optional[datetime]=None, end_time: Optional[datetime]=None, level: Optional[AuditLogLevel]=None, limit: int=100, offset: int=0, sort_field: str='timestamp', sort_order: str='desc') -> Dict[str, Any]:
        if not self.enabled:
            return {'total': 0, 'items': []}
        if not self.query:
            return {'total': 0, 'items': [], 'error': 'Database querying not available'}
        return await self.query.get_events(user_id=user_id, event_type=event_type, resource_id=resource_id, resource_type=resource_type, start_time=start_time, end_time=end_time, level=level, limit=limit, offset=offset, sort_field=sort_field, sort_order=sort_order)
    async def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        if not self.enabled:
            return None
        if not self.query:
            return None
        return await self.query.get_event_by_id(event_id)
    async def get_user_activity(self, user_id: str, start_time: Optional[datetime]=None, end_time: Optional[datetime]=None, limit: int=100) -> List[Dict[str, Any]]:
        if not self.enabled:
            return []
        if not self.query:
            return []
        return await self.query.get_user_activity(user_id=user_id, start_time=start_time, end_time=end_time, limit=limit)
    async def get_resource_history(self, resource_type: str, resource_id: str, limit: int=100) -> List[Dict[str, Any]]:
        if not self.enabled:
            return []
        if not self.query:
            return []
        return await self.query.get_resource_history(resource_type=resource_type, resource_id=resource_id, limit=limit)
    async def purge_old_logs(self, days_to_keep: int=90) -> int:
        if not self.enabled:
            return 0
        if not self.query:
            return 0
        deleted_count = await self.query.purge_old_logs(days_to_keep)
        await self.log_event(event_type=AuditEventType.DATA_DELETED, details={'action': 'purge_old_logs', 'days_kept': days_to_keep, 'cutoff_date': (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=days_to_keep)).isoformat(), 'records_deleted': deleted_count}, level=AuditLogLevel.WARNING)
        return deleted_count