# Module: app.core.cache.backends.null

**Path:** `app/core/cache/backends/null.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, TypeVar
from app.core.cache.base import CacheBackend
from app.logging import get_logger
```

## Global Variables
```python
T = T = TypeVar("T")
logger = logger = get_logger("app.core.cache.null")
```

## Classes

| Class | Description |
| --- | --- |
| `NullCacheBackend` |  |

### Class: `NullCacheBackend`
**Inherits from:** CacheBackend[T]

#### Methods

| Method | Description |
| --- | --- |
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
async def get(self, key, default) -> Optional[T]:
```

##### `get_many`
```python
async def get_many(self, keys) -> Dict[(str, Optional[T])]:
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
