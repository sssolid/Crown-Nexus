# Module: app.core.pagination.exceptions

**Path:** `app/core/pagination/exceptions.py`

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
| `InvalidCursorException` |  |
| `InvalidPaginationParamsException` |  |
| `InvalidSortFieldException` |  |
| `PaginationException` |  |

### Class: `InvalidCursorException`
**Inherits from:** PaginationException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, cursor, details, original_exception) -> None:
```

### Class: `InvalidPaginationParamsException`
**Inherits from:** PaginationException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, params, details, original_exception) -> None:
```

### Class: `InvalidSortFieldException`
**Inherits from:** PaginationException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, field, model, message, details, original_exception) -> None:
```

### Class: `PaginationException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, original_exception) -> None:
```
