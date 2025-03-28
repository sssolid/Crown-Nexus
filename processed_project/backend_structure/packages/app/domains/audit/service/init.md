# Module: app.domains.audit.service

**Path:** `app/domains/audit/service/__init__.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.audit.service.service import AuditService
```

## Functions

| Function | Description |
| --- | --- |
| `get_audit_service` |  |

### `get_audit_service`
```python
def get_audit_service(db) -> AuditService:
```
