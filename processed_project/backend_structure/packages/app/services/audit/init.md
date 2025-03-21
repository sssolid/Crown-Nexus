# Module: app.services.audit

**Path:** `app/services/audit/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.services.audit.base import AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.services.audit.service import AuditService
```

## Global Variables
```python
__all__ = __all__ = [
    "get_audit_service",
    "AuditService",
    "AuditEventType",
    "AuditLogLevel",
    "AuditContext",
    "AuditOptions",
]
```

## Functions

| Function | Description |
| --- | --- |
| `get_audit_service` |  |

### `get_audit_service`
```python
def get_audit_service(db):
```
