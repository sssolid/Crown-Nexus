# Module: app.core.cache.backends

**Path:** `app/core/cache/backends/__init__.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Dict, Any
from app.core.cache.backends.memory import MemoryCacheBackend
from app.core.cache.backends.null import NullCacheBackend
from app.core.cache.backends.redis import RedisCacheBackend
```

## Global Variables
```python
__all__ = __all__ = ["MemoryCacheBackend", "RedisCacheBackend", "NullCacheBackend", "get_backend"]
```

## Functions

| Function | Description |
| --- | --- |
| `get_backend` |  |

### `get_backend`
```python
def get_backend(name) -> Any:
```
