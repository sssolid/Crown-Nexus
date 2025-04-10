# Module: app.core.security.service

**Path:** `app/core/security/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from app.core.dependency_manager import get_service, register_service
from app.core.error import ErrorContext, handle_exception, report_error
from app.core.exceptions import AuthenticationException, SecurityException
from app.core.security.api_keys import ApiKeyManager
from app.core.security.csrf import CsrfManager
from app.core.security.encryption import EncryptionManager
from app.core.security.models import ApiKeyData, TokenClaimsModel, TokenPair, TokenType
from app.core.security.passwords import PasswordManager
from app.core.security.tokens import TokenManager, add_token_to_blacklist, decode_token, is_token_blacklisted
from app.core.security.validation import ValidationManager
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.security.service")
```

## Functions

| Function | Description |
| --- | --- |
| `get_security_service` |  |

### `get_security_service`
```python
@register_service
def get_security_service(db) -> SecurityService:
```

## Classes

| Class | Description |
| --- | --- |
| `SecurityService` |  |

### Class: `SecurityService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `create_token_pair` `async` |  |
| `decrypt_data` |  |
| `detect_suspicious_content` |  |
| `encrypt_data` |  |
| `generate_api_key` |  |
| `generate_csrf_token` |  |
| `generate_secure_token` |  |
| `get_security_headers` |  |
| `hash_password` |  |
| `initialize` `async` |  |
| `is_trusted_ip` |  |
| `refresh_tokens` `async` |  |
| `revoke_token` `async` |  |
| `sanitize_input` |  |
| `shutdown` `async` |  |
| `validate_csrf_token` |  |
| `validate_password_policy` `async` |  |
| `validate_token` `async` |  |
| `verify_api_key` |  |
| `verify_password` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `create_token_pair`
```python
async def create_token_pair(self, user_id, role, permissions, user_data) -> TokenPair:
```

##### `decrypt_data`
```python
def decrypt_data(self, encrypted_data) -> Union[(str, dict)]:
```

##### `detect_suspicious_content`
```python
def detect_suspicious_content(self, content) -> bool:
```

##### `encrypt_data`
```python
def encrypt_data(self, data) -> str:
```

##### `generate_api_key`
```python
def generate_api_key(self, user_id, name, permissions) -> ApiKeyData:
```

##### `generate_csrf_token`
```python
def generate_csrf_token(self, session_id) -> str:
```

##### `generate_secure_token`
```python
def generate_secure_token(self, length) -> str:
```

##### `get_security_headers`
```python
def get_security_headers(self) -> Dict[(str, str)]:
```

##### `hash_password`
```python
def hash_password(self, password) -> str:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `is_trusted_ip`
```python
def is_trusted_ip(self, ip_address) -> bool:
```

##### `refresh_tokens`
```python
async def refresh_tokens(self, refresh_token, request_id) -> TokenPair:
```

##### `revoke_token`
```python
async def revoke_token(self, token, user_id, reason, request_id) -> None:
```

##### `sanitize_input`
```python
def sanitize_input(self, input_str) -> str:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

##### `validate_csrf_token`
```python
def validate_csrf_token(self, token, session_id) -> bool:
```

##### `validate_password_policy`
```python
async def validate_password_policy(self, password, user_id) -> Tuple[(bool, Optional[str])]:
```

##### `validate_token`
```python
async def validate_token(self, token, request_id) -> TokenClaimsModel:
```

##### `verify_api_key`
```python
def verify_api_key(self, api_key, stored_hash) -> bool:
```

##### `verify_password`
```python
async def verify_password(self, plain_password, hashed_password, user_id) -> bool:
```
