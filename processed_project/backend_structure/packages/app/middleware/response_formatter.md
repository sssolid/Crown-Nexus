# Module: app.middleware.response_formatter

**Path:** `app/middleware/response_formatter.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
import json
import time
from typing import Callable, Optional, Any, Dict
from fastapi import Request, Response
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import get_logger
from app.core.dependency_manager import get_service
from app.core.metrics import MetricName
from app.utils.circuit_breaker_utils import safe_observe_histogram
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.response_formatter")
```

## Classes

| Class | Description |
| --- | --- |
| `ResponseFormatterMiddleware` |  |

### Class: `ResponseFormatterMiddleware`
**Inherits from:** BaseHTTPMiddleware

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `dispatch` `async` |  |

##### `__init__`
```python
def __init__(self, app, exclude_paths, skip_binary_responses) -> None:
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
