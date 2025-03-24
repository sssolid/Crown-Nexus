# /app/services/audit/loggers.py
from __future__ import annotations

"""Audit logger implementations.

This module provides different implementations of the AuditLogger protocol
for logging audit events to various destinations.
"""

import json
import uuid
import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.services.audit.base import (
    AuditContext,
    AuditEventType,
    AuditLogLevel,
    AuditLogger,
    AuditOptions,
)

logger = get_logger("app.services.audit.loggers")


class BaseAuditLogger:
    """Base class for audit loggers with common functionality."""

    def __init__(self) -> None:
        """Initialize the base audit logger."""
        self.logger = logger

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

        # Map event types to log levels
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

    def _get_log_level(
        self, event_type: AuditEventType, level: Optional[AuditLogLevel] = None
    ) -> AuditLogLevel:
        """Get the appropriate log level for an event type.

        Args:
            event_type: Type of the audit event
            level: Explicitly provided level (takes precedence)

        Returns:
            AuditLogLevel: The determined log level
        """
        if level is not None:
            return level

        return self.event_level_mapping.get(event_type, AuditLogLevel.INFO)

    def _anonymize_data(
        self, data: Dict[str, Any], sensitive_fields: List[str]
    ) -> Dict[str, Any]:
        """Anonymize sensitive data in audit logs.

        Args:
            data: The data to anonymize
            sensitive_fields: List of field names to anonymize

        Returns:
            Dict[str, Any]: Anonymized data dictionary
        """
        if not data:
            return {}

        anonymized = {}

        for key, value in data.items():
            # Check if field name contains any sensitive keywords
            is_sensitive = any(
                sensitive in key.lower() for sensitive in sensitive_fields
            )

            if is_sensitive:
                if isinstance(value, str):
                    # Mask string values with asterisks
                    if len(value) <= 4:
                        anonymized[key] = "****"
                    else:
                        # Keep first and last character, mask the rest
                        anonymized[key] = value[0] + "*" * (len(value) - 2) + value[-1]
                else:
                    # Replace with generic placeholder for non-strings
                    anonymized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                # Recursively process nested dictionaries
                anonymized[key] = self._anonymize_data(value, sensitive_fields)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # Recursively process lists of dictionaries
                anonymized[key] = [
                    (
                        self._anonymize_data(item, sensitive_fields)
                        if isinstance(item, dict)
                        else item
                    )
                    for item in value
                ]
            else:
                # Keep non-sensitive data as is
                anonymized[key] = value

        return anonymized

    def _prepare_log_entry(
        self,
        event_id: str,
        event_type: AuditEventType,
        level: AuditLogLevel,
        user_id: Optional[str],
        ip_address: Optional[str],
        resource_id: Optional[str],
        resource_type: Optional[str],
        details: Optional[Dict[str, Any]],
        context: Optional[AuditContext],
        options: Optional[AuditOptions],
    ) -> Dict[str, Any]:
        """Prepare a standardized log entry.

        Args:
            event_id: Generated event ID
            event_type: Type of the audit event
            level: Severity level of the event
            user_id: ID of the user who performed the action
            ip_address: IP address of the user
            resource_id: ID of the resource affected
            resource_type: Type of the resource affected
            details: Additional details about the event
            context: Additional context information
            options: Audit logging options

        Returns:
            Dict[str, Any]: Standardized log entry
        """
        timestamp = datetime.datetime.now(datetime.UTC).isoformat() + "Z"

        # Use context values if provided, otherwise use direct parameters
        ctx = context or AuditContext()
        ctx_user_id = ctx.user_id or user_id
        ctx_ip = ctx.ip_address or ip_address
        ctx_resource_id = ctx.resource_id or resource_id
        ctx_resource_type = ctx.resource_type or resource_type

        # Prepare audit details
        audit_details = details or {}

        # Process options
        opts = options or AuditOptions()
        should_anonymize = opts.anonymize_data or event_type in self.anonymize_events
        sensitive_fields = opts.sensitive_fields or self.sensitive_fields

        # Anonymize sensitive data if needed
        if should_anonymize and audit_details:
            audit_details = self._anonymize_data(audit_details, sensitive_fields)

        # Prepare log entry
        log_entry: Dict[str, Any] = {
            "id": event_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "level": level,
            "user_id": ctx_user_id,
            "ip_address": ctx_ip,
            "resource_id": ctx_resource_id,
            "resource_type": ctx_resource_type,
            "details": audit_details,
        }

        # Add additional context if provided
        if context:
            for key, value in context.model_dump(exclude_none=True).items():
                if key not in log_entry and key not in [
                    "user_id",
                    "ip_address",
                    "resource_id",
                    "resource_type",
                ]:
                    log_entry[key] = value

        return log_entry


