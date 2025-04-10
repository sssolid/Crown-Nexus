# Module: app.middleware.metrics

**Path:** `app/middleware/metrics.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from app.utils.circuit_breaker_utils import safe_observe_histogram, safe_increment_counter
import time
from typing import Callable, Dict, Optional, Any, List
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Route, Match
from app.logging import get_logger
from app.core.metrics import track_request, set_gauge, increment_counter, observe_histogram, MetricName, MetricTag
from app.core.dependency_manager import get_service
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
def __init__(self, app, ignore_paths, track_paths_without_match) -> None:
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
