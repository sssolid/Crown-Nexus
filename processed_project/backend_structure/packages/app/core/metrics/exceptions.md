# Module: app.core.metrics.exceptions

**Path:** `app/core/metrics/exceptions.py`

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
| `MetricsConfigurationException` |  |
| `MetricsException` |  |
| `MetricsOperationException` |  |

### Class: `MetricsConfigurationException`
**Inherits from:** MetricsException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, original_exception) -> None:
```

### Class: `MetricsException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, original_exception) -> None:
```

### Class: `MetricsOperationException`
**Inherits from:** MetricsException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, operation, details, original_exception) -> None:
```
