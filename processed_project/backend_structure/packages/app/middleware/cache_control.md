# Module: app.middleware.cache_control

**Path:** `app/middleware/cache_control.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Callable, Dict, Optional, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.cache_control")
```

## Classes

| Class | Description |
| --- | --- |
| `CacheControlMiddleware` |  |

### Class: `CacheControlMiddleware`
**Inherits from:** BaseHTTPMiddleware

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `dispatch` `async` |  |

##### `__init__`
```python
def __init__(self, app, cache_rules, default_rule, cacheable_methods, exclude_paths) -> None:
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
