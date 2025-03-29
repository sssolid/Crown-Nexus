# Module: app.middleware.response_formatter

**Path:** `app/middleware/response_formatter.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
import json
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import get_logger
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
| `dispatch` `async` |  |

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
