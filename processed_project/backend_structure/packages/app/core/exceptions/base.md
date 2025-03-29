# Module: app.core.exceptions.base

**Path:** `app/core/exceptions/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.logging import get_logger
import traceback
import logging
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator
from app.logging.context import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.exceptions")
```

## Classes

| Class | Description |
| --- | --- |
| `AppException` |  |
| `ErrorCategory` |  |
| `ErrorCode` |  |
| `ErrorDetail` |  |
| `ErrorResponse` |  |
| `ErrorSeverity` |  |

### Class: `AppException`
**Inherits from:** Exception

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `log` |  |
| `to_response` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, severity, category, original_exception) -> None:
```

##### `log`
```python
def log(self, request_id) -> None:
```

##### `to_response`
```python
def to_response(self, request_id) -> ErrorResponse:
```

### Class: `ErrorCategory`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `VALIDATION` | `'validation'` |
| `AUTH` | `'auth'` |
| `RESOURCE` | `'resource'` |
| `SYSTEM` | `'system'` |
| `BUSINESS` | `'business'` |

### Class: `ErrorCode`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `RESOURCE_NOT_FOUND` | `'RESOURCE_NOT_FOUND'` |
| `RESOURCE_ALREADY_EXISTS` | `'RESOURCE_ALREADY_EXISTS'` |
| `AUTHENTICATION_FAILED` | `'AUTHENTICATION_FAILED'` |
| `PERMISSION_DENIED` | `'PERMISSION_DENIED'` |
| `VALIDATION_ERROR` | `'VALIDATION_ERROR'` |
| `BAD_REQUEST` | `'BAD_REQUEST'` |
| `BUSINESS_LOGIC_ERROR` | `'BUSINESS_LOGIC_ERROR'` |
| `INVALID_STATE` | `'INVALID_STATE'` |
| `OPERATION_NOT_ALLOWED` | `'OPERATION_NOT_ALLOWED'` |
| `DATABASE_ERROR` | `'DATABASE_ERROR'` |
| `NETWORK_ERROR` | `'NETWORK_ERROR'` |
| `SERVICE_ERROR` | `'SERVICE_ERROR'` |
| `CONFIGURATION_ERROR` | `'CONFIGURATION_ERROR'` |
| `SECURITY_ERROR` | `'SECURITY_ERROR'` |
| `UNKNOWN_ERROR` | `'UNKNOWN_ERROR'` |

### Class: `ErrorDetail`
**Inherits from:** BaseModel

### Class: `ErrorResponse`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_details` |  |

##### `validate_details`
```python
@field_validator('details', mode='before')
@classmethod
def validate_details(cls, v) -> List[ErrorDetail]:
```

### Class: `ErrorSeverity`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `WARNING` | `'warning'` |
| `ERROR` | `'error'` |
| `CRITICAL` | `'critical'` |
