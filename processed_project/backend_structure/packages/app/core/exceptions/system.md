# Module: app.core.exceptions.system

**Path:** `app/core/exceptions/system.py`

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
| `ConfigurationException` |  |
| `DataIntegrityException` |  |
| `DatabaseException` |  |
| `NetworkException` |  |
| `RateLimitException` |  |
| `SecurityException` |  |
| `ServiceException` |  |
| `SystemException` |  |
| `TransactionException` |  |

### Class: `ConfigurationException`
**Inherits from:** SystemException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, component, details, original_exception) -> None:
```

### Class: `DataIntegrityException`
**Inherits from:** DatabaseException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, original_exception) -> None:
```

### Class: `DatabaseException`
**Inherits from:** SystemException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, original_exception) -> None:
```

### Class: `NetworkException`
**Inherits from:** SystemException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, status_code, original_exception) -> None:
```

### Class: `RateLimitException`
**Inherits from:** SecurityException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, headers, original_exception) -> None:
```

### Class: `SecurityException`
**Inherits from:** SystemException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, status_code, original_exception) -> None:
```

### Class: `ServiceException`
**Inherits from:** SystemException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, service_name, details, status_code, original_exception) -> None:
```

### Class: `SystemException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, original_exception) -> None:
```

### Class: `TransactionException`
**Inherits from:** DatabaseException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, original_exception) -> None:
```
