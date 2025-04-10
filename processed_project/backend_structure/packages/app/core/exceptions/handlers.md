# Module: app.core.exceptions.handlers

**Path:** `app/core/exceptions/handlers.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
import traceback
from typing import Dict, Any
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.core.exceptions.base import AppException, ErrorCode, ErrorDetail, ErrorResponse, ErrorSeverity
from app.logging.context import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.exceptions.handlers")
```

## Functions

| Function | Description |
| --- | --- |
| `app_exception_handler` |  |
| `generic_exception_handler` |  |
| `validation_exception_handler` |  |

### `app_exception_handler`
```python
async def app_exception_handler(request, exc) -> JSONResponse:
```

### `generic_exception_handler`
```python
async def generic_exception_handler(request, exc) -> JSONResponse:
```

### `validation_exception_handler`
```python
async def validation_exception_handler(request, exc) -> JSONResponse:
```
