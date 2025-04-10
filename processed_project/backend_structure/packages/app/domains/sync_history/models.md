# Module: app.domains.sync_history.models

**Path:** `app/domains/sync_history/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
```

## Classes

| Class | Description |
| --- | --- |
| `SyncEntityType` |  |
| `SyncEvent` |  |
| `SyncHistory` |  |
| `SyncSource` |  |
| `SyncStatus` |  |

### Class: `SyncEntityType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `PRODUCT` | `'product'` |
| `MEASUREMENT` | `'measurement'` |
| `STOCK` | `'stock'` |
| `PRICING` | `'pricing'` |
| `MANUFACTURER` | `'manufacturer'` |
| `CUSTOMER` | `'customer'` |
| `ORDER` | `'order'` |
| `AUTOCARE` | `'autocare'` |

### Class: `SyncEvent`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'sync_event'` |
| `__table_args__` | `    __table_args__ = {"schema": "sync_history"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `SyncHistory`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'sync_history'` |
| `triggered_by` | `    triggered_by = relationship("User", foreign_keys=[triggered_by_id])` |
| `__table_args__` | `    __table_args__ = (
        Index("ix_sync_history_status_started_at", status, started_at.desc()),
        Index("ix_sync_history_entity_source", entity_type, source),
        {"schema": "sync_history"},
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |
| `add_event` |  |
| `complete` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

##### `add_event`
```python
def add_event(self, event_type, message, details) -> 'SyncEvent':
```

##### `complete`
```python
def complete(self, status, records_processed, records_created, records_updated, records_failed, error_message, details) -> None:
```

### Class: `SyncSource`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `AS400` | `'as400'` |
| `FILEMAKER` | `'filemaker'` |
| `API` | `'api'` |
| `FILE` | `'file'` |
| `EXTERNAL` | `'external'` |

### Class: `SyncStatus`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `PENDING` | `'pending'` |
| `RUNNING` | `'running'` |
| `COMPLETED` | `'completed'` |
| `FAILED` | `'failed'` |
| `CANCELLED` | `'cancelled'` |
