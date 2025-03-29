# Module: app.core.security.validation

**Path:** `app/core/security/validation.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import ipaddress
import json
import re
from typing import Any, Dict, Set, Tuple, Optional, Type
from enum import Enum
from app.core.config import settings
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.security.validation")
```

## Functions

| Function | Description |
| --- | --- |
| `detect_suspicious_content` |  |
| `get_security_headers` |  |
| `is_trusted_ip` |  |
| `is_valid_enum_value` |  |
| `is_valid_hostname` |  |
| `moderate_content` |  |
| `sanitize_input` |  |
| `validate_json_input` |  |

### `detect_suspicious_content`
```python
def detect_suspicious_content(content) -> bool:
```

### `get_security_headers`
```python
def get_security_headers() -> Dict[(str, str)]:
```

### `is_trusted_ip`
```python
def is_trusted_ip(ip_address) -> bool:
```

### `is_valid_enum_value`
```python
def is_valid_enum_value(enum_class, value) -> bool:
```

### `is_valid_hostname`
```python
def is_valid_hostname(hostname) -> bool:
```

### `moderate_content`
```python
def moderate_content(content, content_type) -> Tuple[(bool, Optional[str])]:
```

### `sanitize_input`
```python
def sanitize_input(input_str) -> str:
```

### `validate_json_input`
```python
def validate_json_input(json_data) -> bool:
```

## Classes

| Class | Description |
| --- | --- |
| `ValidationManager` |  |

### Class: `ValidationManager`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `detect_suspicious_content` |  |
| `get_security_headers` |  |
| `is_trusted_ip` |  |
| `is_valid_enum_value` |  |
| `is_valid_hostname` |  |
| `moderate_content` |  |
| `sanitize_input` |  |
| `validate_json_input` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `detect_suspicious_content`
```python
def detect_suspicious_content(self, content) -> bool:
```

##### `get_security_headers`
```python
def get_security_headers(self) -> Dict[(str, str)]:
```

##### `is_trusted_ip`
```python
def is_trusted_ip(self, ip_address) -> bool:
```

##### `is_valid_enum_value`
```python
def is_valid_enum_value(self, enum_class, value) -> bool:
```

##### `is_valid_hostname`
```python
def is_valid_hostname(self, hostname) -> bool:
```

##### `moderate_content`
```python
def moderate_content(self, content, content_type) -> Tuple[(bool, Optional[str])]:
```

##### `sanitize_input`
```python
def sanitize_input(self, input_str) -> str:
```

##### `validate_json_input`
```python
def validate_json_input(self, json_data) -> bool:
```
