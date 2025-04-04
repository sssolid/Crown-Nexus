# Module: app.middleware.compression

**Path:** `app/middleware/compression.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from app.utils.circuit_breaker_utils import safe_observe_histogram
import time
from typing import Callable, Optional, Any, Dict
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import MutableHeaders
import gzip
from app.logging import get_logger
from app.core.dependency_manager import get_service
```

## Global Variables
```python
logger = logger = get_logger("app.middleware.compression")
```

## Classes

| Class | Description |
| --- | --- |
| `CompressionMiddleware` |  |

### Class: `CompressionMiddleware`
**Inherits from:** BaseHTTPMiddleware

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `dispatch` `async` |  |

##### `__init__`
```python
def __init__(self, app, minimum_size, compression_level, exclude_paths) -> None:
```

##### `dispatch`
```python
async def dispatch(self, request, call_next) -> Response:
```
