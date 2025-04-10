# Module: app.core.audit.manager

**Path:** `app/core/audit/manager.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
import uuid
from typing import Any, Dict, List, Optional, Union, cast
from sqlalchemy import delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit.backends import create_default_backends, get_backend
from app.core.audit.base import AuditBackend, AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.core.audit.exceptions import AuditBackendException, AuditManagerException
from app.core.audit.utils import get_event_level_mapping, get_sensitive_fields
from app.core.base import CoreManager
from app.core.config import settings
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.audit.manager")
```

## Classes

| Class | Description |
| --- | --- |
| `AuditManager` |  |

### Class: `AuditManager`
**Inherits from:** CoreManager

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `add_backend` |  |
| `component_name` `@property` |  |
| `get_event_by_id` `async` |  |
| `get_events` `async` |  |
| `get_resource_history` `async` |  |
| `get_user_activity` `async` |  |
| `log_event` `async` |  |
| `purge_old_logs` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `add_backend`
```python
def add_backend(self, backend) -> None:
```

##### `component_name`
```python
@property
def component_name(self) -> str:
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

##### `log_event`
```python
async def log_event(self, event_type, level, context, details, options) -> str:
```

##### `purge_old_logs`
```python
async def purge_old_logs(self, days_to_keep) -> int:
```
