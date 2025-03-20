from __future__ import annotations

"""Audit schema definitions.

This module defines Pydantic schemas for audit log objects,
including creation, filtering, and response models.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AuditLogLevel(str, Enum):
    """Severity levels for audit logs.

    Attributes:
        INFO: Informational events.
        WARNING: Warning events that might require attention.
        ERROR: Error events that indicate problems.
        CRITICAL: Critical events that require immediate attention.
    """

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditEventType(str, Enum):
    """Types of auditable events.

    This is a subset of common event types. The system can handle
    any string value for event_type, not just these enumerated ones.
    """

    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    VIEW = "view"
    EXPORT = "export"
    IMPORT = "import"
    APPROVE = "approve"
    REJECT = "reject"
    PASSWORD_CHANGE = "password_change"
    ROLE_CHANGE = "role_change"
    API_ACCESS = "api_access"


class AuditLogBase(BaseModel):
    """Base schema for audit log data.

    Attributes:
        timestamp: When the audited event occurred.
        event_type: Type of event being audited.
        level: Log level (info, warning, error).
        user_id: ID of the user who performed the action.
        ip_address: IP address of the user.
        resource_id: ID of the affected resource.
        resource_type: Type of the affected resource.
        details: Additional details about the event.
        request_id: ID of the request that triggered the event.
        user_agent: User agent of the client.
        session_id: ID of the user's session.
        company_id: ID of the company context.
    """

    timestamp: datetime = Field(
        default_factory=datetime.now, description="Event timestamp"
    )
    event_type: str = Field(..., description="Event type")
    level: AuditLogLevel = Field(AuditLogLevel.INFO, description="Log level")
    user_id: Optional[uuid.UUID] = Field(
        None, description="User who performed the action"
    )
    ip_address: Optional[str] = Field(None, description="IP address of the user")
    resource_id: Optional[uuid.UUID] = Field(
        None, description="ID of the affected resource"
    )
    resource_type: Optional[str] = Field(
        None, description="Type of the affected resource"
    )
    details: Optional[Dict[str, Any]] = Field(
        None, description="Additional event details"
    )
    request_id: Optional[str] = Field(None, description="Request ID")
    user_agent: Optional[str] = Field(None, description="User agent of the client")
    session_id: Optional[str] = Field(None, description="Session ID")
    company_id: Optional[uuid.UUID] = Field(None, description="Company context")


class AuditLogCreate(AuditLogBase):
    """Schema for creating a new audit log entry."""

    pass


class AuditLogInDB(AuditLogBase):
    """Schema for audit log data as stored in the database.

    Includes database-specific fields like ID.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")

    model_config = ConfigDict(from_attributes=True)


class AuditLog(AuditLogInDB):
    """Schema for complete audit log data in API responses.

    Includes related entities like user and company details.
    """

    user: Optional[Dict[str, Any]] = Field(None, description="User details")
    company: Optional[Dict[str, Any]] = Field(None, description="Company details")


class AuditLogFilter(BaseModel):
    """Schema for filtering audit logs.

    Attributes:
        start_date: Filter logs after this date.
        end_date: Filter logs before this date.
        event_type: Filter by event type.
        level: Filter by log level.
        user_id: Filter by user ID.
        resource_type: Filter by resource type.
        resource_id: Filter by resource ID.
        company_id: Filter by company ID.
    """

    start_date: Optional[datetime] = Field(None, description="Start date for filter")
    end_date: Optional[datetime] = Field(None, description="End date for filter")
    event_type: Optional[str] = Field(None, description="Event type to filter by")
    level: Optional[AuditLogLevel] = Field(None, description="Log level to filter by")
    user_id: Optional[uuid.UUID] = Field(None, description="User ID to filter by")
    resource_type: Optional[str] = Field(None, description="Resource type to filter by")
    resource_id: Optional[uuid.UUID] = Field(
        None, description="Resource ID to filter by"
    )
    company_id: Optional[uuid.UUID] = Field(None, description="Company ID to filter by")


class AuditLogStatistics(BaseModel):
    """Schema for audit log statistics.

    Attributes:
        total_count: Total number of log entries.
        by_level: Count of logs grouped by level.
        by_event_type: Count of logs grouped by event type.
        by_user: Count of logs grouped by user.
        by_resource_type: Count of logs grouped by resource type.
    """

    total_count: int = Field(..., description="Total number of log entries")
    by_level: Dict[str, int] = Field(..., description="Count by level")
    by_event_type: Dict[str, int] = Field(..., description="Count by event type")
    by_user: Dict[str, int] = Field(..., description="Count by user")
    by_resource_type: Dict[str, int] = Field(..., description="Count by resource type")


class AuditLogExportFormat(str, Enum):
    """Export formats for audit logs.

    Attributes:
        CSV: Comma-separated values format.
        JSON: JSON format.
        XML: XML format.
    """

    CSV = "csv"
    JSON = "json"
    XML = "xml"


class AuditLogExportRequest(BaseModel):
    """Schema for requesting an audit log export.

    Attributes:
        filter: Filter criteria for logs to export.
        format: Export format.
        include_details: Whether to include detailed information.
    """

    filter: Optional[AuditLogFilter] = Field(None, description="Filter criteria")
    format: AuditLogExportFormat = Field(
        AuditLogExportFormat.CSV, description="Export format"
    )
    include_details: bool = Field(True, description="Include detailed information")
