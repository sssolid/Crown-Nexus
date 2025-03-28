# Module: app.api.v1.endpoints.users

**Path:** `app/api/v1/endpoints/users.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.domains.company.models import Company
from app.domains.company.schemas import CompanyCreate, CompanyUpdate
from app.domains.users.models import User, UserRole, get_password_hash
from app.domains.users.schemas import Company as CompanySchema, User as UserSchema, UserCreate, UserUpdate
```

## Global Variables
```python
router = router = APIRouter()
```

## Functions

| Function | Description |
| --- | --- |
| `create_company` |  |
| `create_user` |  |
| `delete_company` |  |
| `delete_user` |  |
| `read_companies` |  |
| `read_company` |  |
| `read_user` |  |
| `read_user_me` |  |
| `read_users` |  |
| `update_company` |  |
| `update_user` |  |

### `create_company`
```python
@router.post('/companies/', response_model=CompanySchema, status_code=status.HTTP_201_CREATED)
async def create_company(company_in, db, current_user) -> Any:
```

### `create_user`
```python
@router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_in, db, current_user) -> Any:
```

### `delete_company`
```python
@router.delete('/companies/{company_id}')
async def delete_company(company_id, db, current_user) -> dict:
```

### `delete_user`
```python
@router.delete('/{user_id}')
async def delete_user(user_id, db, current_user) -> dict:
```

### `read_companies`
```python
@router.get('/companies/', response_model=List[CompanySchema])
async def read_companies(db, current_user, skip, limit, is_active) -> Any:
```

### `read_company`
```python
@router.get('/companies/{company_id}', response_model=CompanySchema)
async def read_company(company_id, db, current_user) -> Any:
```

### `read_user`
```python
@router.get('/{user_id}', response_model=UserSchema)
async def read_user(user_id, db, current_user) -> Any:
```

### `read_user_me`
```python
@router.get('/me', response_model=UserSchema)
async def read_user_me(current_user, db) -> Any:
```

### `read_users`
```python
@router.get('/', response_model=List[UserSchema])
async def read_users(db, current_user, skip, limit, role, company_id, is_active) -> Any:
```

### `update_company`
```python
@router.put('/companies/{company_id}', response_model=CompanySchema)
async def update_company(company_id, company_in, db, current_user) -> Any:
```

### `update_user`
```python
@router.put('/{user_id}', response_model=UserSchema)
async def update_user(user_id, user_in, db, current_user) -> Any:
```
