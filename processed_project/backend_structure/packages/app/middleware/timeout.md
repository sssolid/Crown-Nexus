# Module: app.middleware.timeout

**Path:** `app/middleware/timeout.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import time
from typing import Callable, Optional, Any, Dict
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette import status
from app.core.exceptions import AppException, ErrorCode
from app.logging import get_logger
from app.core.dependency_manager import get_service
from app.utils.circuit_breaker_utils import safe_observe_histogram, safe_increment_counter
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.timeout")
```

## Classes

| Class | Description |
| --- | --- |
| `TimeoutException` |  |
| `TimeoutMiddleware` |  |

### Class: `TimeoutException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, status_code, code) -> None:
```

### Class: `TimeoutMiddleware`
**Inherits from:** BaseHTTPMiddleware

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `dispatch` `async` |  |

##### `__init__`
```python
def __init__(self, app, timeout_seconds, exclude_paths) -> None:
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
