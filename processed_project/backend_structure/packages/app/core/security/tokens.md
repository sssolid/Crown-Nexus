# Module: app.core.security.tokens

**Path:** `app/core/security/tokens.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
import uuid
from typing import Any, Dict, List, Optional, Union
from jose import JWTError, jwt
from pydantic import ValidationError
from app.core.config import settings
from app.core.exceptions import AuthenticationException
from app.logging import get_logger
from app.core.security.models import TokenClaimsModel, TokenPair, TokenType
from app.utils.redis_manager import get_key, set_key
```

## Global Variables
```python
logger = logger = get_logger("app.core.security.tokens")
```

## Functions

| Function | Description |
| --- | --- |
| `add_token_to_blacklist` |  |
| `create_token` |  |
| `create_token_pair` |  |
| `decode_token` |  |
| `generate_token_jti` |  |
| `is_token_blacklisted` |  |
| `refresh_tokens` |  |
| `revoke_token` |  |

### `add_token_to_blacklist`
```python
async def add_token_to_blacklist(token_jti, expires_at) -> None:
```

### `create_token`
```python
def create_token(subject, token_type, expires_delta, role, permissions, user_data) -> str:
```

### `create_token_pair`
```python
def create_token_pair(user_id, role, permissions, user_data) -> TokenPair:
```

### `decode_token`
```python
async def decode_token(token) -> TokenClaimsModel:
```

### `generate_token_jti`
```python
def generate_token_jti() -> str:
```

### `is_token_blacklisted`
```python
async def is_token_blacklisted(token_jti) -> bool:
```

### `refresh_tokens`
```python
async def refresh_tokens(refresh_token) -> TokenPair:
```

### `revoke_token`
```python
async def revoke_token(token) -> None:
```

## Classes

| Class | Description |
| --- | --- |
| `TokenManager` |  |

### Class: `TokenManager`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self) -> None:
```
