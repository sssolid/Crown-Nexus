# Module: app.core.cache.exceptions

**Path:** `app/core/cache/exceptions.py`

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
| `CacheConfigurationException` |  |
| `CacheConnectionException` |  |
| `CacheException` |  |
| `CacheOperationException` |  |

### Class: `CacheConfigurationException`
**Inherits from:** CacheException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, original_exception) -> None:
```

### Class: `CacheConnectionException`
**Inherits from:** CacheException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, backend, details, original_exception) -> None:
```

### Class: `CacheException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, original_exception) -> None:
```

### Class: `CacheOperationException`
**Inherits from:** CacheException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, operation, key, details, original_exception) -> None:
```
