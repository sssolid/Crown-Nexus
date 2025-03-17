# app/services/audit_service.py
from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union, TypedDict

from sqlalchemy import and_, desc, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.db.utils import execute_query
from app.services.interfaces import ServiceInterface
from app.models.audit import AuditLog  # Assuming we have this model

logger = get_logger("app.services.audit")


class AuditEventType(str, Enum):
    """Enum for different types of audit events."""

    # Authentication events
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_RESET_REQUESTED = "password_reset_requested"
    PASSWORD_RESET_COMPLETED = "password_reset_completed"
    MFA_ENABLED = "mfa_enabled"
    MFA_DISABLED = "mfa_disabled"
    SESSION_EXPIRED = "session_expired"
    API_KEY_CREATED = "api_key_created"
    API_KEY_REVOKED = "api_key_revoked"

    # User management events
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    USER_ACTIVATED = "user_activated"
    USER_DEACTIVATED = "user_deactivated"
    PASSWORD_CHANGED = "password_changed"
    EMAIL_CHANGED = "email_changed"
    USER_PROFILE_UPDATED = "user_profile_updated"

    # Permission events
    PERMISSION_CHANGED = "permission_changed"
    ROLE_ASSIGNED = "role_assigned"
    ROLE_REVOKED = "role_revoked"
    ACCESS_DENIED = "access_denied"

    # Product events
    PRODUCT_CREATED = "product_created"
    PRODUCT_UPDATED = "product_updated"
    PRODUCT_DELETED = "product_deleted"
    PRODUCT_ACTIVATED = "product_activated"
    PRODUCT_DEACTIVATED = "product_deactivated"
    PRICE_CHANGED = "price_changed"
    INVENTORY_UPDATED = "inventory_updated"

    # Order events
    ORDER_CREATED = "order_created"
    ORDER_UPDATED = "order_updated"
    ORDER_CANCELED = "order_canceled"
    ORDER_SHIPPED = "order_shipped"
    PAYMENT_RECEIVED = "payment_received"
    PAYMENT_REFUNDED = "payment_refunded"

    # Data events
    DATA_EXPORTED = "data_exported"
    DATA_IMPORTED = "data_imported"
    DATA_DELETED = "data_deleted"
    REPORT_GENERATED = "report_generated"

    # Settings events
    SETTINGS_CHANGED = "settings_changed"
    CONFIGURATION_CHANGED = "configuration_changed"
    FEATURE_ENABLED = "feature_enabled"
    FEATURE_DISABLED = "feature_disabled"

    # Media events
    FILE_UPLOADED = "file_uploaded"
    FILE_DOWNLOADED = "file_downloaded"
    FILE_DELETED = "file_deleted"

    # Communication events
    EMAIL_SENT = "email_sent"
    SMS_SENT = "sms_sent"
    NOTIFICATION_SENT = "notification_sent"

    # Chat events
    CHAT_ROOM_CREATED = "chat_room_created"
    CHAT_MESSAGE_SENT = "chat_message_sent"
    CHAT_MESSAGE_EDITED = "chat_message_edited"
    CHAT_MESSAGE_DELETED = "chat_message_deleted"
    CHAT_MEMBER_ADDED = "chat_member_added"
    CHAT_MEMBER_REMOVED = "chat_member_removed"

    # Integration events
    EXTERNAL_API_CALLED = "external_api_called"
    WEBHOOK_RECEIVED = "webhook_received"
    WEBHOOK_PROCESSED = "webhook_processed"

    # System events
    SYSTEM_STARTED = "system_started"
    SYSTEM_STOPPED = "system_stopped"
    BACKUP_CREATED = "backup_created"
    BACKUP_RESTORED = "backup_restored"
    MAINTENANCE_MODE_ENABLED = "maintenance_mode_enabled"
    MAINTENANCE_MODE_DISABLED = "maintenance_mode_disabled"

    # Compliance events
    GDPR_DATA_EXPORT = "gdpr_data_export"
    GDPR_DATA_DELETED = "gdpr_data_deleted"
    TERMS_ACCEPTED = "terms_accepted"
    PRIVACY_POLICY_ACCEPTED = "privacy_policy_accepted"


