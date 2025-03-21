# Module: app.core.permissions.permissions

**Path:** `app/core/permissions/permissions.py`

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
require_permission = require_permission = require_permission
require_permissions = require_permissions = require_permissions
require_admin = require_admin = require_admin
```
