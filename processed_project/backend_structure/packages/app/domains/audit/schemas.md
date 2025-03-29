# Module: app.domains.audit.schemas

**Path:** `app/domains/audit/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field
```

## Classes

| Class | Description |
| --- | --- |
| `AuditEventType` |  |
| `AuditLog` |  |
| `AuditLogBase` |  |
| `AuditLogCreate` |  |
| `AuditLogExportFormat` |  |
| `AuditLogExportRequest` |  |
| `AuditLogFilter` |  |
| `AuditLogInDB` |  |
| `AuditLogLevel` |  |
| `AuditLogStatistics` |  |

### Class: `AuditEventType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `LOGIN` | `'login'` |
| `LOGOUT` | `'logout'` |
| `CREATE` | `'create'` |
| `UPDATE` | `'update'` |
| `DELETE` | `'delete'` |
| `VIEW` | `'view'` |
| `EXPORT` | `'export'` |
| `IMPORT` | `'import'` |
| `APPROVE` | `'approve'` |
| `REJECT` | `'reject'` |
| `PASSWORD_CHANGE` | `'password_change'` |
| `ROLE_CHANGE` | `'role_change'` |
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

### Class: `AuditLogLevel`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `INFO` | `'info'` |
| `WARNING` | `'warning'` |
| `ERROR` | `'error'` |
| `CRITICAL` | `'critical'` |

### Class: `AuditLogStatistics`
**Inherits from:** BaseModel
