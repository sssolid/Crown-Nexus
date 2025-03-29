# Module: app.core.cache

**Path:** `app/core/cache/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.cache.base import CacheBackend
from app.core.cache.decorators import cached, invalidate_cache, cache_aside, memoize
from app.core.cache.exceptions import CacheException, CacheConnectionException, CacheOperationException, CacheConfigurationException
from app.core.cache.keys import generate_cache_key, generate_list_key, generate_model_key, generate_query_key
from app.core.cache.manager import cache_manager, initialize_cache
from app.core.cache.service import CacheService, get_cache_service
```

## Global Variables
```python
__all__ = __all__ = [
    "CacheBackend",
    "cached",
    "invalidate_cache",
    "cache_aside",
    "memoize",
    "CacheException",
    "CacheConnectionException",
    "CacheOperationException",
    "CacheConfigurationException",
    "generate_cache_key",
    "generate_list_key",
    "generate_model_key",
    "generate_query_key",
    "cache_manager",
    "initialize_cache",
    "CacheService",
    "get_cache_service",
]
```
