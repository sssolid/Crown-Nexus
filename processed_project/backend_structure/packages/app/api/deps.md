# Module: app.api.deps

**Path:** `app/api/deps.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Dict, List, Optional, Union, Callable
from app.core.security.dependencies import optional_oauth2_scheme
from app.core.audit.service import AuditService
from fastapi import Depends, Query, WebSocket, status
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect
from app.core.exceptions import AuthenticationException, PermissionDeniedException, RateLimitException
from app.logging import get_logger, set_user_id
from app.core.permissions import Permission, PermissionChecker
from app.core.rate_limiting import RateLimiter, RateLimitRule
from app.core.security import decode_token, oauth2_scheme
from app.db.session import get_db
from app.domains.users.models import User, UserRole
from app.domains.users.repository import UserRepository
```

## Global Variables
```python
logger = logger = get_logger("app.api.deps")
PaginationParams = PaginationParams = Dict[str, Union[int, float]]
```

## Functions

| Function | Description |
| --- | --- |
| `get_admin_user` |  |
| `get_audit_service` |  |
| `get_current_active_user` |  |
| `get_current_user` |  |
| `get_current_user_ws` |  |
| `get_manager_user` |  |
| `get_optional_user` |  |
| `get_pagination` |  |
| `rate_limit` |  |
| `require_permission` |  |
| `require_permissions` |  |

### `get_admin_user`
```python
async def get_admin_user(current_user) -> User:
```

### `get_audit_service`
```python
async def get_audit_service(db) -> AuditService:
```

### `get_current_active_user`
```python
async def get_current_active_user(current_user) -> User:
```

### `get_current_user`
```python
async def get_current_user(db, token) -> User:
```

### `get_current_user_ws`
```python
async def get_current_user_ws(websocket, db) -> User:
```

### `get_manager_user`
```python
async def get_manager_user(current_user) -> User:
```

### `get_optional_user`
```python
async def get_optional_user(db, token) -> Optional[User]:
```

### `get_pagination`
```python
def get_pagination(page, page_size) -> PaginationParams:
```

### `rate_limit`
```python
def rate_limit(requests_per_window, window_seconds) -> Callable:
```

### `require_permission`
```python
def require_permission(permission):
```

### `require_permissions`
```python
def require_permissions(permissions, require_all):
```
