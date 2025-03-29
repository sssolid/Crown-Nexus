# Module: app.core.permissions.utils

**Path:** `app/core/permissions/utils.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, List, Optional, Set, Union, TYPE_CHECKING
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AuthenticationException
from app.logging import get_logger
from app.domains.users.models import User
```

## Global Variables
```python
logger = logger = get_logger("app.core.permissions.utils")
```

## Functions

| Function | Description |
| --- | --- |
| `check_owner_permission` |  |
| `get_user_by_id` |  |
| `has_all_permissions` |  |
| `has_any_permission` |  |

### `check_owner_permission`
```python
def check_owner_permission(user_id, entity_user_id, owner_field) -> bool:
```

### `get_user_by_id`
```python
async def get_user_by_id(db, user_id) -> 'User':
```

### `has_all_permissions`
```python
def has_all_permissions(user, permissions) -> bool:
```

### `has_any_permission`
```python
def has_any_permission(user, permissions) -> bool:
```
