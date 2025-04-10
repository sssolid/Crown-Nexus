# Module: app.db.base_class

**Path:** `app/db/base_class.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, ClassVar
from sqlalchemy import DateTime, Boolean, inspect, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.expression import Select
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.db.base_class")
T = T = TypeVar("T", bound="Base")
```

## Classes

| Class | Description |
| --- | --- |
| `Base` |  |

### Class: `Base`
**Inherits from:** DeclarativeBase

#### Methods

| Method | Description |
| --- | --- |
| `__tablename__` |  |
| `active_only` |  |
| `filter_by_id` |  |
| `from_dict` |  |
| `get_columns` |  |
| `get_relationships` |  |
| `restore` |  |
| `soft_delete` |  |
| `to_dict` |  |
| `update_from_dict` |  |

##### `__tablename__`
```python
@declared_attr
def __tablename__(self) -> str:
```

##### `active_only`
```python
@classmethod
def active_only(cls) -> Select:
```

##### `filter_by_id`
```python
@classmethod
def filter_by_id(cls, id_value) -> Select:
```

##### `from_dict`
```python
@classmethod
def from_dict(cls, data) -> T:
```

##### `get_columns`
```python
@classmethod
def get_columns(cls) -> List[str]:
```

##### `get_relationships`
```python
@classmethod
def get_relationships(cls) -> Dict[(str, Any)]:
```

##### `restore`
```python
def restore(self, user_id) -> None:
```

##### `soft_delete`
```python
def soft_delete(self, user_id) -> None:
```

##### `to_dict`
```python
def to_dict(self, exclude, include_relationships) -> Dict[(str, Any)]:
```

##### `update_from_dict`
```python
def update_from_dict(self, data, user_id, exclude) -> None:
```
