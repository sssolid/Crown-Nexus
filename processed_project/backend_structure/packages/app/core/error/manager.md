# Module: app.core.error.manager

**Path:** `app/core/error/manager.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import functools
import inspect
import traceback
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast, Union
from app.core.exceptions import BusinessException, ErrorCode, PermissionDeniedException, ResourceAlreadyExistsException, ResourceNotFoundException, ValidationException
from app.logging.context import get_logger
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
| `create_error_context` |  |
| `ensure_not_none` |  |
| `error_context_decorator` |  |
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

### `create_error_context`
```python
def create_error_context(function_name, args, kwargs, user_id, request_id) -> ErrorContext:
```

### `ensure_not_none`
```python
def ensure_not_none(value, resource_type, resource_id, message) -> T:
```

### `error_context_decorator`
```python
def error_context_decorator(user_id_param, request_id_param) -> Callable[([Callable[(Ellipsis, Any)]], Callable[(Ellipsis, Any)])]:
```

### `handle_exception`
```python
def handle_exception(exception, request_id, user_id, function_name) -> None:
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
