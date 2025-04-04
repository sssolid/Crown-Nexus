# Module: app.middleware.cors

**Path:** `app/middleware/cors.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from app.utils.circuit_breaker_utils import safe_increment_counter
from typing import Callable, Optional, Any, List, Dict, Union
from fastapi import Request, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp
from app.logging import get_logger
from app.core.dependency_manager import get_service
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.cors")
```

## Classes

| Class | Description |
| --- | --- |
| `EnhancedCORSMiddleware` |  |

### Class: `EnhancedCORSMiddleware`
**Inherits from:** CORSMiddleware

#### Methods

| Method | Description |
| --- | --- |
| `__call__` `async` |  |
| `__init__` |  |

##### `__call__`
```python
async def __call__(self, scope, receive, send) -> None:
```

##### `__init__`
```python
def __init__(self, app, allow_origins, allow_methods, allow_headers, allow_credentials, allow_origin_regex, expose_headers, max_age) -> None:
```
