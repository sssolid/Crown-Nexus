# Module: app.core.security.api_keys

**Path:** `app/core/security/api_keys.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import hashlib
import hmac
import secrets
import uuid
import datetime
from typing import List, Optional
from app.logging import get_logger
from app.core.security.models import ApiKeyData, TokenType
from app.core.security.tokens import create_token
```

## Global Variables
```python
logger = logger = get_logger("app.core.security.api_keys")
```

## Functions

| Function | Description |
| --- | --- |
| `generate_api_key` |  |
| `verify_api_key` |  |

### `generate_api_key`
```python
def generate_api_key(user_id, name, permissions) -> ApiKeyData:
```

### `verify_api_key`
```python
def verify_api_key(api_key, stored_hash) -> bool:
```

## Classes

| Class | Description |
| --- | --- |
| `ApiKeyManager` |  |

### Class: `ApiKeyManager`

#### Methods

| Method | Description |
| --- | --- |
| `generate_api_key` |  |
| `parse_api_key` |  |
| `verify_api_key` |  |

##### `generate_api_key`
```python
def generate_api_key(self, user_id, name, permissions) -> ApiKeyData:
```

##### `parse_api_key`
```python
def parse_api_key(self, api_key) -> Optional[str]:
```

##### `verify_api_key`
```python
def verify_api_key(self, api_key, stored_hash) -> bool:
```
