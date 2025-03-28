# Module: app.core.permissions

**Path:** `app/core/permissions/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.permissions.models import Permission, UserRole, ROLE_PERMISSIONS
from app.core.permissions.checker import PermissionChecker, permissions
from app.core.permissions.decorators import require_permission, require_permissions, require_admin
from app.core.permissions.utils import get_user_by_id, check_owner_permission, has_any_permission, has_all_permissions
```

## Global Variables
```python
__all__ = __all__ = [
    # Models
    "Permission",
    "UserRole",
    "ROLE_PERMISSIONS",
    # Checker
    "PermissionChecker",
    "permissions",
    # Decorators
    "require_permission",
    "require_permissions",
    "require_admin",
    # Utilities
    "get_user_by_id",
    "check_owner_permission",
    "has_any_permission",
    "has_all_permissions",
]
```
