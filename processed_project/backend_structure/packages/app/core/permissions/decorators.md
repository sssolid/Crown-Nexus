# Module: app.core.permissions.decorators

**Path:** `app/core/permissions/decorators.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Callable, List, TypeVar, cast, TYPE_CHECKING
from app.core.exceptions import PermissionDeniedException
from app.logging import get_logger
from app.core.permissions.checker import PermissionChecker
from app.core.permissions.models import Permission
```

## Global Variables
```python
logger = logger = get_logger("app.core.permissions.decorators")
T = T = TypeVar("T", bound=Callable[..., Any])
```

## Functions

| Function | Description |
| --- | --- |
| `require_admin` |  |
| `require_permission` |  |
| `require_permissions` |  |

### `require_admin`
```python
def require_admin() -> Callable[([T], T)]:
```

### `require_permission`
```python
def require_permission(permission) -> Callable[([T], T)]:
```

### `require_permissions`
```python
def require_permissions(permissions, require_all) -> Callable[([T], T)]:
```
