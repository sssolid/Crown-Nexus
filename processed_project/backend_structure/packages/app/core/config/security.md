# Module: app.core.config.security

**Path:** `app/core/config/security.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import secrets
from typing import Any, List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

## Global Variables
```python
security_settings = security_settings = SecuritySettings()
```

## Classes

| Class | Description |
| --- | --- |
| `SecuritySettings` |  |

### Class: `SecuritySettings`
**Inherits from:** BaseSettings

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
        json_schema_extra={
            # Disable JSON parsing for these fields that use string-based parsing
            "ALLOWED_HOSTS": {"env_mode": "str"},
            "TRUSTED_PROXIES": {"env_mode": "str"},
            "BACKEND_CORS_ORIGINS": {"env_mode": "str"},
        },
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `assemble_cors_origins` |  |
| `parse_str_to_list` |  |
| `validate_rate_limit_storage` |  |

##### `assemble_cors_origins`
```python
@field_validator('BACKEND_CORS_ORIGINS', mode='before')
@classmethod
def assemble_cors_origins(cls, v) -> List[str]:
```

##### `parse_str_to_list`
```python
@field_validator('ALLOWED_HOSTS', 'TRUSTED_PROXIES', mode='before')
@classmethod
def parse_str_to_list(cls, v) -> List[str]:
```

##### `validate_rate_limit_storage`
```python
@field_validator('RATE_LIMIT_STORAGE')
@classmethod
def validate_rate_limit_storage(cls, v) -> str:
```
