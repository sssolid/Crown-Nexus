from __future__ import annotations

"""
Utility functions for the audit system.

This module provides utility functions for audit operations.
"""

from typing import Any, Dict, List, Optional

from app.core.audit.base import AuditEventType, AuditLogLevel
from app.logging import get_logger

logger = get_logger("app.core.audit.utils")


def anonymize_data(data: Dict[str, Any], sensitive_fields: List[str]) -> Dict[str, Any]:
    """Anonymize sensitive data in a dictionary.

    Args:
        data: Data to anonymize.
        sensitive_fields: List of sensitive field names.

    Returns:
        Anonymized data.
    """
    if not data:
        return {}

    if not sensitive_fields:
        return data

    anonymized = {}
    for key, value in data.items():
        is_sensitive = any(
            sensitive.lower() in key.lower() for sensitive in sensitive_fields
        )

        if is_sensitive:
            if isinstance(value, str):
                if len(value) <= 4:
                    anonymized[key] = "****"
                else:
                    anonymized[key] = value[0] + "*" * (len(value) - 2) + value[-1]
            else:
                anonymized[key] = "[REDACTED]"
        elif isinstance(value, dict):
            anonymized[key] = anonymize_data(value, sensitive_fields)
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            anonymized[key] = [
                (
                    anonymize_data(item, sensitive_fields)
                    if isinstance(item, dict)
                    else item
                )
                for item in value
            ]
        else:
            anonymized[key] = value

    return anonymized


def get_event_level_mapping() -> Dict[str, str]:
    """Get the default mapping of event types to log levels.

    Returns:
        Dictionary mapping event types to log levels.
    """
    return {
        AuditEventType.ACCESS_DENIED: AuditLogLevel.WARNING,
        AuditEventType.LOGIN_FAILED: AuditLogLevel.WARNING,
        AuditEventType.USER_DELETED: AuditLogLevel.WARNING,
        AuditEventType.API_KEY_REVOKED: AuditLogLevel.WARNING,
        AuditEventType.PAYMENT_REFUNDED: AuditLogLevel.WARNING,
        AuditEventType.DATA_DELETED: AuditLogLevel.WARNING,
        AuditEventType.SYSTEM_STOPPED: AuditLogLevel.WARNING,
        AuditEventType.MAINTENANCE_MODE_ENABLED: AuditLogLevel.WARNING,
        AuditEventType.GDPR_DATA_DELETED: AuditLogLevel.WARNING,
    }


def get_sensitive_fields() -> List[str]:
    """Get the default list of sensitive fields to anonymize.

    Returns:
        List of sensitive field names.
    """
    return [
        "password",
        "token",
        "secret",
        "api_key",
        "credit_card",
        "ssn",
        "social_security",
        "auth",
        "key",
    ]


def format_audit_event(event: Dict[str, Any]) -> str:
    """Format an audit event for display.

    Args:
        event: Audit event data.

    Returns:
        Formatted string representation of the event.
    """
    timestamp = event.get("timestamp", "N/A")
    event_type = event.get("event_type", "N/A")
    level = event.get("level", "N/A")
    user_id = event.get("user_id", "N/A")
    resource = f"{event.get('resource_type', 'N/A')}:{event.get('resource_id', 'N/A')}"

    return f"[{timestamp}] {level.upper()} {event_type} by {user_id} on {resource}"
