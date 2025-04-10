# Module: app.api.v1.endpoints.auth

**Path:** `app/api/v1/endpoints/auth.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from datetime import timedelta
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db
from app.core.config import settings
from app.domains.users.models import User, create_access_token, verify_password
from app.domains.users.schemas import Token, TokenPayload, User as UserSchema
```

## Global Variables
```python
router = router = APIRouter()
oauth2_scheme = oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
```

## Functions

| Function | Description |
| --- | --- |
| `login_for_access_token` |  |
| `read_users_me` |  |
| `validate_token` |  |

### `login_for_access_token`
```python
@router.post('/login', response_model=Token)
async def login_for_access_token(db, form_data) -> Any:
```

### `read_users_me`
```python
@router.get('/me', response_model=UserSchema)
async def read_users_me(current_user) -> Any:
```

### `validate_token`
```python
@router.get('/validate-token')
async def validate_token(token) -> dict:
```