class AuditLogLevel(str, Enum):
    """Enum for audit log severity levels."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditContext(TypedDict, total=False):
    """TypedDict for audit context details."""

    user_id: str
    ip_address: str
    user_agent: str
    session_id: str
    request_id: str
    company_id: str
    resource_id: str
    resource_type: str
    before_state: Dict[str, Any]
    after_state: Dict[str, Any]
    changes: Dict[str, Any]
    metadata: Dict[str, Any]


class AuditOptions(TypedDict, total=False):
    """TypedDict for audit options."""

    include_request_body: bool
    sensitive_fields: List[str]
    anonymize_data: bool
    capture_before_after: bool
    retention_period: int


class AuditService:
    """Service for recording and retrieving audit logs.

    This service provides methods for logging user and system actions
    for security, compliance, and troubleshooting purposes.
    """

    def __init__(self, db: Optional[AsyncSession] = None) -> None:
        """Initialize the audit service.

        Args:
            db: Optional database session
        """
        self.db: Optional[AsyncSession] = db
        self.enabled: bool = settings.security.AUDIT_LOGGING_ENABLED
        self.log_to_db: bool = settings.security.AUDIT_LOG_TO_DB
        self.log_to_file: bool = settings.security.AUDIT_LOG_TO_FILE
        self.audit_log_file: str = settings.security.AUDIT_LOG_FILE

        # Define which event types require specific log levels
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

        # Define which event types should be anonymized
        self.anonymize_events: List[AuditEventType] = [
            AuditEventType.GDPR_DATA_EXPORT,
            AuditEventType.GDPR_DATA_DELETED
        ]

        # Default sensitive fields to mask
        self.sensitive_fields: List[str] = [
            "password",
            "token",
            "secret",
            "credit_card",
            "ssn",
            "social_security",
            "api_key"
        ]

        logger.info("AuditService initialized")

    async def initialize(self) -> None:
        """Initialize the audit service."""
        logger.debug("Initializing audit service")
        if self.log_to_file:
            # Ensure log directory exists
            import os
            from pathlib import Path
            log_dir = Path(self.audit_log_file).parent
            os.makedirs(log_dir, exist_ok=True)

        # Log service initialization
        if self.enabled:
            await self.log_event(
                event_type=AuditEventType.SYSTEM_STARTED,
                details={"service": "AuditService", "action": "initialize"}
            )

    async def shutdown(self) -> None:
        """Shutdown the audit service."""
        logger.debug("Shutting down audit service")
        if self.enabled:
            await self.log_event(
                event_type=AuditEventType.SYSTEM_STOPPED,
                details={"service": "AuditService", "action": "shutdown"}
            )

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
            return str(uuid.uuid4())

        # Determine the level if not provided
        if level is None:
            level = self.event_level_mapping.get(event_type, AuditLogLevel.INFO)

        # Generate event ID
        event_id: str = str(uuid.uuid4())
        timestamp: str = datetime.utcnow().isoformat() + "Z"

        # Prepare context data
        ctx = context or {}
        ctx_user_id = ctx.get("user_id") or user_id
        ctx_ip = ctx.get("ip_address") or ip_address
        ctx_resource_id = ctx.get("resource_id") or resource_id
        ctx_resource_type = ctx.get("resource_type") or resource_type

        # Prepare audit details
        audit_details = details or {}

        # Process options
        opts = options or {}
        should_anonymize = opts.get("anonymize_data", False) or event_type in self.anonymize_events
        sensitive_fields = opts.get("sensitive_fields", self.sensitive_fields)

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
            for key, value in context.items():
                if key not in log_entry and key not in ["user_id", "ip_address", "resource_id", "resource_type"]:
                    log_entry[key] = value

        # Log to application logs
        log_message: str = f"AUDIT: {event_type} by user {ctx_user_id} from {ctx_ip}"

        # Use appropriate log level
        if level == AuditLogLevel.INFO:
            logger.info(log_message, extra=log_entry)
        elif level == AuditLogLevel.WARNING:
            logger.warning(log_message, extra=log_entry)
        elif level == AuditLogLevel.ERROR:
            logger.error(log_message, extra=log_entry)
        elif level == AuditLogLevel.CRITICAL:
            logger.critical(log_message, extra=log_entry)

        # Write to database if enabled
        if self.log_to_db and self.db:
            await self._log_to_database(log_entry)

        # Write to file if enabled
        if self.log_to_file:
            self._log_to_file(log_entry)

        return event_id

    async def _log_to_database(self, log_entry: Dict[str, Any]) -> None:
        """Save audit log entry to the database.

        Args:
            log_entry: The audit log entry to save
        """
        try:
            # Create a new AuditLog instance
            audit_log = AuditLog(
                id=uuid.UUID(log_entry["id"]),
                timestamp=datetime.fromisoformat(log_entry["timestamp"].rstrip("Z")),
                event_type=log_entry["event_type"],
                level=log_entry["level"],
                user_id=uuid.UUID(log_entry["user_id"]) if log_entry.get("user_id") else None,
                ip_address=log_entry.get("ip_address"),
                resource_id=uuid.UUID(log_entry["resource_id"]) if log_entry.get("resource_id") else None,
                resource_type=log_entry.get("resource_type"),
                details=log_entry.get("details", {}),
                request_id=log_entry.get("request_id"),
                user_agent=log_entry.get("user_agent"),
                session_id=log_entry.get("session_id"),
                company_id=uuid.UUID(log_entry["company_id"]) if log_entry.get("company_id") else None,
            )

            # Add to session and commit
            self.db.add(audit_log)
            await self.db.commit()
            logger.debug(f"Audit log saved to database: {log_entry['id']}")
        except Exception as e:
            logger.error(f"Failed to write audit log to database: {str(e)}")
            await self.db.rollback()

    def _log_to_file(self, log_entry: Dict[str, Any]) -> None:
        """Save audit log entry to a file.

        Args:
            log_entry: The audit log entry to save
        """
        try:
            log_line: str = json.dumps(log_entry)
            with open(self.audit_log_file, "a") as f:
                f.write(log_line + "\n")
            logger.debug(f"Audit log saved to file: {log_entry['id']}")
        except Exception as e:
            logger.error(f"Failed to write audit log to file: {str(e)}")

    def _anonymize_data(self, data: Dict[str, Any], sensitive_fields: List[str]) -> Dict[str, Any]:
        """Anonymize sensitive data in audit logs.

        Args:
            data: The data to anonymize
            sensitive_fields: List of field names to anonymize

        Returns:
            Anonymized data dictionary
        """
        if not data:
            return {}

        anonymized = {}

        for key, value in data.items():
            # Check if field name contains any sensitive keywords
            is_sensitive = any(sensitive in key.lower() for sensitive in sensitive_fields)

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
                    self._anonymize_data(item, sensitive_fields) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                # Keep non-sensitive data as is
                anonymized[key] = value

        return anonymized

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
        if not self.enabled or not self.log_to_db or not self.db:
            return {"total": 0, "items": []}

        try:
            # Build base query
            query = select(AuditLog)

            # Apply filters
            if user_id:
                query = query.filter(AuditLog.user_id == uuid.UUID(user_id))

            if event_type:
                query = query.filter(AuditLog.event_type == event_type)

            if resource_id:
                query = query.filter(AuditLog.resource_id == uuid.UUID(resource_id))

            if resource_type:
                query = query.filter(AuditLog.resource_type == resource_type)

            if level:
                query = query.filter(AuditLog.level == level)

            if start_time:
                query = query.filter(AuditLog.timestamp >= start_time)

            if end_time:
                query = query.filter(AuditLog.timestamp <= end_time)

            # Get total count
            count_query = select(func.count()).select_from(query.subquery())
            count_result = await self.db.execute(count_query)
            total = count_result.scalar() or 0

            # Apply sorting
            if sort_order.lower() == "desc":
                query = query.order_by(desc(getattr(AuditLog, sort_field)))
            else:
                query = query.order_by(getattr(AuditLog, sort_field))

            # Apply pagination
            query = query.offset(offset).limit(limit)

            # Execute query
            result = await self.db.execute(query)
            logs = result.scalars().all()

            # Convert to dictionaries
            items = [log.to_dict() for log in logs]

            return {"total": total, "items": items}
        except Exception as e:
            logger.error(f"Error retrieving audit events: {str(e)}")
            return {"total": 0, "items": [], "error": str(e)}

    async def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific audit event by ID.

        Args:
            event_id: The ID of the audit event to retrieve

        Returns:
            The audit event or None if not found
        """
        if not self.enabled or not self.log_to_db or not self.db:
            return None

        try:
            query = select(AuditLog).filter(AuditLog.id == uuid.UUID(event_id))
            result = await self.db.execute(query)
            log = result.scalar_one_or_none()

            if log:
                return log.to_dict()

            return None
        except Exception as e:
            logger.error(f"Error retrieving audit event by ID: {str(e)}")
            return None

    async def get_user_activity(
        self,
        user_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
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
        result = await self.get_events(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
            sort_field="timestamp",
            sort_order="desc"
        )
        return result.get("items", [])

    async def get_resource_history(
        self,
        resource_type: str,
        resource_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get history of actions performed on a specific resource.

        Args:
            resource_type: The type of resource
            resource_id: The ID of the resource
            limit: Maximum number of results to return

        Returns:
            List of audit events for the resource
        """
        result = await self.get_events(
            resource_id=resource_id,
            resource_type=resource_type,
            limit=limit,
            sort_field="timestamp",
            sort_order="desc"
        )
        return result.get("items", [])

    async def purge_old_logs(self, days_to_keep: int = 90) -> int:
        """Purge audit logs older than the specified number of days.

        Args:
            days_to_keep: Number of days of logs to keep

        Returns:
            Number of purged log entries
        """
        if not self.enabled or not self.log_to_db or not self.db:
            return 0

        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)

            # Create delete query
            delete_stmt = delete(AuditLog).where(AuditLog.timestamp < cutoff_date)

            # Execute query
            result = await self.db.execute(delete_stmt)
            await self.db.commit()

            deleted_count = result.rowcount
            logger.info(f"Purged {deleted_count} audit logs older than {cutoff_date}")

            # Log the purge action
            await self.log_event(
                event_type=AuditEventType.DATA_DELETED,
                details={
                    "action": "purge_old_logs",
                    "days_kept": days_to_keep,
                    "cutoff_date": cutoff_date.isoformat(),
                    "records_deleted": deleted_count
                },
                level=AuditLogLevel.WARNING
            )

            return deleted_count
        except Exception as e:
            logger.error(f"Error purging old audit logs: {str(e)}")
            await self.db.rollback()
            return 0
