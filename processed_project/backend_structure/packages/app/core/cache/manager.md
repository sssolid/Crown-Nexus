# Module: app.core.cache.manager

**Path:** `app/core/cache/manager.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import time
from typing import Dict, Optional, Any, TypeVar, List, Union, cast
from app.core.cache.backends import get_backend
from app.core.cache.base import CacheBackend
from app.core.config import settings
from app.logging import get_logger
from app.core.dependency_manager import get_dependency
```

## Global Variables
```python
logger = logger = get_logger("app.core.cache.manager")
T = T = TypeVar("T")
HAS_METRICS = False
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
| `clear` `async` |  |
| `decr` `async` |  |
| `delete` `async` |  |
| `delete_many` `async` |  |
| `exists` `async` |  |
| `get` `async` |  |
| `get_backend` |  |
| `get_many` `async` |  |
| `incr` `async` |  |
| `initialize` `async` |  |
| `invalidate_pattern` `async` |  |
| `set` `async` |  |
| `set_many` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self):
```

##### `clear`
```python
async def clear(self, backend) -> bool:
```

##### `decr`
```python
async def decr(self, key, amount, default, ttl, backend) -> int:
```

##### `delete`
```python
async def delete(self, key, backend) -> bool:
```

##### `delete_many`
```python
async def delete_many(self, keys, backend) -> int:
```

##### `exists`
```python
async def exists(self, key, backend) -> bool:
```

##### `get`
```python
async def get(self, key, default, backend) -> Optional[T]:
```

##### `get_backend`
```python
def get_backend(self, name) -> CacheBackend:
```

##### `get_many`
```python
async def get_many(self, keys, backend) -> Dict[(str, Optional[T])]:
```

##### `incr`
```python
async def incr(self, key, amount, default, ttl, backend) -> int:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `invalidate_pattern`
```python
async def invalidate_pattern(self, pattern, backend) -> int:
```

##### `set`
```python
async def set(self, key, value, ttl, backend) -> bool:
```

##### `set_many`
```python
async def set_many(self, mapping, ttl, backend) -> bool:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
