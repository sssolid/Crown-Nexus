# Module: app.core.security.dependencies

**Path:** `app/core/security/dependencies.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.exceptions import AuthenticationException
from app.logging import get_logger
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
| `get_token_from_header` |  |

### `get_current_user_id`
```python
async def get_current_user_id(token) -> str:
```

### `get_token_from_header`
```python
async def get_token_from_header(token) -> str:
```
