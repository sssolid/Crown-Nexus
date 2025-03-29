# Module: app.core.security.encryption

**Path:** `app/core/security/encryption.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import base64
import binascii
import json
from typing import Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.core.config import settings
from app.core.exceptions import SecurityException, ErrorCode, ConfigurationException
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.security.encryption")
```

## Functions

| Function | Description |
| --- | --- |
| `decrypt_data` |  |
| `encrypt_data` |  |
| `generate_secure_token` |  |

### `decrypt_data`
```python
def decrypt_data(encrypted_data) -> Union[(str, dict)]:
```

### `encrypt_data`
```python
def encrypt_data(data) -> str:
```

### `generate_secure_token`
```python
def generate_secure_token(length) -> str:
```

## Classes

| Class | Description |
| --- | --- |
| `EncryptionManager` |  |

### Class: `EncryptionManager`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `decrypt_data` |  |
| `encrypt_data` |  |
| `generate_secure_token` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `decrypt_data`
```python
def decrypt_data(self, encrypted_data) -> Union[(str, dict)]:
```

##### `encrypt_data`
```python
def encrypt_data(self, data) -> str:
```

##### `generate_secure_token`
```python
def generate_secure_token(self, length) -> str:
```