class LoggingAuditLogger(BaseAuditLogger, AuditLogger):
    """Audit logger that logs events to the application logging system."""

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
        """Log an audit event to the application logging system.

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
            str: The ID of the created audit event
        """
        # Generate event ID
        event_id = str(uuid.uuid4())

        # Determine log level
        log_level = self._get_log_level(event_type, level)

        # Prepare log entry
        log_entry = self._prepare_log_entry(
            event_id,
            event_type,
            log_level,
            user_id,
            ip_address,
            resource_id,
            resource_type,
            details,
            context,
            options,
        )

        # Create log message
        log_message = f"AUDIT: {event_type} by user {log_entry['user_id']} from {log_entry['ip_address']}"

        # Log to application logs with appropriate level
        if log_level == AuditLogLevel.INFO:
            self.logger.info(log_message, extra=log_entry)
        elif log_level == AuditLogLevel.WARNING:
            self.logger.warning(log_message, extra=log_entry)
        elif log_level == AuditLogLevel.ERROR:
            self.logger.error(log_message, extra=log_entry)
        elif log_level == AuditLogLevel.CRITICAL:
            self.logger.critical(log_message, extra=log_entry)

        return event_id


class FileAuditLogger(BaseAuditLogger, AuditLogger):
    """Audit logger that logs events to a file."""

    def __init__(self, file_path: str) -> None:
        """Initialize the file audit logger.

        Args:
            file_path: Path to the audit log file
        """
        super().__init__()
        self.file_path = file_path

        # Ensure log directory exists
        import os
        from pathlib import Path

        log_dir = Path(file_path).parent
        os.makedirs(log_dir, exist_ok=True)

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
        """Log an audit event to a file.

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
            str: The ID of the created audit event
        """
        # Generate event ID
        event_id = str(uuid.uuid4())

        # Determine log level
        log_level = self._get_log_level(event_type, level)

        # Prepare log entry
        log_entry = self._prepare_log_entry(
            event_id,
            event_type,
            log_level,
            user_id,
            ip_address,
            resource_id,
            resource_type,
            details,
            context,
            options,
        )

        try:
            # Serialize log entry to JSON
            log_line = json.dumps(log_entry)

            # Write to file
            with open(self.file_path, "a") as f:
                f.write(log_line + "\n")

            self.logger.debug(f"Audit log saved to file: {event_id}")

        except Exception as e:
            self.logger.error(f"Failed to write audit log to file: {str(e)}")

        return event_id


class DatabaseAuditLogger(BaseAuditLogger, AuditLogger):
    """Audit logger that logs events to the database."""

    def __init__(self, db: Optional[AsyncSession] = None) -> None:
        """Initialize the database audit logger.

        Args:
            db: Database session for database operations
        """
        super().__init__()
        self.db = db

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
        """Log an audit event to the database.

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
            str: The ID of the created audit event
        """
        # If no DB session, return early
        if not self.db:
            self.logger.warning(
                "No database session provided for database audit logger"
            )
            return str(uuid.uuid4())

        # Generate event ID
        event_id = str(uuid.uuid4())

        # Determine log level
        log_level = self._get_log_level(event_type, level)

        # Prepare log entry
        log_entry = self._prepare_log_entry(
            event_id,
            event_type,
            log_level,
            user_id,
            ip_address,
            resource_id,
            resource_type,
            details,
            context,
            options,
        )

        try:
            # Import the AuditLog model here to avoid circular imports
            from app.domains.audit.models import AuditLog

            # Create a new AuditLog instance
            audit_log = AuditLog(
                id=uuid.UUID(log_entry["id"]),
                timestamp=datetime.fromisoformat(log_entry["timestamp"].rstrip("Z")),
                event_type=log_entry["event_type"],
                level=log_entry["level"],
                user_id=(
                    uuid.UUID(log_entry["user_id"])
                    if log_entry.get("user_id")
                    else None
                ),
                ip_address=log_entry.get("ip_address"),
                resource_id=(
                    uuid.UUID(log_entry["resource_id"])
                    if log_entry.get("resource_id")
                    else None
                ),
                resource_type=log_entry.get("resource_type"),
                details=log_entry.get("details", {}),
                request_id=log_entry.get("request_id"),
                user_agent=log_entry.get("user_agent"),
                session_id=log_entry.get("session_id"),
                company_id=(
                    uuid.UUID(log_entry["company_id"])
                    if log_entry.get("company_id")
                    else None
                ),
            )

            # Add to session and commit
            self.db.add(audit_log)
            await self.db.commit()

            self.logger.debug(f"Audit log saved to database: {event_id}")

        except Exception as e:
            self.logger.error(f"Failed to write audit log to database: {str(e)}")
            await self.db.rollback()

        return event_id
