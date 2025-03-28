from __future__ import annotations
'Audit repository implementation.\n\nThis module provides data access and persistence operations for Audit entities.\n'
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy import select, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.audit.models import AuditLog
from app.repositories.base import BaseRepository
class AuditLogRepository(BaseRepository[AuditLog, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=AuditLog, db=db)
    async def create_log(self, event_type: str, level: str, details: Optional[Dict[str, Any]]=None, user_id: Optional[uuid.UUID]=None, ip_address: Optional[str]=None, resource_id: Optional[uuid.UUID]=None, resource_type: Optional[str]=None, request_id: Optional[str]=None, user_agent: Optional[str]=None, session_id: Optional[str]=None, company_id: Optional[uuid.UUID]=None, timestamp: Optional[datetime]=None) -> AuditLog:
        if timestamp is None:
            timestamp = datetime.now()
        audit_log = AuditLog(timestamp=timestamp, event_type=event_type, level=level, user_id=user_id, ip_address=ip_address, resource_id=resource_id, resource_type=resource_type, details=details, request_id=request_id, user_agent=user_agent, session_id=session_id, company_id=company_id)
        self.db.add(audit_log)
        await self.db.flush()
        await self.db.refresh(audit_log)
        return audit_log
    async def get_by_user(self, user_id: uuid.UUID, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(AuditLog).where(AuditLog.user_id == user_id).order_by(desc(AuditLog.timestamp))
        return await self.paginate(query, page, page_size)
    async def get_by_resource(self, resource_type: str, resource_id: uuid.UUID, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(AuditLog).where(AuditLog.resource_type == resource_type, AuditLog.resource_id == resource_id).order_by(desc(AuditLog.timestamp))
        return await self.paginate(query, page, page_size)
    async def get_by_event_type(self, event_type: str, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(AuditLog).where(AuditLog.event_type == event_type).order_by(desc(AuditLog.timestamp))
        return await self.paginate(query, page, page_size)
    async def get_by_level(self, level: str, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(AuditLog).where(AuditLog.level == level).order_by(desc(AuditLog.timestamp))
        return await self.paginate(query, page, page_size)
    async def get_by_company(self, company_id: uuid.UUID, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(AuditLog).where(AuditLog.company_id == company_id).order_by(desc(AuditLog.timestamp))
        return await self.paginate(query, page, page_size)
    async def get_by_time_range(self, start_time: datetime, end_time: Optional[datetime]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        if end_time is None:
            end_time = datetime.now()
        query = select(AuditLog).where(AuditLog.timestamp >= start_time, AuditLog.timestamp <= end_time).order_by(desc(AuditLog.timestamp))
        return await self.paginate(query, page, page_size)
    async def get_recent_logs(self, hours: int=24, page: int=1, page_size: int=20) -> Dict[str, Any]:
        start_time = datetime.now() - timedelta(hours=hours)
        query = select(AuditLog).where(AuditLog.timestamp >= start_time).order_by(desc(AuditLog.timestamp))
        return await self.paginate(query, page, page_size)
    async def search(self, search_term: str, page: int=1, page_size: int=20) -> Dict[str, Any]:
        resource_id = None
        try:
            resource_id = uuid.UUID(search_term)
        except ValueError:
            pass
        conditions = []
        if resource_id:
            conditions.append(AuditLog.resource_id == resource_id)
        conditions.extend([AuditLog.event_type.ilike(f'%{search_term}%'), AuditLog.resource_type.ilike(f'%{search_term}%'), AuditLog.ip_address.ilike(f'%{search_term}%'), AuditLog.request_id.ilike(f'%{search_term}%'), AuditLog.session_id.ilike(f'%{search_term}%')])
        query = select(AuditLog).where(or_(*conditions)).order_by(desc(AuditLog.timestamp))
        return await self.paginate(query, page, page_size)