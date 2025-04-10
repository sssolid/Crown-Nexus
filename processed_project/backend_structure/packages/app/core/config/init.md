# Module: app.core.config

**Path:** `app/core/config/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.config.base import Environment, LogLevel
from app.core.config.settings import Settings, get_settings, settings
from app.core.config.integrations import AS400Settings, as400_settings, get_as400_connector_config, FilemakerSettings, filemaker_settings, get_filemaker_connector_config, ElasticsearchSettings, elasticsearch_settings
```

## Global Variables
```python
__all__ = __all__ = [
    "Settings",
    "Environment",
    "LogLevel",
    "get_settings",
    "settings",
    "AS400Settings",
    "FilemakerSettings",
    "ElasticsearchSettings",
    "as400_settings",
    "filemaker_settings",
    "elasticsearch_settings",
    "get_as400_connector_config",
    "get_filemaker_connector_config",
]
```

## Functions

| Function | Description |
| --- | --- |
| `__getattr__` |  |

### `__getattr__`
```python
def __getattr__(name) -> object:
```
