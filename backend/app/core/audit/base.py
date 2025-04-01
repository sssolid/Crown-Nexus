from __future__ import annotations

"""
Base interfaces and types for the audit system.

This module defines common types, protocols, and interfaces
used throughout the audit service components.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, TypeVar

from pydantic import BaseModel, Field

from app.core.base import CoreBackend

T = TypeVar("T")


class AuditEventType(str, Enum):
    """Types of events that can be audited."""

    # Authentication events
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_RESET_REQUESTED = "password_reset_requested"
    PASSWORD_RESET_COMPLETED = "password_reset_completed"
    MFA_ENABLED = "mfa_enabled"
    MFA_DISABLED = "mfa_disabled"
    SESSION_EXPIRED = "session_expired"

    # API key events
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

    # Payment events
    PAYMENT_RECEIVED = "payment_received"
    PAYMENT_REFUNDED = "payment_refunded"

    # Data events
    DATA_EXPORTED = "data_exported"
    DATA_IMPORTED = "data_imported"
    DATA_DELETED = "data_deleted"
    REPORT_GENERATED = "report_generated"

    # System events
    SYSTEM_STARTED = "system_started"
    SYSTEM_STOPPED = "system_stopped"
    MAINTENANCE_MODE_ENABLED = "maintenance_mode_enabled"
    MAINTENANCE_MODE_DISABLED = "maintenance_mode_disabled"

    # GDPR events
    GDPR_DATA_EXPORT = "gdpr_data_export"
    GDPR_DATA_DELETED = "gdpr_data_deleted"


class AuditLogLevel(str, Enum):
    """Log levels for audit events."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditContext(BaseModel):
    """Context information for audit events."""

    user_id: Optional[str] = Field(None, description="ID of the user who performed the action")
    ip_address: Optional[str] = Field(None, description="IP address the action was performed from")
    user_agent: Optional[str] = Field(None, description="User agent of the client")
    session_id: Optional[str] = Field(None, description="Session ID")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")
    company_id: Optional[str] = Field(None, description="Company context ID")
    resource_id: Optional[str] = Field(None, description="ID of the affected resource")
    resource_type: Optional[str] = Field(None, description="Type of the affected resource")
    before_state: Optional[Dict[str, Any]] = Field(None, description="Resource state before change")
    after_state: Optional[Dict[str, Any]] = Field(None, description="Resource state after change")
    changes: Optional[Dict[str, Any]] = Field(None, description="Changes made to the resource")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class AuditOptions(BaseModel):
    """Options for audit logging."""

    include_request_body: bool = Field(False, description="Include request body in the audit log")
    sensitive_fields: List[str] = Field(default_factory=list, description="Sensitive fields to redact")
    anonymize_data: bool = Field(False, description="Anonymize sensitive data")
    capture_before_after: bool = Field(False, description="Capture before/after state")
    retention_period: int = Field(90, description="Retention period in days")


class AuditBackend(CoreBackend, Protocol):
    """Protocol for audit backends."""

    async def log_event(
        self,
        event_type: AuditEventType,
        level: AuditLogLevel,
        context: AuditContext,
        details: Optional[Dict[str, Any]] = None,
        options: Optional[AuditOptions] = None,
    ) -> str:
        """Log an audit event.

        Args:
            event_type: Type of event being logged.
            level: Log level for the event.
            context: Context information for the event.
            details: Additional event details.
            options: Options for logging the event.

        Returns:
            ID of the logged event.
        """
        ...
