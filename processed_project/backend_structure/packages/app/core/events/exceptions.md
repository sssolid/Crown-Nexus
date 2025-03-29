# Module: app.core.events.exceptions

**Path:** `app/core/events/exceptions.py`

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
| `EventBackendException` |  |
| `EventConfigurationException` |  |
| `EventException` |  |
| `EventHandlerException` |  |
| `EventPublishException` |  |
| `EventServiceException` |  |

### Class: `EventBackendException`
**Inherits from:** EventException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, backend_type, details, original_exception) -> None:
```

### Class: `EventConfigurationException`
**Inherits from:** EventException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, original_exception) -> None:
```

### Class: `EventException`
**Inherits from:** AppException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, original_exception) -> None:
```

### Class: `EventHandlerException`
**Inherits from:** EventException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, event_name, handler_name, details, original_exception) -> None:
```

### Class: `EventPublishException`
**Inherits from:** EventException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, event_name, details, original_exception) -> None:
```

### Class: `EventServiceException`
**Inherits from:** EventException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, original_exception) -> None:
```
