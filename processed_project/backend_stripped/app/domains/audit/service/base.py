from __future__ import annotations
'Base interfaces and types for the audit system.\n\nThis module defines common types, protocols, and interfaces\nused throughout the audit service components.\n'
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, TypeVar
from pydantic import BaseModel
T = TypeVar('T')
class AuditEventType(str, Enum):
    USER_LOGIN = 'user_login'
    USER_LOGOUT = 'user_logout'
    LOGIN_FAILED = 'login_failed'
    PASSWORD_RESET_REQUESTED = 'password_reset_requested'
    PASSWORD_RESET_COMPLETED = 'password_reset_completed'
    MFA_ENABLED = 'mfa_enabled'
    MFA_DISABLED = 'mfa_disabled'
    SESSION_EXPIRED = 'session_expired'
    API_KEY_CREATED = 'api_key_created'
    API_KEY_REVOKED = 'api_key_revoked'
    USER_CREATED = 'user_created'
    USER_UPDATED = 'user_updated'
    USER_DELETED = 'user_deleted'
    USER_ACTIVATED = 'user_activated'
    USER_DEACTIVATED = 'user_deactivated'
    PASSWORD_CHANGED = 'password_changed'
    EMAIL_CHANGED = 'email_changed'
    USER_PROFILE_UPDATED = 'user_profile_updated'
    PERMISSION_CHANGED = 'permission_changed'
    ROLE_ASSIGNED = 'role_assigned'
    ROLE_REVOKED = 'role_revoked'
    ACCESS_DENIED = 'access_denied'
    PRODUCT_CREATED = 'product_created'
    PRODUCT_UPDATED = 'product_updated'
    PRODUCT_DELETED = 'product_deleted'
    PRODUCT_ACTIVATED = 'product_activated'
    PRODUCT_DEACTIVATED = 'product_deactivated'
    PRICE_CHANGED = 'price_changed'
    INVENTORY_UPDATED = 'inventory_updated'
    ORDER_CREATED = 'order_created'
    ORDER_UPDATED = 'order_updated'
    ORDER_CANCELED = 'order_canceled'
    ORDER_SHIPPED = 'order_shipped'
    PAYMENT_RECEIVED = 'payment_received'
    PAYMENT_REFUNDED = 'payment_refunded'
    DATA_EXPORTED = 'data_exported'
    DATA_IMPORTED = 'data_imported'
    DATA_DELETED = 'data_deleted'
    REPORT_GENERATED = 'report_generated'
    SETTINGS_CHANGED = 'settings_changed'
    CONFIGURATION_CHANGED = 'configuration_changed'
    FEATURE_ENABLED = 'feature_enabled'
    FEATURE_DISABLED = 'feature_disabled'
    FILE_UPLOADED = 'file_uploaded'
    FILE_DOWNLOADED = 'file_downloaded'
    FILE_DELETED = 'file_deleted'
    EMAIL_SENT = 'email_sent'
    SMS_SENT = 'sms_sent'
    NOTIFICATION_SENT = 'notification_sent'
    CHAT_ROOM_CREATED = 'chat_room_created'
    CHAT_MESSAGE_SENT = 'chat_message_sent'
    CHAT_MESSAGE_EDITED = 'chat_message_edited'
    CHAT_MESSAGE_DELETED = 'chat_message_deleted'
    CHAT_MEMBER_ADDED = 'chat_member_added'
    CHAT_MEMBER_REMOVED = 'chat_member_removed'
    EXTERNAL_API_CALLED = 'external_api_called'
    WEBHOOK_RECEIVED = 'webhook_received'
    WEBHOOK_PROCESSED = 'webhook_processed'
    SYSTEM_STARTED = 'system_started'
    SYSTEM_STOPPED = 'system_stopped'
    BACKUP_CREATED = 'backup_created'
    BACKUP_RESTORED = 'backup_restored'
    MAINTENANCE_MODE_ENABLED = 'maintenance_mode_enabled'
    MAINTENANCE_MODE_DISABLED = 'maintenance_mode_disabled'
    GDPR_DATA_EXPORT = 'gdpr_data_export'
    GDPR_DATA_DELETED = 'gdpr_data_deleted'
    TERMS_ACCEPTED = 'terms_accepted'
    PRIVACY_POLICY_ACCEPTED = 'privacy_policy_accepted'
class AuditLogLevel(str, Enum):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'
class AuditContext(BaseModel):
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    company_id: Optional[str] = None
    resource_id: Optional[str] = None
    resource_type: Optional[str] = None
    before_state: Optional[Dict[str, Any]] = None
    after_state: Optional[Dict[str, Any]] = None
    changes: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
class AuditOptions(BaseModel):
    include_request_body: bool = False
    sensitive_fields: List[str] = []
    anonymize_data: bool = False
    capture_before_after: bool = False
    retention_period: int = 90
class AuditLogger(Protocol):
    async def log_event(self, event_type: AuditEventType, user_id: Optional[str]=None, ip_address: Optional[str]=None, resource_id: Optional[str]=None, resource_type: Optional[str]=None, details: Optional[Dict[str, Any]]=None, context: Optional[AuditContext]=None, level: Optional[AuditLogLevel]=None, options: Optional[AuditOptions]=None) -> str:
        ...