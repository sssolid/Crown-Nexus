# Module: app.core.config.media

**Path:** `app/core/config/media.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import os
from typing import Optional, Set
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.config.base import Environment
```

## Classes

| Class | Description |
| --- | --- |
| `MediaSettings` |  |

### Class: `MediaSettings`
**Inherits from:** BaseSettings

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `create_media_directories` |  |
| `media_base_url` `@property` |  |
| `validate_storage_type` |  |

##### `create_media_directories`
```python
@field_validator('MEDIA_ROOT')
@classmethod
def create_media_directories(cls, v) -> str:
```

##### `media_base_url`
```python
@property
def media_base_url(self) -> str:
```

##### `validate_storage_type`
```python
@field_validator('MEDIA_STORAGE_TYPE')
@classmethod
def validate_storage_type(cls, v) -> str:
```
