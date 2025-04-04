# Module: app.core.pagination.factory

**Path:** `app/core/pagination/factory.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Generic, Optional, Type, TypeVar, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.logging import get_logger
from app.core.pagination.base import PaginationProvider
```

## Global Variables
```python
logger = logger = get_logger("app.core.pagination.factory")
T = T = TypeVar("T")  # Entity type
R = R = TypeVar("R")  # Result type
```

## Classes

| Class | Description |
| --- | --- |
| `PaginationProviderFactory` |  |

### Class: `PaginationProviderFactory`
**Inherits from:** Generic[(T, R)]

#### Methods

| Method | Description |
| --- | --- |
| `clear_cache` |  |
| `create_provider` |  |
| `register_provider` |  |

##### `clear_cache`
```python
@classmethod
def clear_cache(cls) -> None:
```

##### `create_provider`
```python
@classmethod
def create_provider(cls, provider_type, db, model_class, response_model, **kwargs) -> PaginationProvider[(T, R)]:
```

##### `register_provider`
```python
@classmethod
def register_provider(cls, name, provider_class) -> None:
```
