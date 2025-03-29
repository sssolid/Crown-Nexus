# Module: app.core.exceptions.domain

**Path:** `app/core/exceptions/domain.py`

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
| `AuthException` |  |
| `AuthenticationException` |  |
| `BusinessException` |  |
| `InvalidStateException` |  |
| `OperationNotAllowedException` |  |
| `PermissionDeniedException` |  |
| `ResourceAlreadyExistsException` |  |
| `ResourceException` |  |
| `ResourceNotFoundException` |  |
| `ValidationException` |  |

### Class: `AuthException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, original_exception) -> None:
```

### Class: `AuthenticationException`
**Inherits from:** AuthException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, original_exception) -> None:
```

### Class: `BusinessException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, original_exception) -> None:
```

### Class: `InvalidStateException`
**Inherits from:** BusinessException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, current_state, expected_state, details, original_exception) -> None:
```

### Class: `OperationNotAllowedException`
**Inherits from:** BusinessException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, operation, reason, details, original_exception) -> None:
```

### Class: `PermissionDeniedException`
**Inherits from:** AuthException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, action, resource_type, permission, details, original_exception) -> None:
```

### Class: `ResourceAlreadyExistsException`
**Inherits from:** ResourceException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, resource_type, identifier, field, message, details, original_exception) -> None:
```

### Class: `ResourceException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, original_exception) -> None:
```

### Class: `ResourceNotFoundException`
**Inherits from:** ResourceException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, resource_type, resource_id, message, details, original_exception) -> None:
```

### Class: `ValidationException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, errors, details, original_exception) -> None:
```
