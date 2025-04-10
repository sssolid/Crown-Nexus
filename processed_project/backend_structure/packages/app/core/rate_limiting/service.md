# Module: app.core.rate_limiting.service

**Path:** `app/core/rate_limiting/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Dict, Optional, Tuple
from fastapi import Request
from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.config import settings
```

## Global Variables
```python
logger = logger = get_logger("app.core.rate_limiting.service")
```

## Functions

| Function | Description |
| --- | --- |
| `get_rate_limiting_service` |  |

### `get_rate_limiting_service`
```python
def get_rate_limiting_service() -> RateLimitingService:
```

## Classes

| Class | Description |
| --- | --- |
| `RateLimitingService` |  |

### Class: `RateLimitingService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_key_for_request` |  |
| `initialize` `async` |  |
| `is_rate_limited` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `get_key_for_request`
```python
def get_key_for_request(self, request, rule) -> str:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `is_rate_limited`
```python
async def is_rate_limited(self, key, rule) -> Tuple[(bool, int, int)]:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
