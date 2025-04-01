from __future__ import annotations

"""
Logging backend for audit events.

This module provides a backend that logs audit events to the application logger.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.core.audit.base import AuditBackend, AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.core.audit.utils import anonymize_data
from app.logging import get_logger

logger = get_logger("app.core.audit.backends.logging")


class LoggingAuditBackend(AuditBackend):
    """Audit backend that logs to the application logger."""

    __backend_name__ = "logging"

    def __init__(self) -> None:
        """Initialize the logging audit backend."""
        self.logger = get_logger("app.audit")

    async def initialize(self) -> None:
        """Initialize the backend."""
        logger.info("Logging audit backend initialized")

    async def shutdown(self) -> None:
        """Shut down the backend."""
        logger.info("Logging audit backend shut down")

    async def log_event(
        self,
        event_type: AuditEventType,
        level: AuditLogLevel,
        context: AuditContext,
        details: Optional[Dict[str, Any]] = None,
        options: Optional[AuditOptions] = None,
    ) -> str:
        """Log an audit event to the application logger.

        Args:
            event_type: Type of event being logged.
            level: Log level for the event.
            context: Context information for the event.
            details: Additional event details.
            options: Options for logging the event.

        Returns:
            ID of the logged event.
        """
        options = options or AuditOptions()
        event_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        # Prepare log entry
        log_entry = {
            "id": event_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "level": level,
            **context.model_dump(exclude_none=True),
        }

        # Add details if provided
        if details:
            # Anonymize sensitive data if needed
            if options.anonymize_data:
                details = anonymize_data(details, options.sensitive_fields)
            log_entry["details"] = details

        # Create log message
        user_id = context.user_id or "system"
        ip_address = context.ip_address or "internal"
        log_message = f"AUDIT: {event_type} by {user_id} from {ip_address}"

        # Log with appropriate level
        if level == AuditLogLevel.INFO:
            self.logger.info(log_message, extra={"audit": log_entry})
        elif level == AuditLogLevel.WARNING:
            self.logger.warning(log_message, extra={"audit": log_entry})
        elif level == AuditLogLevel.ERROR:
            self.logger.error(log_message, extra={"audit": log_entry})
        elif level == AuditLogLevel.CRITICAL:
            self.logger.critical(log_message, extra={"audit": log_entry})

        return event_id

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check.

        Returns:
            Dict containing health status information.
        """
        return {
            "status": "healthy",
            "component": "logging_backend",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
