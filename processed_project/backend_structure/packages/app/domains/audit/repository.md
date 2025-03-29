# Module: app.domains.audit.repository

**Path:** `app/domains/audit/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy import select, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.audit.models import AuditLog
from app.repositories.base import BaseRepository
```

## Classes

| Class | Description |
| --- | --- |
| `AuditLogRepository` |  |

### Class: `AuditLogRepository`
**Inherits from:** BaseRepository[(AuditLog, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `create_log` `async` |  |
| `get_by_company` `async` |  |
| `get_by_event_type` `async` |  |
| `get_by_level` `async` |  |
| `get_by_resource` `async` |  |
| `get_by_time_range` `async` |  |
| `get_by_user` `async` |  |
| `get_recent_logs` `async` |  |
| `search` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `create_log`
```python
async def create_log(self, event_type, level, details, user_id, ip_address, resource_id, resource_type, request_id, user_agent, session_id, company_id, timestamp) -> AuditLog:
```

##### `get_by_company`
```python
async def get_by_company(self, company_id, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_event_type`
```python
async def get_by_event_type(self, event_type, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_level`
```python
async def get_by_level(self, level, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_resource`
```python
async def get_by_resource(self, resource_type, resource_id, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_time_range`
```python
async def get_by_time_range(self, start_time, end_time, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_user`
```python
async def get_by_user(self, user_id, page, page_size) -> Dict[(str, Any)]:
```

##### `get_recent_logs`
```python
async def get_recent_logs(self, hours, page, page_size) -> Dict[(str, Any)]:
```

##### `search`
```python
async def search(self, search_term, page, page_size) -> Dict[(str, Any)]:
```
