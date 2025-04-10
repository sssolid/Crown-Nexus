# Module: app.domains.users.repository

**Path:** `app/domains/users/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.users.models import User, UserRole
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, AuthenticationException
```

## Classes

| Class | Description |
| --- | --- |
| `UserRepository` |  |

### Class: `UserRepository`
**Inherits from:** BaseRepository[(User, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `authenticate` `async` |  |
| `ensure_exists` `async` |  |
| `find_by_email` `async` |  |
| `get_by_company` `async` |  |
| `get_by_role` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `authenticate`
```python
async def authenticate(self, email, password) -> User:
```

##### `ensure_exists`
```python
async def ensure_exists(self, user_id) -> User:
```

##### `find_by_email`
```python
async def find_by_email(self, email) -> Optional[User]:
```

##### `get_by_company`
```python
async def get_by_company(self, company_id, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_role`
```python
async def get_by_role(self, role) -> List[User]:
```
