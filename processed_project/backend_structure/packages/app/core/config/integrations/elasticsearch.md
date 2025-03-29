# Module: app.core.config.integrations.elasticsearch

**Path:** `app/core/config/integrations/elasticsearch.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Optional
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
```

## Global Variables
```python
elasticsearch_settings = elasticsearch_settings = ElasticsearchSettings()
```

## Classes

| Class | Description |
| --- | --- |
| `ElasticsearchSettings` |  |

### Class: `ElasticsearchSettings`
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
| `elasticsearch_uri` `@property` |  |

##### `elasticsearch_uri`
```python
@property
def elasticsearch_uri(self) -> str:
```
