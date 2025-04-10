# Module: app.core.security.passwords

**Path:** `app/core/security/passwords.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import re
from pathlib import Path
from typing import Optional, Set, Tuple
from passlib.context import CryptContext
from app.core.config import settings
from app.logging import get_logger
from app.core.security.models import PasswordPolicy
```

## Global Variables
```python
logger = logger = get_logger("app.core.security.passwords")
pwd_context = pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

## Functions

| Function | Description |
| --- | --- |
| `get_password_hash` |  |
| `validate_password_policy` |  |
| `verify_password` |  |

### `get_password_hash`
```python
def get_password_hash(password) -> str:
```

### `validate_password_policy`
```python
async def validate_password_policy(password, user_id) -> Tuple[(bool, Optional[str])]:
```

### `verify_password`
```python
def verify_password(plain_password, hashed_password) -> bool:
```

## Classes

| Class | Description |
| --- | --- |
| `PasswordManager` |  |

### Class: `PasswordManager`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `hash_password` |  |
| `validate_password_policy` `async` |  |
| `verify_password` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `hash_password`
```python
def hash_password(self, password) -> str:
```

##### `validate_password_policy`
```python
async def validate_password_policy(self, password, user_id) -> Tuple[(bool, Optional[str])]:
```

##### `verify_password`
```python
def verify_password(self, plain_password, hashed_password) -> bool:
```
