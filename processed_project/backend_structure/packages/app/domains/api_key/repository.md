# Module: app.domains.api_key.repository

**Path:** `app/domains/api_key/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.api_key.models import ApiKey
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

## Classes

| Class | Description |
| --- | --- |
| `ApiKeyRepository` |  |

### Class: `ApiKeyRepository`
**Inherits from:** BaseRepository[(ApiKey, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `clean_expired_keys` `async` |  |
| `create_api_key` `async` |  |
| `ensure_exists` `async` |  |
| `find_by_key_id` `async` |  |
| `get_by_user` `async` |  |
| `revoke_all_user_keys` `async` |  |
| `revoke_api_key` `async` |  |
| `verify_api_key` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `clean_expired_keys`
```python
async def clean_expired_keys(self) -> int:
```

##### `create_api_key`
```python
async def create_api_key(self, user_id, name, permissions, extra_metadata, expires_in_days) -> Tuple[(ApiKey, str)]:
```

##### `ensure_exists`
```python
async def ensure_exists(self, api_key_id) -> ApiKey:
```

##### `find_by_key_id`
```python
async def find_by_key_id(self, key_id) -> Optional[ApiKey]:
```

##### `get_by_user`
```python
async def get_by_user(self, user_id, active_only) -> List[ApiKey]:
```

##### `revoke_all_user_keys`
```python
async def revoke_all_user_keys(self, user_id) -> int:
```

##### `revoke_api_key`
```python
async def revoke_api_key(self, api_key_id) -> bool:
```

##### `verify_api_key`
```python
async def verify_api_key(self, key_id, secret) -> Optional[ApiKey]:
```
