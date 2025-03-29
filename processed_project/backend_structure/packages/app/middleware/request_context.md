# Module: app.middleware.request_context

**Path:** `app/middleware/request_context.py`

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
| `dispatch` `async` |  |

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
