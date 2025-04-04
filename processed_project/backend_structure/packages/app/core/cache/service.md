# Module: app.core.cache.service

**Path:** `app/core/cache/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, TypeVar
from app.core.cache.manager import cache_manager
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.cache.service")
T = T = TypeVar("T")
```

## Functions

| Function | Description |
| --- | --- |
| `get_cache_service` |  |

### `get_cache_service`
```python
def get_cache_service() -> CacheService:
```

## Classes

| Class | Description |
| --- | --- |
| `CacheService` |  |

### Class: `CacheService`

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
| `get_many` `async` |  |
| `incr` `async` |  |
| `initialize` `async` |  |
| `invalidate_pattern` `async` |  |
| `set` `async` |  |
| `set_many` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self) -> None:
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
