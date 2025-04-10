# Module: app.core.config.integrations.filemaker

**Path:** `app/core/config/integrations/filemaker.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import json
import logging
from typing import Any, Dict, List, Optional, Union
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

## Global Variables
```python
filemaker_settings = filemaker_settings = FilemakerSettings()
```

## Functions

| Function | Description |
| --- | --- |
| `get_filemaker_connector_config` |  |

### `get_filemaker_connector_config`
```python
def get_filemaker_connector_config() -> Dict[(str, Any)]:
```

## Classes

| Class | Description |
| --- | --- |
| `FilemakerSettings` |  |

### Class: `FilemakerSettings`
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
            "FILEMAKER_ALLOWED_TABLES": {"env_mode": "str"},
            "FILEMAKER_ALLOWED_LAYOUTS": {"env_mode": "str"},
            "FILEMAKER_SYNC_LAYOUTS": {"env_mode": "str"},
        },
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `parse_boolean` |  |
| `parse_str_to_list` |  |
| `parse_sync_layouts` |  |
| `validate_interval` |  |
| `validate_port` |  |

##### `parse_boolean`
```python
@field_validator('FILEMAKER_SSL', 'FILEMAKER_ENCRYPT_CONNECTION', 'FILEMAKER_SYNC_ENABLED', 'FILEMAKER_USE_EXTENDED_STATEMENTS', mode='before')
@classmethod
def parse_boolean(cls, v) -> bool:
```

##### `parse_str_to_list`
```python
@field_validator('FILEMAKER_ALLOWED_TABLES', 'FILEMAKER_ALLOWED_LAYOUTS', mode='before')
@classmethod
def parse_str_to_list(cls, v) -> List[str]:
```

##### `parse_sync_layouts`
```python
@field_validator('FILEMAKER_SYNC_LAYOUTS', mode='before')
@classmethod
def parse_sync_layouts(cls, v) -> Dict[(str, str)]:
```

##### `validate_interval`
```python
@field_validator('FILEMAKER_SYNC_INTERVAL')
@classmethod
def validate_interval(cls, v) -> int:
```

##### `validate_port`
```python
@field_validator('FILEMAKER_PORT')
@classmethod
def validate_port(cls, v) -> Optional[int]:
```
