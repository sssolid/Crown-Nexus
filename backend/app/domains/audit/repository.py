from __future__ import annotations

"""Audit repository implementation.

This module provides data access and persistence operations for Audit entities.
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from sqlalchemy import select, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.audit.models import AuditLog
from app.repositories.base import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog, uuid.UUID]):
    """Repository for AuditLog entity operations.

    Provides methods for querying, creating, and retrieving
    AuditLog entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the audit log repository.

        Args:
            db: The database session.
        """
        super().__init__(model=AuditLog, db=db)

    async def create_log(
        self,
        event_type: str,
        level: str,
        details: Optional[Dict[str, Any]] = None,
        user_id: Optional[uuid.UUID] = None,
        ip_address: Optional[str] = None,
        resource_id: Optional[uuid.UUID] = None,
        resource_type: Optional[str] = None,
        request_id: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        company_id: Optional[uuid.UUID] = None,
        timestamp: Optional[datetime] = None,
    ) -> AuditLog:
        """Create a new audit log entry.

        Args:
            event_type: Type of event being audited.
            level: Log level (info, warning, error).
            details: Additional details about the event.
            user_id: ID of the user who performed the action.
            ip_address: IP address of the user.
            resource_id: ID of the affected resource.
            resource_type: Type of the affected resource.
            request_id: ID of the request that triggered the event.
            user_agent: User agent of the client.
            session_id: ID of the user's session.
            company_id: ID of the company context.
            timestamp: When the audited event occurred (defaults to now).

        Returns:
            The created audit log entry.
        """
        if timestamp is None:
            timestamp = datetime.now()

        audit_log = AuditLog(
            timestamp=timestamp,
            event_type=event_type,
            level=level,
            user_id=user_id,
            ip_address=ip_address,
            resource_id=resource_id,
            resource_type=resource_type,
            details=details,
            request_id=request_id,
            user_agent=user_agent,
            session_id=session_id,
            company_id=company_id,
        )

        self.db.add(audit_log)
        await self.db.flush()
        await self.db.refresh(audit_log)

        return audit_log

    async def get_by_user(
        self, user_id: uuid.UUID, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated audit logs for a specific user.

        Args:
            user_id: The user ID to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(desc(AuditLog.timestamp))
        )

        return await self.paginate(query, page, page_size)

    async def get_by_resource(
        self,
        resource_type: str,
        resource_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Get paginated audit logs for a specific resource.

        Args:
            resource_type: The resource type to filter by.
            resource_id: The resource ID to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(AuditLog)
            .where(
                AuditLog.resource_type == resource_type,
                AuditLog.resource_id == resource_id,
            )
            .order_by(desc(AuditLog.timestamp))
        )

        return await self.paginate(query, page, page_size)

    async def get_by_event_type(
        self, event_type: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated audit logs for a specific event type.

        Args:
            event_type: The event type to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(AuditLog)
            .where(AuditLog.event_type == event_type)
            .order_by(desc(AuditLog.timestamp))
        )

        return await self.paginate(query, page, page_size)

    async def get_by_level(
        self, level: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated audit logs for a specific log level.

        Args:
            level: The log level to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(AuditLog)
            .where(AuditLog.level == level)
            .order_by(desc(AuditLog.timestamp))
        )

        return await self.paginate(query, page, page_size)

    async def get_by_company(
        self, company_id: uuid.UUID, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated audit logs for a specific company.

        Args:
            company_id: The company ID to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(AuditLog)
            .where(AuditLog.company_id == company_id)
            .order_by(desc(AuditLog.timestamp))
        )

        return await self.paginate(query, page, page_size)

    async def get_by_time_range(
        self,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Get paginated audit logs within a time range.

        Args:
            start_time: The start time of the range.
            end_time: The end time of the range (defaults to now).
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        if end_time is None:
            end_time = datetime.now()

        query = (
            select(AuditLog)
            .where(AuditLog.timestamp >= start_time, AuditLog.timestamp <= end_time)
            .order_by(desc(AuditLog.timestamp))
        )

        return await self.paginate(query, page, page_size)

    async def get_recent_logs(
        self, hours: int = 24, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated recent audit logs.

        Args:
            hours: Number of hours to look back.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        start_time = datetime.now() - timedelta(hours=hours)

        query = (
            select(AuditLog)
            .where(AuditLog.timestamp >= start_time)
            .order_by(desc(AuditLog.timestamp))
        )

        return await self.paginate(query, page, page_size)

    async def search(
        self, search_term: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Search audit logs by various fields.

        Args:
            search_term: The term to search for.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        # Convert search term to UUID if possible (for resource_id)
        resource_id = None
        try:
            resource_id = uuid.UUID(search_term)
        except ValueError:
            pass

        conditions = []

        # Add search conditions
        if resource_id:
            conditions.append(AuditLog.resource_id == resource_id)

        conditions.extend(
            [
                AuditLog.event_type.ilike(f"%{search_term}%"),
                AuditLog.resource_type.ilike(f"%{search_term}%"),
                AuditLog.ip_address.ilike(f"%{search_term}%"),
                AuditLog.request_id.ilike(f"%{search_term}%"),
                AuditLog.session_id.ilike(f"%{search_term}%"),
            ]
        )

        query = (
            select(AuditLog).where(or_(*conditions)).order_by(desc(AuditLog.timestamp))
        )

        return await self.paginate(query, page, page_size)
