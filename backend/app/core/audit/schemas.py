from __future__ import annotations

"""
Audit schema definitions.

This module defines Pydantic schemas for audit log objects,
including creation, filtering, and response models.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AuditLogLevelEnum(str, Enum):
    """Log levels for audit events."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditEventTypeEnum(str, Enum):
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

    # System events
    SYSTEM_STARTED = "system_started"
    SYSTEM_STOPPED = "system_stopped"

    # Generic events for backward compatibility
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    VIEW = "view"
    EXPORT = "export"
    IMPORT = "import"
    API_ACCESS = "api_access"


class AuditLogBase(BaseModel):
    """Base schema for audit logs."""

    timestamp: datetime = Field(
        default_factory=datetime.now, description="Event timestamp"
    )
    event_type: str = Field(..., description="Event type")
    level: AuditLogLevelEnum = Field(
        AuditLogLevelEnum.INFO, description="Log level"
    )
    user_id: Optional[uuid.UUID] = Field(
        None, description="User who performed the action"
    )
    ip_address: Optional[str] = Field(
        None, description="IP address of the user"
    )
    resource_id: Optional[uuid.UUID] = Field(
        None, description="ID of the affected resource"
    )
    resource_type: Optional[str] = Field(
        None, description="Type of the affected resource"
    )
    details: Optional[Dict[str, Any]] = Field(
        None, description="Additional event details"
    )
    request_id: Optional[str] = Field(
        None, description="Request ID"
    )
    user_agent: Optional[str] = Field(
        None, description="User agent of the client"
    )
    session_id: Optional[str] = Field(
        None, description="Session ID"
    )
    company_id: Optional[uuid.UUID] = Field(
        None, description="Company context"
    )


class AuditLogCreate(AuditLogBase):
    """Schema for creating an audit log."""

    pass


class AuditLogInDB(AuditLogBase):
    """Schema for an audit log in the database."""

    id: uuid.UUID = Field(..., description="Unique identifier")

    model_config = ConfigDict(from_attributes=True)


class AuditLog(AuditLogInDB):
    """Schema for an audit log with related information."""

    user: Optional[Dict[str, Any]] = Field(
        None, description="User details"
    )
    company: Optional[Dict[str, Any]] = Field(
        None, description="Company details"
    )


class AuditLogFilter(BaseModel):
    """Schema for filtering audit logs."""

    start_date: Optional[datetime] = Field(
        None, description="Start date for filter"
    )
    end_date: Optional[datetime] = Field(
        None, description="End date for filter"
    )
    event_type: Optional[str] = Field(
        None, description="Event type to filter by"
    )
    level: Optional[AuditLogLevelEnum] = Field(
        None, description="Log level to filter by"
    )
    user_id: Optional[uuid.UUID] = Field(
        None, description="User ID to filter by"
    )
    resource_type: Optional[str] = Field(
        None, description="Resource type to filter by"
    )
    resource_id: Optional[uuid.UUID] = Field(
        None, description="Resource ID to filter by"
    )
    company_id: Optional[uuid.UUID] = Field(
        None, description="Company ID to filter by"
    )


class AuditLogStatistics(BaseModel):
    """Schema for audit log statistics."""

    total_count: int = Field(..., description="Total number of log entries")
    by_level: Dict[str, int] = Field(
        ..., description="Count by level"
    )
    by_event_type: Dict[str, int] = Field(
        ..., description="Count by event type"
    )
    by_user: Dict[str, int] = Field(
        ..., description="Count by user"
    )
    by_resource_type: Dict[str, int] = Field(
        ..., description="Count by resource type"
    )


class AuditLogExportFormat(str, Enum):
    """Export formats for audit logs."""

    CSV = "csv"
    JSON = "json"
    XML = "xml"


class AuditLogExportRequest(BaseModel):
    """Schema for exporting audit logs."""

    filter: Optional[AuditLogFilter] = Field(
        None, description="Filter criteria"
    )
    format: AuditLogExportFormat = Field(
        AuditLogExportFormat.CSV, description="Export format"
    )
    include_details: bool = Field(
        True, description="Include detailed information"
    )


class AuditLogResponse(BaseModel):
    """Schema for paginated audit log responses."""

    total: int = Field(..., description="Total number of logs matching criteria")
    items: List[AuditLog] = Field(..., description="Audit logs")
    page: int = Field(1, description="Current page number")
    page_size: int = Field(..., description="Number of logs per page")
    pages: int = Field(..., description="Total number of pages")
