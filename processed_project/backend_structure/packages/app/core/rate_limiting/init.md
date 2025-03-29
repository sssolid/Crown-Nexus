# Module: app.core.rate_limiting

**Path:** `app/core/rate_limiting/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.rate_limiting.utils import check_rate_limit, get_ttl
from app.core.rate_limiting.exceptions import RateLimitingException, RateLimitExceededException, RateLimitingServiceException, RateLimitingConfigurationException
from app.core.rate_limiting.service import RateLimitingService, get_rate_limiting_service
```

## Global Variables
```python
logger = logger = get_logger("app.core.rate_limiting.__init__")
__all__ = __all__ = [
    "RateLimitRule",
    "RateLimitStrategy",
    "RateLimiter",
    "initialize",
    "shutdown",
    "check_rate_limit",
    "get_ttl",
    "RateLimitingException",
    "RateLimitExceededException",
    "RateLimitingServiceException",
    "RateLimitingConfigurationException",
    "RateLimitingService",
    "get_rate_limiting_service",
]
```

## Functions

| Function | Description |
| --- | --- |
| `initialize` |  |
| `shutdown` |  |

### `initialize`
```python
async def initialize() -> None:
```

### `shutdown`
```python
async def shutdown() -> None:
```
