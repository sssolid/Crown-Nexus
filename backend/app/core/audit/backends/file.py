from __future__ import annotations

"""
File backend for audit events.

This module provides a backend that logs audit events to a file.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from app.core.audit.base import (
    AuditBackend,
    AuditContext,
    AuditEventType,
    AuditLogLevel,
    AuditOptions,
)
from app.core.audit.exceptions import AuditBackendException
from app.core.audit.utils import anonymize_data
from app.core.base import InitializableComponent
from app.logging import get_logger

logger = get_logger("app.core.audit.backends.file")


class FileAuditBackend(AuditBackend, InitializableComponent):
    """Audit backend that logs to a file."""

    __backend_name__ = "file"

    def __init__(self, file_path: str = "/var/log/app/audit.log") -> None:
        """Initialize the file audit backend.

        Args:
            file_path: Path to the log file.
        """
        self.file_path = file_path
        self.log_dir = Path(file_path).parent

    async def initialize(self) -> None:
        """Initialize the backend.

        This ensures the log directory exists.
        """
        try:
            os.makedirs(self.log_dir, exist_ok=True)
            logger.info(f"File audit backend initialized with path: {self.file_path}")
        except Exception as e:
            raise AuditBackendException(
                backend_name="file",
                message=f"Failed to create log directory: {self.log_dir}",
                original_exception=e,
            )

    async def shutdown(self) -> None:
        """Shut down the backend."""
        logger.info("File audit backend shut down")

    async def log_event(
        self,
        event_type: AuditEventType,
        level: AuditLogLevel,
        context: AuditContext,
        details: Optional[Dict[str, Any]] = None,
        options: Optional[AuditOptions] = None,
    ) -> str:
        """Log an audit event to a file.

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

        # Write to file
        try:
            with open(self.file_path, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            logger.debug(f"Audit event {event_id} written to file")
        except Exception as e:
            logger.error(f"Failed to write audit event to file: {str(e)}")
            raise AuditBackendException(
                backend_name="file",
                message="Failed to write audit event to file",
                details={"event_id": event_id, "file_path": self.file_path},
                original_exception=e,
            )

        return event_id

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check.

        Returns:
            Dict containing health status information.
        """
        try:
            # Check if the file is writable
            with open(self.file_path, "a") as f:
                pass

            # Get file size
            file_size = (
                Path(self.file_path).stat().st_size
                if Path(self.file_path).exists()
                else 0
            )

            return {
                "status": "healthy",
                "backend": "file",
                "file_path": self.file_path,
                "file_size": file_size,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "backend": "file",
                "file_path": self.file_path,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
