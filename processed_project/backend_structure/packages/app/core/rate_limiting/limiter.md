# Module: app.core.rate_limiting.limiter

**Path:** `app/core/rate_limiting/limiter.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import time
from typing import Any, Dict, Optional, Tuple
from fastapi import Request
from app.core.config import settings
from app.core.logging import get_logger
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.utils.redis_manager import get_redis_client, increment_counter
from app.core.rate_limiting.utils import check_rate_limit
```

## Global Variables
```python
logger = logger = get_logger(__name__)
```

## Classes

| Class | Description |
| --- | --- |
| `RateLimiter` |  |

### Class: `RateLimiter`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_key_for_request` |  |
| `is_rate_limited` `async` |  |

##### `__init__`
```python
def __init__(self, use_redis, prefix, default_rule) -> None:
```

##### `get_key_for_request`
```python
def get_key_for_request(self, request, rule) -> str:
```

##### `is_rate_limited`
```python
async def is_rate_limited(self, key, rule) -> Tuple[(bool, int, int)]:
```
