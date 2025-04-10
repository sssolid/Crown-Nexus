# Module: app.core.security.csrf

**Path:** `app/core/security/csrf.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import hmac
import secrets
import time
from typing import Optional, Tuple
from app.core.config import settings
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.security.csrf")
```

## Functions

| Function | Description |
| --- | --- |
| `generate_csrf_token` |  |
| `validate_csrf_token` |  |

### `generate_csrf_token`
```python
def generate_csrf_token(session_id) -> str:
```

### `validate_csrf_token`
```python
def validate_csrf_token(token, session_id) -> bool:
```

## Classes

| Class | Description |
| --- | --- |
| `CsrfManager` |  |

### Class: `CsrfManager`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `generate_token` |  |
| `parse_token` |  |
| `validate_token` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `generate_token`
```python
def generate_token(self, session_id) -> str:
```

##### `parse_token`
```python
def parse_token(self, token) -> Optional[Tuple[(str, int, str, str)]]:
```

##### `validate_token`
```python
def validate_token(self, token, session_id) -> bool:
```
