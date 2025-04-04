# Module: app.domains.sync_history.repository

**Path:** `app/domains/sync_history/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import select, desc, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.logging import get_logger
from app.domains.sync_history.models import SyncHistory, SyncEvent, SyncStatus, SyncEntityType, SyncSource
from app.repositories.base import BaseRepository
```

## Global Variables
```python
logger = logger = get_logger("app.repositories.sync_history_repository")
```

## Classes

| Class | Description |
| --- | --- |
| `SyncEventRepository` |  |
| `SyncHistoryRepository` |  |

### Class: `SyncEventRepository`
**Inherits from:** BaseRepository[(SyncEvent, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_events_by_type` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_events_by_type`
```python
async def get_events_by_type(self, event_type, sync_id, limit) -> List[SyncEvent]:
```

### Class: `SyncHistoryRepository`
**Inherits from:** BaseRepository[(SyncHistory, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `add_sync_event` `async` |  |
| `cancel_active_syncs` `async` |  |
| `create_sync` `async` |  |
| `get_active_syncs` `async` |  |
| `get_latest_syncs` `async` |  |
| `get_sync_events` `async` |  |
| `get_sync_stats` `async` |  |
| `update_sync_status` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `add_sync_event`
```python
async def add_sync_event(self, sync_id, event_type, message, details) -> SyncEvent:
```

##### `cancel_active_syncs`
```python
async def cancel_active_syncs(self, entity_type, source, cancelled_by_id) -> int:
```

##### `create_sync`
```python
async def create_sync(self, entity_type, source, triggered_by_id, details) -> SyncHistory:
```

##### `get_active_syncs`
```python
async def get_active_syncs(self, entity_type, source) -> List[SyncHistory]:
```

##### `get_latest_syncs`
```python
async def get_latest_syncs(self, entity_type, source, status, limit) -> List[SyncHistory]:
```

##### `get_sync_events`
```python
async def get_sync_events(self, sync_id, limit) -> List[SyncEvent]:
```

##### `get_sync_stats`
```python
async def get_sync_stats(self, days, entity_type, source) -> Dict[(str, Any)]:
```

##### `update_sync_status`
```python
async def update_sync_status(self, sync_id, status, records_processed, records_created, records_updated, records_failed, error_message, details) -> SyncHistory:
```
