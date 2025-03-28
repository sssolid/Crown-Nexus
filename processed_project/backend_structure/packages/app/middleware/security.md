# Module: app.middleware.security

**Path:** `app/middleware/security.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Callable, Optional
from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.exceptions import SecurityException
from app.logging.context import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.security")
```

## Classes

| Class | Description |
| --- | --- |
| `SecureRequestMiddleware` |  |
| `SecurityHeadersMiddleware` |  |

### Class: `SecureRequestMiddleware`
**Inherits from:** BaseHTTPMiddleware

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `dispatch` `async` |  |

##### `__init__`
```python
def __init__(self, app, block_suspicious_requests) -> None:
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```

### Class: `SecurityHeadersMiddleware`
**Inherits from:** BaseHTTPMiddleware

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `dispatch` `async` |  |

##### `__init__`
```python
def __init__(self, app, content_security_policy, permissions_policy, expect_ct) -> None:
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
