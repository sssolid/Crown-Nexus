# Module: app.middleware.error_handler

**Path:** `app/middleware/error_handler.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.error import handle_exception
from app.core.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.logging.context import get_logger
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
| `dispatch` `async` |  |

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
