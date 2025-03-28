from __future__ import annotations
'Audit schema definitions.\n\nThis module defines Pydantic schemas for audit log objects,\nincluding creation, filtering, and response models.\n'
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field
class AuditLogLevel(str, Enum):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'
class AuditEventType(str, Enum):
    LOGIN = 'login'
    LOGOUT = 'logout'
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    VIEW = 'view'
    EXPORT = 'export'
    IMPORT = 'import'
    APPROVE = 'approve'
    REJECT = 'reject'
    PASSWORD_CHANGE = 'password_change'
    ROLE_CHANGE = 'role_change'
    API_ACCESS = 'api_access'
class AuditLogBase(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now, description='Event timestamp')
    event_type: str = Field(..., description='Event type')
    level: AuditLogLevel = Field(AuditLogLevel.INFO, description='Log level')
    user_id: Optional[uuid.UUID] = Field(None, description='User who performed the action')
    ip_address: Optional[str] = Field(None, description='IP address of the user')
    resource_id: Optional[uuid.UUID] = Field(None, description='ID of the affected resource')
    resource_type: Optional[str] = Field(None, description='Type of the affected resource')
    details: Optional[Dict[str, Any]] = Field(None, description='Additional event details')
    request_id: Optional[str] = Field(None, description='Request ID')
    user_agent: Optional[str] = Field(None, description='User agent of the client')
    session_id: Optional[str] = Field(None, description='Session ID')
    company_id: Optional[uuid.UUID] = Field(None, description='Company context')
class AuditLogCreate(AuditLogBase):
    pass
class AuditLogInDB(AuditLogBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    model_config = ConfigDict(from_attributes=True)
class AuditLog(AuditLogInDB):
    user: Optional[Dict[str, Any]] = Field(None, description='User details')
    company: Optional[Dict[str, Any]] = Field(None, description='Company details')
class AuditLogFilter(BaseModel):
    start_date: Optional[datetime] = Field(None, description='Start date for filter')
    end_date: Optional[datetime] = Field(None, description='End date for filter')
    event_type: Optional[str] = Field(None, description='Event type to filter by')
    level: Optional[AuditLogLevel] = Field(None, description='Log level to filter by')
    user_id: Optional[uuid.UUID] = Field(None, description='User ID to filter by')
    resource_type: Optional[str] = Field(None, description='Resource type to filter by')
    resource_id: Optional[uuid.UUID] = Field(None, description='Resource ID to filter by')
    company_id: Optional[uuid.UUID] = Field(None, description='Company ID to filter by')
class AuditLogStatistics(BaseModel):
    total_count: int = Field(..., description='Total number of log entries')
    by_level: Dict[str, int] = Field(..., description='Count by level')
    by_event_type: Dict[str, int] = Field(..., description='Count by event type')
    by_user: Dict[str, int] = Field(..., description='Count by user')
    by_resource_type: Dict[str, int] = Field(..., description='Count by resource type')
class AuditLogExportFormat(str, Enum):
    CSV = 'csv'
    JSON = 'json'
    XML = 'xml'
class AuditLogExportRequest(BaseModel):
    filter: Optional[AuditLogFilter] = Field(None, description='Filter criteria')
    format: AuditLogExportFormat = Field(AuditLogExportFormat.CSV, description='Export format')
    include_details: bool = Field(True, description='Include detailed information')