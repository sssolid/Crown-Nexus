# Module: app.data_import.connectors

**Path:** `app/data_import/connectors/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.data_import.connectors.base import Connector
from app.data_import.connectors.file_connector import FileConnector, FileConnectionConfig
from app.data_import.connectors.filemaker_connector import FileMakerConnector, FileMakerConnectionConfig
from app.data_import.connectors.as400_connector import AS400Connector, AS400ConnectionConfig
```

## Global Variables
```python
__all__ = __all__ = [
    "Connector",
    "FileConnector",
    "FileConnectionConfig",
    "FileMakerConnector",
    "FileMakerConnectionConfig",
    "AS400Connector",
    "AS400ConnectionConfig",
]
```
