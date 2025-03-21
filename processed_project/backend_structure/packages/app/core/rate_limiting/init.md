# Module: app.core.rate_limiting

**Path:** `app/core/rate_limiting/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.utils import check_rate_limit, get_ttl
from app.core.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.rate_limiting")
__all__ = __all__ = [
    # Models
    "RateLimitRule",
    "RateLimitStrategy",
    # Core functions
    "initialize",
    "shutdown",
    # Core classes
    "RateLimiter",
    # Utility functions
    "check_rate_limit",
    "get_ttl",
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
