# Module: app.core.audit.schemas

**Path:** `app/core/audit/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
```

## Classes

| Class | Description |
| --- | --- |
| `AuditEventTypeEnum` |  |
| `AuditLog` |  |
| `AuditLogBase` |  |
| `AuditLogCreate` |  |
| `AuditLogExportFormat` |  |
| `AuditLogExportRequest` |  |
| `AuditLogFilter` |  |
| `AuditLogInDB` |  |
| `AuditLogLevelEnum` |  |
| `AuditLogResponse` |  |
| `AuditLogStatistics` |  |

### Class: `AuditEventTypeEnum`
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
| `SYSTEM_STARTED` | `'system_started'` |
| `SYSTEM_STOPPED` | `'system_stopped'` |
| `LOGIN` | `'login'` |
| `LOGOUT` | `'logout'` |
| `CREATE` | `'create'` |
| `UPDATE` | `'update'` |
| `DELETE` | `'delete'` |
| `VIEW` | `'view'` |
| `EXPORT` | `'export'` |
| `IMPORT` | `'import'` |
| `API_ACCESS` | `'api_access'` |

### Class: `AuditLog`
**Inherits from:** AuditLogInDB

### Class: `AuditLogBase`
**Inherits from:** BaseModel

### Class: `AuditLogCreate`
**Inherits from:** AuditLogBase

### Class: `AuditLogExportFormat`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `CSV` | `'csv'` |
| `JSON` | `'json'` |
| `XML` | `'xml'` |

### Class: `AuditLogExportRequest`
**Inherits from:** BaseModel

### Class: `AuditLogFilter`
**Inherits from:** BaseModel

### Class: `AuditLogInDB`
**Inherits from:** AuditLogBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `AuditLogLevelEnum`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `INFO` | `'info'` |
| `WARNING` | `'warning'` |
| `ERROR` | `'error'` |
| `CRITICAL` | `'critical'` |

### Class: `AuditLogResponse`
**Inherits from:** BaseModel

### Class: `AuditLogStatistics`
**Inherits from:** BaseModel
