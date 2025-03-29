# Module: app.core.cache.backends.redis

**Path:** `app/core/cache/backends/redis.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import json
import pickle
from typing import Any, Dict, List, Optional, TypeVar, cast
import redis.asyncio as redis
from redis.asyncio import Redis
from app.core.cache.base import CacheBackend
from app.core.config import settings
from app.logging import get_logger
```

## Global Variables
```python
T = T = TypeVar("T")
logger = logger = get_logger("app.core.cache.redis")
```

## Classes

| Class | Description |
| --- | --- |
| `RedisCacheBackend` |  |

### Class: `RedisCacheBackend`
**Inherits from:** CacheBackend[T]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `add_many_to_set` `async` |  |
| `add_to_set` `async` |  |
| `clear` `async` |  |
| `decr` `async` |  |
| `delete` `async` |  |
| `delete_many` `async` |  |
| `exists` `async` |  |
| `get` `async` |  |
| `get_many` `async` |  |
| `get_set_members` `async` |  |
| `get_ttl` `async` |  |
| `incr` `async` |  |
| `initialize` `async` |  |
| `invalidate_pattern` `async` |  |
| `remove_from_set` `async` |  |
| `set` `async` |  |
| `set_many` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self, redis_url, serializer, prefix, **redis_options) -> None:
```

##### `add_many_to_set`
```python
async def add_many_to_set(self, key, members) -> int:
```

##### `add_to_set`
```python
async def add_to_set(self, key, member) -> bool:
```

##### `clear`
```python
async def clear(self) -> bool:
```

##### `decr`
```python
async def decr(self, key, amount, default, ttl) -> int:
```

##### `delete`
```python
async def delete(self, key) -> bool:
```

##### `delete_many`
```python
async def delete_many(self, keys) -> int:
```

##### `exists`
```python
async def exists(self, key) -> bool:
```

##### `get`
```python
async def get(self, key) -> Optional[T]:
```

##### `get_many`
```python
async def get_many(self, keys) -> Dict[(str, Optional[T])]:
```

##### `get_set_members`
```python
async def get_set_members(self, key) -> List[str]:
```

##### `get_ttl`
```python
async def get_ttl(self, key) -> Optional[int]:
```

##### `incr`
```python
async def incr(self, key, amount, default, ttl) -> int:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `invalidate_pattern`
```python
async def invalidate_pattern(self, pattern) -> int:
```

##### `remove_from_set`
```python
async def remove_from_set(self, key, member) -> bool:
```

##### `set`
```python
async def set(self, key, value, ttl) -> bool:
```

##### `set_many`
```python
async def set_many(self, mapping, ttl) -> bool:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
