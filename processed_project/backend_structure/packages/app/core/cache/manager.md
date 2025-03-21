# Module: app.core.cache.manager

**Path:** `app/core/cache/manager.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Optional, Type, Union
from app.core.cache.backends import get_backend
from app.core.cache.base import CacheBackend
from app.core.config import settings
from app.core.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.cache.manager")
cache_manager = cache_manager = CacheManager()
```

## Functions

| Function | Description |
| --- | --- |
| `initialize_cache` |  |

### `initialize_cache`
```python
async def initialize_cache() -> None:
```

## Classes

| Class | Description |
| --- | --- |
| `CacheManager` |  |

### Class: `CacheManager`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_backend` |  |
| `initialize` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self):
```

##### `get_backend`
```python
def get_backend(self, name) -> CacheBackend:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
