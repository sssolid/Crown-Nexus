# /app/services/audit/service.py
from __future__ import annotations

"""Main audit service implementation.

This module provides the primary AuditService that coordinates audit logging
and querying operations.
"""

import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.logging import get_logger
from app.domains.audit.service.base import (
    AuditContext,
    AuditEventType,
    AuditLogLevel,
    AuditLogger,
    AuditOptions,
)
from app.domains.audit.service.factory import AuditLoggerFactory
from app.domains.audit.service.query import AuditQuery
from app.services.interfaces import ServiceInterface

logger = get_logger("app.domains.audit.service.service")


class AuditService(ServiceInterface):
    """Service for recording and retrieving audit logs.

    This service provides methods for logging user and system actions
    for security, compliance, and troubleshooting purposes.
    """

    def __init__(self, db: Optional[AsyncSession] = None) -> None:
        """Initialize the audit service.

        Args:
            db: Optional database session
        """
        self.db = db
        self.enabled = getattr(settings, "AUDIT_LOGGING_ENABLED", True)
        self.loggers: List[AuditLogger] = []

        # Default sensitive fields to mask
        self.sensitive_fields: List[str] = [
            "password",
            "token",
            "secret",
            "credit_card",
            "ssn",
            "social_security",
            "api_key",
        ]

        # Event types that should be anonymized by default
        self.anonymize_events: List[AuditEventType] = [
            AuditEventType.GDPR_DATA_EXPORT,
            AuditEventType.GDPR_DATA_DELETED,
        ]

        # Default event level mapping
        self.event_level_mapping: Dict[AuditEventType, AuditLogLevel] = {
            AuditEventType.ACCESS_DENIED: AuditLogLevel.WARNING,
            AuditEventType.LOGIN_FAILED: AuditLogLevel.WARNING,
            AuditEventType.USER_DELETED: AuditLogLevel.WARNING,
            AuditEventType.API_KEY_REVOKED: AuditLogLevel.WARNING,
            AuditEventType.PAYMENT_REFUNDED: AuditLogLevel.WARNING,
            AuditEventType.DATA_DELETED: AuditLogLevel.WARNING,
            AuditEventType.CHAT_MESSAGE_DELETED: AuditLogLevel.INFO,
            AuditEventType.GDPR_DATA_DELETED: AuditLogLevel.WARNING,
            AuditEventType.SYSTEM_STOPPED: AuditLogLevel.WARNING,
            AuditEventType.MAINTENANCE_MODE_ENABLED: AuditLogLevel.WARNING,
        }

        # Initialize query functionality if db is provided
        self.query = AuditQuery(db) if db else None

        logger.info("AuditService initialized")

    async def initialize(self) -> None:
        """Initialize the audit service."""
        logger.debug("Initializing audit service")

        # Create default loggers based on configuration
        self.loggers = AuditLoggerFactory.create_default_loggers(self.db)

        # Log service initialization
        if self.enabled:
            await self.log_event(
                event_type=AuditEventType.SYSTEM_STARTED,
                details={"service": "AuditService", "action": "initialize"},
            )

    async def shutdown(self) -> None:
        """Shutdown the audit service."""
        logger.debug("Shutting down audit service")

        if self.enabled:
            await self.log_event(
                event_type=AuditEventType.SYSTEM_STOPPED,
                details={"service": "AuditService", "action": "shutdown"},
            )

    def add_logger(self, logger: AuditLogger) -> None:
        """Add an audit logger to the service.

        Args:
            logger: The audit logger to add
        """
        self.loggers.append(logger)
        logger.debug(f"Added audit logger: {logger.__class__.__name__}")

    async def log_event(
        self,
        event_type: AuditEventType,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        context: Optional[AuditContext] = None,
        level: Optional[AuditLogLevel] = None,
        options: Optional[AuditOptions] = None,
    ) -> str:
        """Log an audit event.

        Args:
            event_type: Type of the audit event
            user_id: ID of the user who performed the action
            ip_address: IP address of the user
            resource_id: ID of the resource affected
            resource_type: Type of the resource affected
            details: Additional details about the event
            context: Additional context information
            level: Severity level of the event
            options: Audit logging options

        Returns:
            The ID of the created audit event
        """
        if not self.enabled:
            return "disabled"

        if not self.loggers:
            logger.warning("No audit loggers configured")
            return "no-loggers"

        # Determine the level if not provided
        if level is None:
            level = self.event_level_mapping.get(event_type, AuditLogLevel.INFO)

        # Create options if not provided
        if options is None:
            options = AuditOptions(
                sensitive_fields=self.sensitive_fields,
                anonymize_data=event_type in self.anonymize_events,
            )

        # Log through all registered loggers
        event_id = None

        for audit_logger in self.loggers:
            try:
                logger_event_id = await audit_logger.log_event(
                    event_type=event_type,
                    user_id=user_id,
                    ip_address=ip_address,
                    resource_id=resource_id,
                    resource_type=resource_type,
                    details=details,
                    context=context,
                    level=level,
                    options=options,
                )

                # Use the first logger's event ID as the return value
                if event_id is None:
                    event_id = logger_event_id

            except Exception as e:
                logger.error(f"Error in audit logger: {str(e)}")

        return event_id or "error"

    async def get_events(
        self,
        user_id: Optional[str] = None,
        event_type: Optional[AuditEventType] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[AuditLogLevel] = None,
        limit: int = 100,
        offset: int = 0,
        sort_field: str = "timestamp",
        sort_order: str = "desc",
    ) -> Dict[str, Any]:
        """Retrieve audit events with filtering.

        Args:
            user_id: Filter by user ID
            event_type: Filter by event type
            resource_id: Filter by resource ID
            resource_type: Filter by resource type
            start_time: Filter by start time
            end_time: Filter by end time
            level: Filter by log level
            limit: Maximum number of results to return
            offset: Result offset for pagination
            sort_field: Field to sort by
            sort_order: Sort order ("asc" or "desc")

        Returns:
            Dictionary with audit log events and total count
        """
        if not self.enabled:
            return {"total": 0, "items": []}

        if not self.query:
            return {"total": 0, "items": [], "error": "Database querying not available"}

        return await self.query.get_events(
            user_id=user_id,
            event_type=event_type,
            resource_id=resource_id,
            resource_type=resource_type,
            start_time=start_time,
            end_time=end_time,
            level=level,
            limit=limit,
            offset=offset,
            sort_field=sort_field,
            sort_order=sort_order,
        )

    async def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific audit event by ID.

        Args:
            event_id: The ID of the audit event to retrieve

        Returns:
            The audit event or None if not found
        """
        if not self.enabled:
            return None

        if not self.query:
            return None

        return await self.query.get_event_by_id(event_id)

    async def get_user_activity(
        self,
        user_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get recent activity for a specific user.

        Args:
            user_id: The ID of the user
            start_time: Optional start time filter
            end_time: Optional end time filter
            limit: Maximum number of results to return

        Returns:
            List of audit events for the user
        """
        if not self.enabled:
            return []

        if not self.query:
            return []

        return await self.query.get_user_activity(
            user_id=user_id, start_time=start_time, end_time=end_time, limit=limit
        )

    async def get_resource_history(
        self, resource_type: str, resource_id: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get history of actions performed on a specific resource.

        Args:
            resource_type: The type of resource
            resource_id: The ID of the resource
            limit: Maximum number of results to return

        Returns:
            List of audit events for the resource
        """
        if not self.enabled:
            return []

        if not self.query:
            return []

        return await self.query.get_resource_history(
            resource_type=resource_type, resource_id=resource_id, limit=limit
        )

    async def purge_old_logs(self, days_to_keep: int = 90) -> int:
        """Purge audit logs older than the specified number of days.

        Args:
            days_to_keep: Number of days of logs to keep

        Returns:
            Number of purged log entries
        """
        if not self.enabled:
            return 0

        if not self.query:
            return 0

        deleted_count = await self.query.purge_old_logs(days_to_keep)

        # Log the purge action
        await self.log_event(
            event_type=AuditEventType.DATA_DELETED,
            details={
                "action": "purge_old_logs",
                "days_kept": days_to_keep,
                "cutoff_date": (
                    datetime.datetime.now(datetime.UTC)
                    - datetime.timedelta(days=days_to_keep)
                ).isoformat(),
                "records_deleted": deleted_count,
            },
            level=AuditLogLevel.WARNING,
        )

        return deleted_count
