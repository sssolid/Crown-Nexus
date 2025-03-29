# Module: app.core.permissions.service

**Path:** `app/core/permissions/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import time
from typing import Any, Dict, List, Optional, Set, Union, cast, TYPE_CHECKING
from app.core.dependency_manager import get_service, register_service
from app.core.error import handle_exception
from app.core.exceptions import AuthenticationException, PermissionDeniedException
from app.core.permissions.checker import PermissionChecker
from app.core.permissions.models import Permission, ROLE_PERMISSIONS
from app.core.permissions.utils import get_user_by_id, check_owner_permission
from app.logging import get_logger
from app.domains.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
```

## Global Variables
```python
logger = logger = get_logger("app.core.permissions.service")
```

## Functions

| Function | Description |
| --- | --- |
| `get_permission_service` |  |

### `get_permission_service`
```python
@register_service
def get_permission_service(db) -> PermissionService:
```

## Classes

| Class | Description |
| --- | --- |
| `PermissionService` |  |

### Class: `PermissionService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `check_object_permission` `async` |  |
| `check_permission` `async` |  |
| `check_permissions` `async` |  |
| `ensure_object_permission` `async` |  |
| `ensure_permission` `async` |  |
| `get_user_permissions` `async` |  |
| `initialize` `async` |  |
| `invalidate_permissions_cache` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `check_object_permission`
```python
async def check_object_permission(self, user, obj, permission, owner_field) -> bool:
```

##### `check_permission`
```python
async def check_permission(self, user, permission, resource_id, resource_type) -> bool:
```

##### `check_permissions`
```python
async def check_permissions(self, user, permissions, require_all, resource_id, resource_type) -> bool:
```

##### `ensure_object_permission`
```python
async def ensure_object_permission(self, user, obj, permission, owner_field) -> None:
```

##### `ensure_permission`
```python
async def ensure_permission(self, user, permission, resource_type, resource_id) -> None:
```

##### `get_user_permissions`
```python
async def get_user_permissions(self, user_id) -> Set[Permission]:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `invalidate_permissions_cache`
```python
async def invalidate_permissions_cache(self, user_id) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
