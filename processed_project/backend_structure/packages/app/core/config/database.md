# Module: app.core.config.database

**Path:** `app/core/config/database.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Optional, List, Any
from pydantic import PostgresDsn, SecretStr, model_validator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

## Classes

| Class | Description |
| --- | --- |
| `DatabaseSettings` |  |

### Class: `DatabaseSettings`
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
            # Disable JSON parsing for these fields
            "POSTGRES_SCHEMAS": {"env_mode": "str"},
        },
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `assemble_db_connection` |  |
| `parse_str_to_list` |  |
| `redis_uri` `@property` |  |

##### `assemble_db_connection`
```python
@model_validator(mode='after')
def assemble_db_connection(self) -> 'DatabaseSettings':
```

##### `parse_str_to_list`
```python
@field_validator('DB_SCHEMAS', mode='before')
@classmethod
def parse_str_to_list(cls, v) -> List[str]:
```

##### `redis_uri`
```python
@property
def redis_uri(self) -> str:
```
