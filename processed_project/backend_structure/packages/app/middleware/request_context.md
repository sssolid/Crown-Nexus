# Module: app.middleware.request_context

**Path:** `app/middleware/request_context.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.metrics import MetricName
from app.utils.circuit_breaker_utils import safe_increment_counter, safe_observe_histogram
import time
import uuid
from typing import Callable, Any, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging.context import get_logger, request_context, set_user_id, clear_user_id
from app.core.dependency_manager import get_service
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.request_context")
```

## Classes

| Class | Description |
| --- | --- |
| `RequestContextMiddleware` |  |

### Class: `RequestContextMiddleware`
**Inherits from:** BaseHTTPMiddleware

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `dispatch` `async` |  |

##### `__init__`
```python
def __init__(self, app) -> None:
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
