# Module: app.core.audit.exceptions

**Path:** `app/core/audit/exceptions.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import ErrorCode
from app.core.exceptions.service import BackendError, CoreServiceException, ManagerError
```

## Classes

| Class | Description |
| --- | --- |
| `AuditBackendException` |  |
| `AuditConfigurationException` |  |
| `AuditException` |  |
| `AuditManagerException` |  |

### Class: `AuditBackendException`
**Inherits from:** BackendError

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, backend_name, operation, message, details, original_exception) -> None:
```

### Class: `AuditConfigurationException`
**Inherits from:** AuditException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details, original_exception) -> None:
```

### Class: `AuditException`
**Inherits from:** CoreServiceException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, status_code, original_exception) -> None:
```

### Class: `AuditManagerException`
**Inherits from:** ManagerError

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, operation, message, details, original_exception) -> None:
```
