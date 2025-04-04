# Module: app.domains.users.schemas

**Path:** `app/domains/users/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.domains.company.schemas import Company
```

## Classes

| Class | Description |
| --- | --- |
| `Token` |  |
| `TokenPayload` |  |
| `User` |  |
| `UserBase` |  |
| `UserCreate` |  |
| `UserInDB` |  |
| `UserRole` |  |
| `UserUpdate` |  |

### Class: `Token`
**Inherits from:** BaseModel

### Class: `TokenPayload`
**Inherits from:** BaseModel

### Class: `User`
**Inherits from:** UserInDB

### Class: `UserBase`
**Inherits from:** BaseModel

### Class: `UserCreate`
**Inherits from:** UserBase

#### Methods

| Method | Description |
| --- | --- |
| `password_strength` |  |

##### `password_strength`
```python
@field_validator('password')
@classmethod
def password_strength(cls, v) -> str:
```

### Class: `UserInDB`
**Inherits from:** UserBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

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

### Class: `UserUpdate`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `password_strength` |  |

##### `password_strength`
```python
@field_validator('password')
@classmethod
def password_strength(cls, v) -> Optional[str]:
```
