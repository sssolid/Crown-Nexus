# Module: app.middleware.response_formatter

**Path:** `app/middleware/response_formatter.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import json
import datetime
from typing import Any, Callable, Dict, Optional, Union
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import get_logger
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
