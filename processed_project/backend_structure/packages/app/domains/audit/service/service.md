# Module: app.domains.audit.service.service

**Path:** `app/domains/audit/service/service.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.logging import get_logger
from app.domains.audit.service.base import AuditContext, AuditEventType, AuditLogLevel, AuditLogger, AuditOptions
from app.domains.audit.service.factory import AuditLoggerFactory
from app.domains.audit.service.query import AuditQuery
from app.services.interfaces import ServiceInterface
```

## Global Variables
```python
logger = logger = get_logger("app.domains.audit.service.service")
```

## Classes

| Class | Description |
| --- | --- |
| `AuditService` |  |

### Class: `AuditService`
**Inherits from:** ServiceInterface

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `add_logger` |  |
| `get_event_by_id` `async` |  |
| `get_events` `async` |  |
| `get_resource_history` `async` |  |
| `get_user_activity` `async` |  |
| `initialize` `async` |  |
| `log_event` `async` |  |
| `purge_old_logs` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `add_logger`
```python
def add_logger(self, logger) -> None:
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

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `log_event`
```python
async def log_event(self, event_type, user_id, ip_address, resource_id, resource_type, details, context, level, options) -> str:
```

##### `purge_old_logs`
```python
async def purge_old_logs(self, days_to_keep) -> int:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
