from __future__ import annotations

"""
Audit manager for the application.

This module provides a central manager for audit backends,
handling initialization, configuration, and access to backends.
"""

import datetime
import uuid
from typing import Any, Dict, List, Optional, Union, cast

from sqlalchemy import delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit.backends import create_default_backends, get_backend
from app.core.audit.base import (
    AuditBackend,
    AuditContext,
    AuditEventType,
    AuditLogLevel,
    AuditOptions,
)
from app.core.audit.exceptions import AuditBackendException, AuditManagerException
from app.core.audit.utils import get_event_level_mapping, get_sensitive_fields
from app.core.base import CoreManager
from app.core.config import settings
from app.logging import get_logger

logger = get_logger("app.core.audit.manager")


class AuditManager(CoreManager):
    """Manager for audit backends.

    Provides a central point for accessing and managing different audit backends.
    """

    @property
    def component_name(self) -> str:
        """Get the component name.

        Returns:
            The component name.
        """
        return "audit"

    def __init__(self, db: Optional[AsyncSession] = None) -> None:
        """Initialize the audit manager.

        Args:
            db: Database session for database operations.
        """
        super().__init__()
        self.db = db
        self.backends: List[AuditBackend] = []
        self.enabled = getattr(settings, "AUDIT_LOGGING_ENABLED", True)
        self.event_level_mapping = get_event_level_mapping()
        self.sensitive_fields = get_sensitive_fields()
        self.anonymize_events = [
            AuditEventType.GDPR_DATA_EXPORT,
            AuditEventType.GDPR_DATA_DELETED,
        ]

    async def _initialize_manager(self) -> None:
        """Initialize manager-specific logic."""
        if not self.enabled:
            self.logger.info("Audit logging is disabled")
            return

        # Initialize backends
        try:
            self.backends = create_default_backends(self.db)

            for backend in self.backends:
                self.register_component(backend)

            self.logger.info(
                f"Initialized {len(self.backends)} audit backends: "
                f"{', '.join([b.__class__.__name__ for b in self.backends])}"
            )
        except Exception as e:
            self.logger.error(
                f"Failed to initialize audit backends: {str(e)}", exc_info=True
            )
            raise AuditBackendException(
                backend_name="manager",
                operation="initialize",
                message="Failed to initialize audit backends",
                original_exception=e,
            )

        # Log system start event
        await self.log_event(
            event_type=AuditEventType.SYSTEM_STARTED,
            level=AuditLogLevel.INFO,
            context=AuditContext(),
            details={"service": "AuditManager", "action": "initialize"},
        )

    async def _shutdown_manager(self) -> None:
        """Shut down manager-specific logic."""
        if self.enabled:
            # Log system stop event
            await self.log_event(
                event_type=AuditEventType.SYSTEM_STOPPED,
                level=AuditLogLevel.INFO,
                context=AuditContext(),
                details={"service": "AuditManager", "action": "shutdown"},
            )

    def add_backend(self, backend: AuditBackend) -> None:
        """Add an audit backend to the manager.

        Args:
            backend: Backend to add.
        """
        self.backends.append(backend)
        self.register_component(backend)
        self.logger.debug(f"Added audit backend: {backend.__class__.__name__}")

    async def log_event(
        self,
        event_type: AuditEventType,
        level: Optional[AuditLogLevel] = None,
        context: Optional[AuditContext] = None,
        details: Optional[Dict[str, Any]] = None,
        options: Optional[AuditOptions] = None,
    ) -> str:
        """Log an audit event to all backends.

        Args:
            event_type: Type of event being logged.
            level: Log level for the event.
            context: Context information for the event.
            details: Additional event details.
            options: Options for logging the event.

        Returns:
            ID of the logged event.
        """
        if not self.enabled:
            return "disabled"

        if not self.backends:
            self.logger.warning("No audit backends configured")
            return "no-backends"

        # Set default values
        actual_level = level or self.event_level_mapping.get(
            event_type, AuditLogLevel.INFO
        )
        actual_context = context or AuditContext()
        actual_options = options or AuditOptions(
            sensitive_fields=self.sensitive_fields,
            anonymize_data=event_type in self.anonymize_events,
        )

        # Log to all backends
        event_id = None
        for backend in self.backends:
            try:
                backend_event_id = await backend.log_event(
                    event_type=event_type,
                    level=actual_level,
                    context=actual_context,
                    details=details,
                    options=actual_options,
                )
                if event_id is None:
                    event_id = backend_event_id
            except Exception as e:
                self.logger.error(
                    f"Error in audit backend {backend.__class__.__name__}: {str(e)}",
                    exc_info=True,
                )

        return event_id or "error"

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
        if not self.enabled:
            return {"total": 0, "items": []}

        if not self.db:
            return {
                "total": 0,
                "items": [],
                "error": "Database connection not available",
            }

        try:
            from app.core.audit.models import AuditLog

            # Build query
            query = select(AuditLog)

            # Apply filters
            if start_time:
                start_datetime = datetime.datetime.fromisoformat(
                    start_time.replace("Z", "+00:00")
                )
                query = query.filter(AuditLog.timestamp >= start_datetime)

            if end_time:
                end_datetime = datetime.datetime.fromisoformat(
                    end_time.replace("Z", "+00:00")
                )
                query = query.filter(AuditLog.timestamp <= end_datetime)

            if event_type:
                query = query.filter(AuditLog.event_type == event_type)

            if level:
                query = query.filter(AuditLog.level == level)

            if user_id:
                query = query.filter(AuditLog.user_id == uuid.UUID(user_id))

            if resource_id:
                query = query.filter(AuditLog.resource_id == uuid.UUID(resource_id))

            if resource_type:
                query = query.filter(AuditLog.resource_type == resource_type)

            # Get total count
            count_query = select(func.count()).select_from(query.subquery())
            count_result = await self.db.execute(count_query)
            total = count_result.scalar() or 0

            # Apply pagination and sorting
            query = query.order_by(desc(AuditLog.timestamp))
            query = query.offset(offset).limit(limit)

            # Execute query
            result = await self.db.execute(query)
            logs = result.scalars().all()

            # Convert to dictionaries
            items = [log.to_dict() for log in logs]

            return {"total": total, "items": items}
        except Exception as e:
            self.logger.error(f"Error retrieving audit events: {str(e)}", exc_info=True)
            raise AuditManagerException(
                operation="get_events",
                message="Error retrieving audit events",
                original_exception=e,
            )

    async def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get an audit event by ID.

        Args:
            event_id: ID of the event to get.

        Returns:
            Event details or None if not found.
        """
        if not self.enabled:
            return None

        if not self.db:
            return None

        try:
            from app.core.audit.models import AuditLog

            # Build query
            query = select(AuditLog).filter(AuditLog.id == uuid.UUID(event_id))

            # Execute query
            result = await self.db.execute(query)
            log = result.scalar_one_or_none()

            if log:
                return log.to_dict()

            return None
        except Exception as e:
            self.logger.error(
                f"Error retrieving audit event by ID: {str(e)}", exc_info=True
            )
            raise AuditManagerException(
                operation="get_event_by_id",
                message="Error retrieving audit event by ID",
                details={"event_id": event_id},
                original_exception=e,
            )

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
        if not self.enabled:
            return []

        if not self.db:
            return []

        result = await self.get_events(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

        return result.get("items", [])

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
        if not self.enabled:
            return []

        if not self.db:
            return []

        result = await self.get_events(
            resource_type=resource_type,
            resource_id=resource_id,
            limit=limit,
        )

        return result.get("items", [])

    async def purge_old_logs(self, days_to_keep: int = 90) -> int:
        """Delete audit logs older than the specified number of days.

        Args:
            days_to_keep: Number of days to keep logs for.

        Returns:
            Number of logs deleted.
        """
        if not self.enabled:
            return 0

        if not self.db:
            return 0

        try:
            from app.core.audit.models import AuditLog

            # Calculate cutoff date
            cutoff_date = datetime.datetime.now(
                datetime.timezone.utc
            ) - datetime.timedelta(days=days_to_keep)

            # Build delete statement
            delete_stmt = delete(AuditLog).where(AuditLog.timestamp < cutoff_date)

            # Execute statement
            result = await self.db.execute(delete_stmt)
            await self.db.commit()

            deleted_count = result.rowcount
            self.logger.info(
                f"Purged {deleted_count} audit logs older than {cutoff_date.isoformat()}"
            )

            # Log purge event
            await self.log_event(
                event_type=AuditEventType.DATA_DELETED,
                level=AuditLogLevel.WARNING,
                context=AuditContext(),
                details={
                    "action": "purge_old_logs",
                    "days_kept": days_to_keep,
                    "cutoff_date": cutoff_date.isoformat(),
                    "records_deleted": deleted_count,
                },
            )

            return deleted_count
        except Exception as e:
            self.logger.error(f"Error purging old audit logs: {str(e)}", exc_info=True)
            await self.db.rollback()
            raise AuditManagerException(
                operation="purge_old_logs",
                message="Error purging old audit logs",
                details={"days_to_keep": days_to_keep},
                original_exception=e,
            )
