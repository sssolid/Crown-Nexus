# Module: app.services.base_service.permissions

**Path:** `app/services/base_service/permissions.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Optional, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AuthenticationException, ErrorCode
from app.logging import get_logger
from app.domains.users.models import User
```

## Global Variables
```python
logger = logger = get_logger("app.services.base_service.permissions")
```

## Classes

| Class | Description |
| --- | --- |
| `PermissionHelper` |  |

### Class: `PermissionHelper`

#### Methods

| Method | Description |
| --- | --- |
| `check_owner_permission` |  |
| `get_user` `async` |  |
| `has_all_permissions` |  |
| `has_any_permission` |  |

##### `check_owner_permission`
```python
@staticmethod
def check_owner_permission(user_id, entity_user_id, owner_field) -> bool:
```

##### `get_user`
```python
@staticmethod
async def get_user(db, user_id) -> User:
```

##### `has_all_permissions`
```python
@staticmethod
def has_all_permissions(user, permissions) -> bool:
```

##### `has_any_permission`
```python
@staticmethod
def has_any_permission(user, permissions) -> bool:
```
