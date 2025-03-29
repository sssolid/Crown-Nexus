# Module: app.core.cache.decorators

**Path:** `app/core/cache/decorators.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import functools
import time
from typing import Any, Callable, List, Optional, TypeVar, cast, Dict
from app.core.cache.keys import generate_cache_key
from app.core.cache.manager import cache_manager
from app.logging import get_logger
from app.core.dependency_manager import get_dependency
```

## Global Variables
```python
F = F = TypeVar("F", bound=Callable[..., Any])
T = T = TypeVar("T")
logger = logger = get_logger("app.core.cache.decorators")
HAS_METRICS = False
```

## Functions

| Function | Description |
| --- | --- |
| `cache_aside` |  |
| `cached` |  |
| `invalidate_cache` |  |
| `memoize` |  |

### `cache_aside`
```python
def cache_aside(key_func, ttl, backend, tags) -> Callable[([F], F)]:
```

### `cached`
```python
def cached(ttl, prefix, backend, skip_args, skip_kwargs, tags) -> Callable[([F], F)]:
```

### `invalidate_cache`
```python
def invalidate_cache(pattern, prefix, backend, tags) -> Callable[([F], F)]:
```

### `memoize`
```python
def memoize(ttl, max_size) -> Callable[([F], F)]:
```
