# Module: app.core.rate_limiting.limiter

**Path:** `app/core/rate_limiting/limiter.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.metrics import MetricName
import time
from typing import Dict, Optional, Tuple
from fastapi import Request
from app.core.config import settings
from app.logging import get_logger
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.utils.redis_manager import get_redis_client, increment_counter
from app.core.dependency_manager import get_dependency
```

## Global Variables
```python
logger = logger = get_logger("app.core.rate_limiting.limiter")
HAS_METRICS = False
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
