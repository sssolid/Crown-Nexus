# Module: app.core.audit

**Path:** `app/core/audit/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit.base import AuditBackend, AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.core.audit.service import AuditService
from app.core.audit.exceptions import AuditBackendException, AuditConfigurationException, AuditException, AuditManagerException
```

## Global Variables
```python
__all__ = __all__ = [
    # Service
    "AuditService",
    "get_audit_service",
    # Base types
    "AuditBackend",
    "AuditContext",
    "AuditEventType",
    "AuditLogLevel",
    "AuditOptions",
    # Exceptions
    "AuditException",
    "AuditBackendException",
    "AuditManagerException",
    "AuditConfigurationException",
]
```

## Functions

| Function | Description |
| --- | --- |
| `get_audit_service` |  |

### `get_audit_service`
```python
def get_audit_service(db) -> AuditService:
```
