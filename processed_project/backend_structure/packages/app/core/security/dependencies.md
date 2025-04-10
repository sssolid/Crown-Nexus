# Module: app.core.security.dependencies

**Path:** `app/core/security/dependencies.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import time
from typing import Optional, Union
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.dependency_manager import get_service
from app.core.error import handle_exception
from app.core.exceptions import AuthenticationException
from app.logging import get_logger, set_user_id
from app.core.security.service import get_security_service
from app.core.security.tokens import decode_token
```

## Global Variables
```python
logger = logger = get_logger("app.core.security.dependencies")
oauth2_scheme = oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
optional_oauth2_scheme = optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False
)
```

## Functions

| Function | Description |
| --- | --- |
| `get_current_user_id` |  |
| `get_current_user_with_permissions` |  |
| `get_optional_user_id` |  |
| `get_token_from_header` |  |

### `get_current_user_id`
```python
async def get_current_user_id(token, request) -> str:
```

### `get_current_user_with_permissions`
```python
async def get_current_user_with_permissions(token, request, db) -> Union[(dict, Any)]:
```

### `get_optional_user_id`
```python
async def get_optional_user_id(token, request) -> Optional[str]:
```

### `get_token_from_header`
```python
async def get_token_from_header(token, request) -> str:
```
