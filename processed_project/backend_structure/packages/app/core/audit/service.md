# Module: app.core.audit.service

**Path:** `app/core/audit/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit.base import AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.core.audit.manager import AuditManager
from app.core.base import CoreService, HealthCheckable
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.audit.service")
```

## Classes

| Class | Description |
| --- | --- |
| `AuditService` |  |

### Class: `AuditService`
**Inherits from:** CoreService, HealthCheckable

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_event_by_id` `async` |  |
| `get_events` `async` |  |
| `get_resource_history` `async` |  |
| `get_user_activity` `async` |  |
| `health_check` `async` |  |
| `log_event` `async` |  |
| `purge_old_logs` `async` |  |
| `service_name` `@property` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_event_by_id`
```python
async def get_event_by_id(self, event_id) -> Optional[Dict[(str, Any)]]:
```

##### `get_events`
```python
async def get_events(self, start_time, end_time, event_type, level, user_id, resource_id, resource_type, limit, offset) -> Dict[(str, Any)]:
```

##### `get_resource_history`
```python
async def get_resource_history(self, resource_type, resource_id, limit) -> List[Dict[(str, Any)]]:
```

##### `get_user_activity`
```python
async def get_user_activity(self, user_id, start_time, end_time, limit) -> List[Dict[(str, Any)]]:
```

##### `health_check`
```python
async def health_check(self) -> Dict[(str, Any)]:
```

##### `log_event`
```python
async def log_event(self, event_type, user_id, ip_address, resource_id, resource_type, details, level, options) -> str:
```

##### `purge_old_logs`
```python
async def purge_old_logs(self, days_to_keep) -> int:
```

##### `service_name`
```python
@property
def service_name(self) -> str:
```
