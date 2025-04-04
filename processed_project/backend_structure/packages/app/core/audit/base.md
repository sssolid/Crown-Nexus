# Module: app.core.audit.base

**Path:** `app/core/audit/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, TypeVar
from pydantic import BaseModel, Field
from app.core.base import CoreBackend
```

## Global Variables
```python
T = T = TypeVar("T")
```

## Classes

| Class | Description |
| --- | --- |
| `AuditBackend` |  |
| `AuditContext` |  |
| `AuditEventType` |  |
| `AuditLogLevel` |  |
| `AuditOptions` |  |

### Class: `AuditBackend`
**Inherits from:** CoreBackend, Protocol

#### Methods

| Method | Description |
| --- | --- |
| `log_event` `async` |  |

##### `log_event`
```python
async def log_event(self, event_type, level, context, details, options) -> str:
```

### Class: `AuditContext`
**Inherits from:** BaseModel

### Class: `AuditEventType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `USER_LOGIN` | `'user_login'` |
| `USER_LOGOUT` | `'user_logout'` |
| `LOGIN_FAILED` | `'login_failed'` |
| `PASSWORD_RESET_REQUESTED` | `'password_reset_requested'` |
| `PASSWORD_RESET_COMPLETED` | `'password_reset_completed'` |
| `MFA_ENABLED` | `'mfa_enabled'` |
| `MFA_DISABLED` | `'mfa_disabled'` |
| `SESSION_EXPIRED` | `'session_expired'` |
| `API_KEY_CREATED` | `'api_key_created'` |
| `API_KEY_REVOKED` | `'api_key_revoked'` |
| `USER_CREATED` | `'user_created'` |
| `USER_UPDATED` | `'user_updated'` |
| `USER_DELETED` | `'user_deleted'` |
| `USER_ACTIVATED` | `'user_activated'` |
| `USER_DEACTIVATED` | `'user_deactivated'` |
| `PASSWORD_CHANGED` | `'password_changed'` |
| `EMAIL_CHANGED` | `'email_changed'` |
| `USER_PROFILE_UPDATED` | `'user_profile_updated'` |
| `PERMISSION_CHANGED` | `'permission_changed'` |
| `ROLE_ASSIGNED` | `'role_assigned'` |
| `ROLE_REVOKED` | `'role_revoked'` |
| `ACCESS_DENIED` | `'access_denied'` |
| `PRODUCT_CREATED` | `'product_created'` |
| `PRODUCT_UPDATED` | `'product_updated'` |
| `PRODUCT_DELETED` | `'product_deleted'` |
| `PRODUCT_ACTIVATED` | `'product_activated'` |
| `PRODUCT_DEACTIVATED` | `'product_deactivated'` |
| `PRICE_CHANGED` | `'price_changed'` |
| `INVENTORY_UPDATED` | `'inventory_updated'` |
| `ORDER_CREATED` | `'order_created'` |
| `ORDER_UPDATED` | `'order_updated'` |
| `ORDER_CANCELED` | `'order_canceled'` |
| `ORDER_SHIPPED` | `'order_shipped'` |
| `PAYMENT_RECEIVED` | `'payment_received'` |
| `PAYMENT_REFUNDED` | `'payment_refunded'` |
| `DATA_EXPORTED` | `'data_exported'` |
| `DATA_IMPORTED` | `'data_imported'` |
| `DATA_DELETED` | `'data_deleted'` |
| `REPORT_GENERATED` | `'report_generated'` |
| `SYSTEM_STARTED` | `'system_started'` |
| `SYSTEM_STOPPED` | `'system_stopped'` |
| `MAINTENANCE_MODE_ENABLED` | `'maintenance_mode_enabled'` |
| `MAINTENANCE_MODE_DISABLED` | `'maintenance_mode_disabled'` |
| `GDPR_DATA_EXPORT` | `'gdpr_data_export'` |
| `GDPR_DATA_DELETED` | `'gdpr_data_deleted'` |

### Class: `AuditLogLevel`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `INFO` | `'info'` |
| `WARNING` | `'warning'` |
| `ERROR` | `'error'` |
| `CRITICAL` | `'critical'` |

### Class: `AuditOptions`
**Inherits from:** BaseModel
