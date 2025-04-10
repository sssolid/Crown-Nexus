from __future__ import annotations
'\nMain audit service implementation.\n\nThis module provides the primary AuditService that coordinates audit logging\nand querying operations.\n'
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit.base import AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.core.audit.manager import AuditManager
from app.core.base import CoreService, HealthCheckable
from app.logging import get_logger
logger = get_logger('app.core.audit.service')
class AuditService(CoreService, HealthCheckable):
    @property
    def service_name(self) -> str:
        return 'audit'
    def __init__(self, db: Optional[AsyncSession]=None) -> None:
        super().__init__()
        self.manager = AuditManager(db)
        self.register_component(self.manager)
        logger.debug('Audit service created')
    async def log_event(self, event_type: AuditEventType, user_id: Optional[str]=None, ip_address: Optional[str]=None, resource_id: Optional[str]=None, resource_type: Optional[str]=None, details: Optional[Dict[str, Any]]=None, level: Optional[AuditLogLevel]=None, options: Optional[AuditOptions]=None) -> str:
        context = AuditContext(user_id=user_id, ip_address=ip_address, resource_id=resource_id, resource_type=resource_type)
        return await self.manager.log_event(event_type=event_type, level=level, context=context, details=details, options=options)
    async def get_events(self, start_time: Optional[str]=None, end_time: Optional[str]=None, event_type: Optional[AuditEventType]=None, level: Optional[AuditLogLevel]=None, user_id: Optional[str]=None, resource_id: Optional[str]=None, resource_type: Optional[str]=None, limit: int=100, offset: int=0) -> Dict[str, Any]:
        return await self.manager.get_events(start_time=start_time, end_time=end_time, event_type=event_type, level=level, user_id=user_id, resource_id=resource_id, resource_type=resource_type, limit=limit, offset=offset)
    async def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        return await self.manager.get_event_by_id(event_id)
    async def get_user_activity(self, user_id: str, start_time: Optional[str]=None, end_time: Optional[str]=None, limit: int=100) -> List[Dict[str, Any]]:
        return await self.manager.get_user_activity(user_id=user_id, start_time=start_time, end_time=end_time, limit=limit)
    async def get_resource_history(self, resource_type: str, resource_id: str, limit: int=100) -> List[Dict[str, Any]]:
        return await self.manager.get_resource_history(resource_type=resource_type, resource_id=resource_id, limit=limit)
    async def purge_old_logs(self, days_to_keep: int=90) -> int:
        return await self.manager.purge_old_logs(days_to_keep)
    async def health_check(self) -> Dict[str, Any]:
        return await self.manager.health_check()