# Module: app.utils.redis_manager

**Path:** `app/utils/redis_manager.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import json
from typing import Any, Dict, Optional, TypeVar, cast
import redis.asyncio as redis
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from app.core.config import settings
from app.core.exceptions import ServiceException, ErrorCode
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.utils.redis_manager")
T = T = TypeVar("T")
```

## Functions

| Function | Description |
| --- | --- |
| `cache_get_or_set` |  |
| `delete_key` |  |
| `get_key` |  |
| `get_redis_client` |  |
| `get_redis_pool` |  |
| `increment_counter` |  |
| `publish_message` |  |
| `rate_limit_check` |  |
| `set_key` |  |

### `cache_get_or_set`
```python
async def cache_get_or_set(key, callback, ttl, force_refresh) -> Any:
```

### `delete_key`
```python
async def delete_key(key) -> bool:
```

### `get_key`
```python
async def get_key(key, default) -> Optional[T]:
```

### `get_redis_client`
```python
async def get_redis_client() -> Redis:
```

### `get_redis_pool`
```python
async def get_redis_pool() -> ConnectionPool:
```

### `increment_counter`
```python
async def increment_counter(key, amount, ttl) -> Optional[int]:
```

### `publish_message`
```python
async def publish_message(channel, message) -> bool:
```

### `rate_limit_check`
```python
async def rate_limit_check(key, limit, window) -> tuple[(bool, int)]:
```

### `set_key`
```python
async def set_key(key, value, ttl) -> bool:
```
