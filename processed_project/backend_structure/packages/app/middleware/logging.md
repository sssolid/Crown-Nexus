# Module: app.middleware.logging

**Path:** `app/middleware/logging.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging.context import get_logger, request_context
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.logging")
```

## Classes

| Class | Description |
| --- | --- |
| `RequestLoggingMiddleware` |  |

### Class: `RequestLoggingMiddleware`
**Inherits from:** BaseHTTPMiddleware

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `dispatch` `async` |  |

##### `__init__`
```python
def __init__(self, app):
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
