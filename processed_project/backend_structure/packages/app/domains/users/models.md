# Module: app.domains.users.models

**Path:** `app/domains/users/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from jose import jwt
from passlib.context import CryptContext
import sqlalchemy as sa
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.core.config import settings
from app.db.base_class import Base
from app.domains.company.models import Company
from app.domains.api_key.models import ApiKey
from app.domains.media.models import Media
from app.domains.chat.models import ChatMember
```

## Global Variables
```python
pwd_context = pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

## Functions

| Function | Description |
| --- | --- |
| `create_access_token` |  |
| `get_password_hash` |  |
| `verify_password` |  |

### `create_access_token`
```python
def create_access_token(subject, role, expires_delta) -> str:
```

### `get_password_hash`
```python
def get_password_hash(password) -> str:
```

### `verify_password`
```python
def verify_password(plain_password, hashed_password) -> bool:
```

## Classes

| Class | Description |
| --- | --- |
| `User` |  |
| `UserRole` |  |

### Class: `User`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'user'` |
| `__table_args__` | `    __table_args__ = {"schema": "user"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `UserRole`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `ADMIN` | `'admin'` |
| `MANAGER` | `'manager'` |
| `CLIENT` | `'client'` |
| `DISTRIBUTOR` | `'distributor'` |
| `READ_ONLY` | `'read_only'` |
