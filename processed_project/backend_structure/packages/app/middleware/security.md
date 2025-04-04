# Module: app.middleware.security

**Path:** `app/middleware/security.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.metrics import MetricName
from app.utils.circuit_breaker_utils import safe_observe_histogram, safe_increment_counter
import re
import time
from typing import Callable, Dict, List, Optional, Any, Pattern
from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.exceptions import SecurityException, ErrorCode
from app.logging.context import get_logger
from app.core.dependency_manager import get_service
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
def __init__(self, app, block_suspicious_requests, suspicious_patterns, suspicious_regex_patterns, exclude_paths) -> None:
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
def __init__(self, app, content_security_policy, permissions_policy, expect_ct, hsts_max_age, include_subdomains, preload, exclude_paths) -> None:
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
