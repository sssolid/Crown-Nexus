# Module: app.utils.crypto

**Path:** `app/utils/crypto.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import base64
import os
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.core.config import settings
from app.core.exceptions import ConfigurationException, SecurityException, ErrorCode
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.utils.crypto")
```

## Functions

| Function | Description |
| --- | --- |
| `decrypt_message` |  |
| `encrypt_message` |  |
| `generate_secure_token` |  |

### `decrypt_message`
```python
def decrypt_message(encrypted_message) -> str:
```

### `encrypt_message`
```python
def encrypt_message(message) -> str:
```

### `generate_secure_token`
```python
def generate_secure_token(length) -> str:
```

## Classes

| Class | Description |
| --- | --- |
| `CryptoError` |  |

### Class: `CryptoError`
**Inherits from:** SecurityException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details, original_exception) -> None:
```
