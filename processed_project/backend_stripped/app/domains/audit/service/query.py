from __future__ import annotations
'Query functionality for audit logs.\n\nThis module provides functionality for querying and retrieving audit logs\nfrom the database.\n'
import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.logging import get_logger
from app.domains.audit.service.base import AuditEventType, AuditLogLevel
logger = get_logger('app.domains.audit.service.query')
class AuditQuery:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.logger = logger
    async def get_events(self, user_id: Optional[str]=None, event_type: Optional[AuditEventType]=None, resource_id: Optional[str]=None, resource_type: Optional[str]=None, start_time: Optional[datetime]=None, end_time: Optional[datetime]=None, level: Optional[AuditLogLevel]=None, limit: int=100, offset: int=0, sort_field: str='timestamp', sort_order: str='desc') -> Dict[str, Any]:
        try:
            from app.domains.audit.models import AuditLog
            query = select(AuditLog)
            if user_id:
                query = query.filter(AuditLog.user_id == user_id)
            if event_type:
                query = query.filter(AuditLog.event_type == event_type)
            if resource_id:
                query = query.filter(AuditLog.resource_id == resource_id)
            if resource_type:
                query = query.filter(AuditLog.resource_type == resource_type)
            if level:
                query = query.filter(AuditLog.level == level)
            if start_time:
                query = query.filter(AuditLog.timestamp >= start_time)
            if end_time:
                query = query.filter(AuditLog.timestamp <= end_time)
            count_query = select(func.count()).select_from(query.subquery())
            count_result = await self.db.execute(count_query)
            total = count_result.scalar() or 0
            if sort_order.lower() == 'desc':
                query = query.order_by(desc(getattr(AuditLog, sort_field)))
            else:
                query = query.order_by(getattr(AuditLog, sort_field))
            query = query.offset(offset).limit(limit)
            result = await self.db.execute(query)
            logs = result.scalars().all()
            items = [log.to_dict() for log in logs]
            return {'total': total, 'items': items}
        except Exception as e:
            self.logger.error(f'Error retrieving audit events: {str(e)}')
            return {'total': 0, 'items': [], 'error': str(e)}
    async def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        try:
            from app.domains.audit.models import AuditLog
            query = select(AuditLog).filter(AuditLog.id == event_id)
            result = await self.db.execute(query)
            log = result.scalar_one_or_none()
            if log:
                return log.to_dict()
            return None
        except Exception as e:
            self.logger.error(f'Error retrieving audit event by ID: {str(e)}')
            return None
    async def get_user_activity(self, user_id: str, start_time: Optional[datetime]=None, end_time: Optional[datetime]=None, limit: int=100) -> List[Dict[str, Any]]:
        result = await self.get_events(user_id=user_id, start_time=start_time, end_time=end_time, limit=limit, sort_field='timestamp', sort_order='desc')
        return result.get('items', [])
    async def get_resource_history(self, resource_type: str, resource_id: str, limit: int=100) -> List[Dict[str, Any]]:
        result = await self.get_events(resource_id=resource_id, resource_type=resource_type, limit=limit, sort_field='timestamp', sort_order='desc')
        return result.get('items', [])
    async def purge_old_logs(self, days_to_keep: int=90) -> int:
        try:
            from app.domains.audit.models import AuditLog
            cutoff_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=days_to_keep)
            delete_stmt = delete(AuditLog).where(AuditLog.timestamp < cutoff_date)
            result = await self.db.execute(delete_stmt)
            await self.db.commit()
            deleted_count = result.rowcount
            self.logger.info(f'Purged {deleted_count} audit logs older than {cutoff_date}')
            return deleted_count
        except Exception as e:
            self.logger.error(f'Error purging old audit logs: {str(e)}')
            await self.db.rollback()
            return 0