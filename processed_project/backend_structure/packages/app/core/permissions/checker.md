# Module: app.core.permissions.checker

**Path:** `app/core/permissions/checker.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, List, TYPE_CHECKING
from app.core.exceptions import PermissionDeniedException
from app.logging import get_logger
from app.core.permissions.models import Permission, ROLE_PERMISSIONS
from app.domains.users.models import User
```

## Global Variables
```python
logger = logger = get_logger("app.core.permissions.checkers")
permissions = permissions = PermissionChecker()
```

## Classes

| Class | Description |
| --- | --- |
| `PermissionChecker` |  |

### Class: `PermissionChecker`

#### Methods

| Method | Description |
| --- | --- |
| `check_object_permission` |  |
| `ensure_object_permission` |  |
| `has_permission` |  |
| `has_permissions` |  |

##### `check_object_permission`
```python
@staticmethod
def check_object_permission(user, obj, permission, owner_field) -> bool:
```

##### `ensure_object_permission`
```python
@staticmethod
def ensure_object_permission(user, obj, permission, owner_field) -> None:
```

##### `has_permission`
```python
@staticmethod
def has_permission(user, permission) -> bool:
```

##### `has_permissions`
```python
@staticmethod
def has_permissions(user, permissions, require_all) -> bool:
```
