# Module: app.core.exceptions.service

**Path:** `app/core/exceptions/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
```

## Classes

| Class | Description |
| --- | --- |
| `BackendError` |  |
| `ConfigurationError` |  |
| `CoreServiceException` |  |
| `ManagerError` |  |
| `ServiceInitializationError` |  |
| `ServiceNotInitializedError` |  |
| `ServiceShutdownError` |  |

### Class: `BackendError`
**Inherits from:** CoreServiceException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, backend_name, operation, message, details, original_exception) -> None:
```

### Class: `ConfigurationError`
**Inherits from:** CoreServiceException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, service_name, message, details, original_exception) -> None:
```

### Class: `CoreServiceException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, severity, original_exception) -> None:
```

### Class: `ManagerError`
**Inherits from:** CoreServiceException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, manager_name, operation, message, details, original_exception) -> None:
```

### Class: `ServiceInitializationError`
**Inherits from:** CoreServiceException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, service_name, message, details, original_exception) -> None:
```

### Class: `ServiceNotInitializedError`
**Inherits from:** CoreServiceException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, service_name, message, details, original_exception) -> None:
```

### Class: `ServiceShutdownError`
**Inherits from:** CoreServiceException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, service_name, message, details, original_exception) -> None:
```
