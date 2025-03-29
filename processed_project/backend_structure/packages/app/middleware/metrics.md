# Module: app.middleware.metrics

**Path:** `app/middleware/metrics.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import time
from typing import Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Route, Match
from app.logging import get_logger
from app.core.metrics import track_request, set_gauge, MetricName, MetricTag
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.metrics")
```

## Classes

| Class | Description |
| --- | --- |
| `MetricsMiddleware` |  |

### Class: `MetricsMiddleware`
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
