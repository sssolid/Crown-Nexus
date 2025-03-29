# Module: app.core.rate_limiting.exceptions

**Path:** `app/core/rate_limiting/exceptions.py`

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
| `RateLimitExceededException` |  |
| `RateLimitingConfigurationException` |  |
| `RateLimitingException` |  |
| `RateLimitingServiceException` |  |

### Class: `RateLimitExceededException`
**Inherits from:** RateLimitingException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, headers, reset_seconds, original_exception) -> None:
```

### Class: `RateLimitingConfigurationException`
**Inherits from:** RateLimitingException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, original_exception) -> None:
```

### Class: `RateLimitingException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, original_exception) -> None:
```

### Class: `RateLimitingServiceException`
**Inherits from:** RateLimitingException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, original_exception) -> None:
```
