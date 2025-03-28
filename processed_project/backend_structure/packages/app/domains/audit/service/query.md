# Module: app.domains.audit.service.query

**Path:** `app/domains/audit/service/query.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.logging import get_logger
from app.domains.audit.service.base import AuditEventType, AuditLogLevel
```

## Global Variables
```python
logger = logger = get_logger("app.domains.audit.service.query")
```

## Classes

| Class | Description |
| --- | --- |
| `AuditQuery` |  |

### Class: `AuditQuery`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_event_by_id` `async` |  |
| `get_events` `async` |  |
| `get_resource_history` `async` |  |
| `get_user_activity` `async` |  |
| `purge_old_logs` `async` |  |

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
async def get_events(self, user_id, event_type, resource_id, resource_type, start_time, end_time, level, limit, offset, sort_field, sort_order) -> Dict[(str, Any)]:
```

##### `get_resource_history`
```python
async def get_resource_history(self, resource_type, resource_id, limit) -> List[Dict[(str, Any)]]:
```

##### `get_user_activity`
```python
async def get_user_activity(self, user_id, start_time, end_time, limit) -> List[Dict[(str, Any)]]:
```

##### `purge_old_logs`
```python
async def purge_old_logs(self, days_to_keep) -> int:
```
