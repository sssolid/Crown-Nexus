# Module: app.middleware.rate_limiting

**Path:** `app/middleware/rate_limiting.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import time
from typing import Any, Callable, Dict, List, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.exceptions import RateLimitException
from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule
from app.core.rate_limiting.exceptions import RateLimitExceededException
from app.core.dependency_manager import get_dependency
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.rate_limiting")
HAS_METRICS = False
```

## Classes

| Class | Description |
| --- | --- |
| `RateLimitMiddleware` |  |

### Class: `RateLimitMiddleware`
**Inherits from:** BaseHTTPMiddleware

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `dispatch` `async` |  |

##### `__init__`
```python
def __init__(self, app, rules, use_redis, enable_headers, block_exceeding_requests) -> None:
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
