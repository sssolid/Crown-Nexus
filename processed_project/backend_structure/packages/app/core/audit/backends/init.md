# Module: app.core.audit.backends

**Path:** `app/core/audit/backends/__init__.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit.base import AuditBackend
from app.core.config import settings
from app.logging import get_logger
from app.core.audit.backends.database import DatabaseAuditBackend
from app.core.audit.backends.file import FileAuditBackend
from app.core.audit.backends.logging import LoggingAuditBackend
```

## Global Variables
```python
logger = logger = get_logger("app.core.audit.backends")
__all__ = __all__ = [
    "get_backend",
    "create_default_backends",
    "register_backend",
    "LoggingAuditBackend",
    "FileAuditBackend",
    "DatabaseAuditBackend",
]
```

## Functions

| Function | Description |
| --- | --- |
| `create_default_backends` |  |
| `get_backend` |  |
| `register_backend` |  |

### `create_default_backends`
```python
def create_default_backends(db) -> List[AuditBackend]:
```

### `get_backend`
```python
def get_backend(name, **kwargs) -> AuditBackend:
```

### `register_backend`
```python
def register_backend(name, backend_class) -> None:
```
