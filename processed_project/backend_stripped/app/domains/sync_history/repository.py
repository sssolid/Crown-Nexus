from __future__ import annotations
'\nSync history repository implementation.\n\nThis module provides data access and persistence operations for sync history entities,\ntracking the status and outcomes of data synchronization operations.\n'
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from sqlalchemy import select, desc, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.logging import get_logger
from app.domains.sync_history.models import SyncHistory, SyncEvent, SyncStatus, SyncEntityType, SyncSource
from app.repositories.base import BaseRepository
logger = get_logger('app.repositories.sync_history_repository')
class SyncHistoryRepository(BaseRepository[SyncHistory, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=SyncHistory, db=db)
    async def create_sync(self, entity_type: SyncEntityType, source: SyncSource=SyncSource.AS400, triggered_by_id: Optional[uuid.UUID]=None, details: Optional[Dict[str, Any]]=None) -> SyncHistory:
        sync = SyncHistory(entity_type=entity_type.value, source=source.value, status=SyncStatus.PENDING.value, triggered_by_id=triggered_by_id, details=details or {}, started_at=datetime.now())
        self.db.add(sync)
        await self.db.flush()
        await self.db.refresh(sync)
        logger.debug(f'Created sync history record: {sync.id} for {entity_type.value}')
        return sync
    async def update_sync_status(self, sync_id: uuid.UUID, status: SyncStatus, records_processed: int=0, records_created: int=0, records_updated: int=0, records_failed: int=0, error_message: Optional[str]=None, details: Optional[Dict[str, Any]]=None) -> SyncHistory:
        sync = await self.get_by_id(sync_id)
        if not sync:
            raise ResourceNotFoundException(resource_type='SyncHistory', resource_id=str(sync_id))
        if status in [SyncStatus.COMPLETED, SyncStatus.FAILED, SyncStatus.CANCELLED]:
            sync.completed_at = datetime.now()
            if sync.started_at:
                sync.sync_duration = (sync.completed_at - sync.started_at).total_seconds()
        sync.status = status.value
        sync.records_processed = records_processed
        sync.records_created = records_created
        sync.records_updated = records_updated
        sync.records_failed = records_failed
        if error_message:
            sync.error_message = error_message
        if details:
            sync.details = details if sync.details is None else {**sync.details, **details}
        self.db.add(sync)
        await self.db.flush()
        await self.db.refresh(sync)
        logger.debug(f'Updated sync history record: {sync.id} to status {status.value}')
        return sync
    async def add_sync_event(self, sync_id: uuid.UUID, event_type: str, message: str, details: Optional[Dict[str, Any]]=None) -> SyncEvent:
        sync = await self.get_by_id(sync_id)
        if not sync:
            raise ResourceNotFoundException(resource_type='SyncHistory', resource_id=str(sync_id))
        event = SyncEvent(sync_id=sync_id, event_type=event_type, message=message, details=details, timestamp=datetime.now())
        self.db.add(event)
        await self.db.flush()
        await self.db.refresh(event)
        logger.debug(f'Added sync event: {event.id} to sync {sync_id}')
        return event
    async def get_sync_events(self, sync_id: uuid.UUID, limit: int=100) -> List[SyncEvent]:
        query = select(SyncEvent).where(SyncEvent.sync_id == sync_id).order_by(desc(SyncEvent.timestamp)).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_latest_syncs(self, entity_type: Optional[SyncEntityType]=None, source: Optional[SyncSource]=None, status: Optional[SyncStatus]=None, limit: int=10) -> List[SyncHistory]:
        conditions = []
        if entity_type:
            conditions.append(SyncHistory.entity_type == entity_type.value)
        if source:
            conditions.append(SyncHistory.source == source.value)
        if status:
            conditions.append(SyncHistory.status == status.value)
        query = select(SyncHistory).order_by(desc(SyncHistory.started_at)).limit(limit)
        if conditions:
            query = query.where(and_(*conditions))
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_active_syncs(self, entity_type: Optional[SyncEntityType]=None, source: Optional[SyncSource]=None) -> List[SyncHistory]:
        conditions = [SyncHistory.status.in_([SyncStatus.PENDING.value, SyncStatus.RUNNING.value])]
        if entity_type:
            conditions.append(SyncHistory.entity_type == entity_type.value)
        if source:
            conditions.append(SyncHistory.source == source.value)
        query = select(SyncHistory).where(and_(*conditions)).order_by(desc(SyncHistory.started_at))
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_sync_stats(self, days: int=30, entity_type: Optional[SyncEntityType]=None, source: Optional[SyncSource]=None) -> Dict[str, Any]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        conditions = [SyncHistory.started_at >= start_date, SyncHistory.started_at <= end_date]
        if entity_type:
            conditions.append(SyncHistory.entity_type == entity_type.value)
        if source:
            conditions.append(SyncHistory.source == source.value)
        total_query = select(func.count()).select_from(SyncHistory).where(and_(*conditions))
        success_query = select(func.count()).select_from(SyncHistory).where(and_(*conditions, SyncHistory.status == SyncStatus.COMPLETED.value))
        failed_query = select(func.count()).select_from(SyncHistory).where(and_(*conditions, SyncHistory.status == SyncStatus.FAILED.value))
        records_query = select(func.sum(SyncHistory.records_processed).label('processed'), func.sum(SyncHistory.records_created).label('created'), func.sum(SyncHistory.records_updated).label('updated'), func.sum(SyncHistory.records_failed).label('failed')).where(and_(*conditions))
        duration_query = select(func.avg(SyncHistory.sync_duration).label('avg_duration')).where(and_(*conditions, SyncHistory.sync_duration.is_not(None)))
        total_result = await self.db.execute(total_query)
        success_result = await self.db.execute(success_query)
        failed_result = await self.db.execute(failed_query)
        records_result = await self.db.execute(records_query)
        duration_result = await self.db.execute(duration_query)
        total_count = total_result.scalar() or 0
        success_count = success_result.scalar() or 0
        failed_count = failed_result.scalar() or 0
        records_row = records_result.first()
        records_processed = records_row[0] if records_row and records_row[0] else 0
        records_created = records_row[1] if records_row and records_row[1] else 0
        records_updated = records_row[2] if records_row and records_row[2] else 0
        records_failed = records_row[3] if records_row and records_row[3] else 0
        avg_duration = duration_result.scalar() or 0
        return {'period_days': days, 'start_date': start_date.isoformat(), 'end_date': end_date.isoformat(), 'total_syncs': total_count, 'successful_syncs': success_count, 'failed_syncs': failed_count, 'success_rate': success_count / total_count * 100 if total_count > 0 else 0, 'records_processed': records_processed, 'records_created': records_created, 'records_updated': records_updated, 'records_failed': records_failed, 'average_duration_seconds': avg_duration, 'entity_type': entity_type.value if entity_type else 'all', 'source': source.value if source else 'all'}
    async def cancel_active_syncs(self, entity_type: Optional[SyncEntityType]=None, source: Optional[SyncSource]=None, cancelled_by_id: Optional[uuid.UUID]=None) -> int:
        active_syncs = await self.get_active_syncs(entity_type, source)
        cancelled_count = 0
        for sync in active_syncs:
            try:
                message = 'Sync cancelled manually'
                if cancelled_by_id:
                    message += f' by user {cancelled_by_id}'
                await self.update_sync_status(sync.id, SyncStatus.CANCELLED, records_processed=sync.records_processed, records_created=sync.records_created, records_updated=sync.records_updated, records_failed=sync.records_failed, error_message=message)
                await self.add_sync_event(sync.id, 'cancel', message, {'cancelled_by': str(cancelled_by_id) if cancelled_by_id else None})
                cancelled_count += 1
            except Exception as e:
                logger.error(f'Failed to cancel sync {sync.id}: {str(e)}')
        return cancelled_count
class SyncEventRepository(BaseRepository[SyncEvent, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=SyncEvent, db=db)
    async def get_events_by_type(self, event_type: str, sync_id: Optional[uuid.UUID]=None, limit: int=100) -> List[SyncEvent]:
        conditions = [SyncEvent.event_type == event_type]
        if sync_id:
            conditions.append(SyncEvent.sync_id == sync_id)
        query = select(SyncEvent).where(and_(*conditions)).order_by(desc(SyncEvent.timestamp)).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())