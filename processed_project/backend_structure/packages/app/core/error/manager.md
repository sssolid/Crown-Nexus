# Module: app.core.error.manager

**Path:** `app/core/error/manager.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import inspect
from typing import Any, Dict, List, Optional, TypeVar
from app.core.exceptions import AppException, AuthenticationException, BusinessException, ErrorCode, PermissionDeniedException, ResourceAlreadyExistsException, ResourceNotFoundException, ValidationException
from app.core.logging import get_logger
from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory
```

## Global Variables
```python
logger = logger = get_logger("app.core.error.manager")
T = T = TypeVar("T")
```

## Functions

| Function | Description |
| --- | --- |
| `business_logic_error` |  |
| `ensure_not_none` |  |
| `handle_exception` |  |
| `initialize` |  |
| `permission_denied` |  |
| `register_reporter` |  |
| `report_error` |  |
| `resource_already_exists` |  |
| `resource_not_found` |  |
| `shutdown` |  |
| `validation_error` |  |

### `business_logic_error`
```python
def business_logic_error(message, details) -> BusinessException:
```

### `ensure_not_none`
```python
def ensure_not_none(value, resource_type, resource_id, message) -> T:
```

### `handle_exception`
```python
def handle_exception(exception, request_id) -> None:
```

### `initialize`
```python
async def initialize() -> None:
```

### `permission_denied`
```python
def permission_denied(action, resource_type, permission) -> PermissionDeniedException:
```

### `register_reporter`
```python
def register_reporter(reporter) -> None:
```

### `report_error`
```python
async def report_error(exception, context) -> None:
```

### `resource_already_exists`
```python
def resource_already_exists(resource_type, identifier, field, message) -> ResourceAlreadyExistsException:
```

### `resource_not_found`
```python
def resource_not_found(resource_type, resource_id, message) -> ResourceNotFoundException:
```

### `shutdown`
```python
async def shutdown() -> None:
```

### `validation_error`
```python
def validation_error(field, message, error_type) -> ValidationException:
```
