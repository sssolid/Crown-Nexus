# Module: app.middleware.error_handler

**Path:** `app/middleware/error_handler.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import time
import sys
import traceback
from typing import Callable, Any, Optional, Dict, Type
from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.error import handle_exception
from app.core.exceptions import AppException, ErrorCode, app_exception_handler, validation_exception_handler, generic_exception_handler
from app.logging.context import get_logger
from app.core.dependency_manager import get_service
from app.utils.circuit_breaker_utils import safe_increment_counter
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.error_handler")
```

## Classes

| Class | Description |
| --- | --- |
| `ErrorHandlerMiddleware` |  |

### Class: `ErrorHandlerMiddleware`
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
