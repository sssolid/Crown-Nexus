# Module: app.core.error.service

**Path:** `app/core/error/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Type
from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory
from app.core.error.manager import business_logic_error, handle_exception, initialize as initialize_manager, permission_denied, register_reporter, report_error, resource_already_exists, resource_not_found, shutdown as shutdown_manager, validation_error
from app.core.error.reporters import CompositeErrorReporter, DatabaseErrorReporter, ExternalServiceReporter, LoggingErrorReporter
from app.logging.context import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.error.service")
```

## Functions

| Function | Description |
| --- | --- |
| `get_error_service` |  |

### `get_error_service`
```python
def get_error_service() -> ErrorService:
```

## Classes

| Class | Description |
| --- | --- |
| `ErrorService` |  |

### Class: `ErrorService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `business_logic_error` |  |
| `handle_exception` |  |
| `initialize` `async` |  |
| `permission_denied` |  |
| `register_reporter` `async` |  |
| `register_reporter_by_name` `async` |  |
| `report_error` `async` |  |
| `resource_already_exists` |  |
| `resource_not_found` |  |
| `shutdown` `async` |  |
| `validation_error` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `business_logic_error`
```python
def business_logic_error(self, message, details) -> Exception:
```

##### `handle_exception`
```python
def handle_exception(self, exception, request_id, user_id, function_name) -> None:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `permission_denied`
```python
def permission_denied(self, action, resource_type, permission) -> Exception:
```

##### `register_reporter`
```python
async def register_reporter(self, reporter) -> None:
```

##### `register_reporter_by_name`
```python
async def register_reporter_by_name(self, reporter_name) -> None:
```

##### `report_error`
```python
async def report_error(self, exception, context) -> None:
```

##### `resource_already_exists`
```python
def resource_already_exists(self, resource_type, identifier, field, message) -> Exception:
```

##### `resource_not_found`
```python
def resource_not_found(self, resource_type, resource_id, message) -> Exception:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

##### `validation_error`
```python
def validation_error(self, field, message, error_type) -> Exception:
```
