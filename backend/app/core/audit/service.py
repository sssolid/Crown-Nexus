from __future__ import annotations

"""
Main audit service implementation.

This module provides the primary AuditService that coordinates audit logging
and querying operations.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit.base import (
    AuditContext,
    AuditEventType,
    AuditLogLevel,
    AuditOptions,
)
from app.core.audit.manager import AuditManager
from app.core.base import CoreService, HealthCheckable
from app.logging import get_logger

logger = get_logger("app.core.audit.service")


class AuditService(CoreService, HealthCheckable):
    """Service for audit logging and querying.

    This service coordinates audit logging across different destinations and provides
    query capabilities for retrieving audit logs.
    """

    @property
    def service_name(self) -> str:
        """Get the service name.

        Returns:
            The service name.
        """
        return "audit"

    def __init__(self, db: Optional[AsyncSession] = None) -> None:
        """Initialize the audit service.

        Args:
            db: Database session for database operations.
        """
        super().__init__()
        self.manager = AuditManager(db)
        self.register_component(self.manager)

        logger.debug("Audit service created")

    async def log_event(
        self,
        event_type: AuditEventType,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        level: Optional[AuditLogLevel] = None,
        options: Optional[AuditOptions] = None,
    ) -> str:
        """Log an audit event.

        Args:
            event_type: Type of event being logged.
            user_id: ID of the user who performed the action.
            ip_address: IP address the action was performed from.
            resource_id: ID of the resource being acted upon.
            resource_type: Type of resource being acted upon.
            details: Additional event details.
            level: Log level for the event.
            options: Options for logging the event.

        Returns:
            ID of the logged event.
        """
        # Create context from parameters
        context = AuditContext(
            user_id=user_id,
            ip_address=ip_address,
            resource_id=resource_id,
            resource_type=resource_type,
        )

        # Delegate to manager
        return await self.manager.log_event(
            event_type=event_type,
            level=level,
            context=context,
            details=details,
            options=options,
        )

    async def get_events(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        event_type: Optional[AuditEventType] = None,
        level: Optional[AuditLogLevel] = None,
        user_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Get audit events matching the specified criteria.

        Args:
            start_time: Filter by start time (ISO format).
            end_time: Filter by end time (ISO format).
            event_type: Filter by event type.
            level: Filter by log level.
            user_id: Filter by user ID.
            resource_id: Filter by resource ID.
            resource_type: Filter by resource type.
            limit: Maximum number of events to return.
            offset: Offset for pagination.

        Returns:
            Dictionary containing total count and list of events.
        """
        # Delegate to manager
        return await self.manager.get_events(
            start_time=start_time,
            end_time=end_time,
            event_type=event_type,
            level=level,
            user_id=user_id,
            resource_id=resource_id,
            resource_type=resource_type,
            limit=limit,
            offset=offset,
        )

    async def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get an audit event by ID.

        Args:
            event_id: ID of the event to get.

        Returns:
            Event details or None if not found.
        """
        # Delegate to manager
        return await self.manager.get_event_by_id(event_id)

    async def get_user_activity(
        self,
        user_id: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get audit events for a specific user.

        Args:
            user_id: ID of the user.
            start_time: Filter by start time (ISO format).
            end_time: Filter by end time (ISO format).
            limit: Maximum number of events to return.

        Returns:
            List of audit events.
        """
        # Delegate to manager
        return await self.manager.get_user_activity(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    async def get_resource_history(
        self,
        resource_type: str,
        resource_id: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get audit events for a specific resource.

        Args:
            resource_type: Type of the resource.
            resource_id: ID of the resource.
            limit: Maximum number of events to return.

        Returns:
            List of audit events.
        """
        # Delegate to manager
        return await self.manager.get_resource_history(
            resource_type=resource_type,
            resource_id=resource_id,
            limit=limit,
        )

    async def purge_old_logs(self, days_to_keep: int = 90) -> int:
        """Delete audit logs older than the specified number of days.

        Args:
            days_to_keep: Number of days to keep logs for.

        Returns:
            Number of logs deleted.
        """
        # Delegate to manager
        return await self.manager.purge_old_logs(days_to_keep)

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check.

        Returns:
            Dict containing health status information.
        """
        return await self.manager.health_check()
