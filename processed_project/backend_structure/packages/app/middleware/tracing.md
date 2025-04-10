# Module: app.middleware.tracing

**Path:** `app/middleware/tracing.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.metrics import MetricName
from app.utils.circuit_breaker_utils import safe_observe_histogram
import time
import uuid
from typing import Callable, Optional, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import get_logger, request_context
from app.core.dependency_manager import get_service
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.tracing")
```

## Classes

| Class | Description |
| --- | --- |
| `TracingMiddleware` |  |

### Class: `TracingMiddleware`
**Inherits from:** BaseHTTPMiddleware

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `dispatch` `async` |  |

##### `__init__`
```python
def __init__(self, app, service_name, exclude_paths) -> None:
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
