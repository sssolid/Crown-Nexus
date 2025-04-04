# Module: app.data_import.pipeline.base

**Path:** `app/data_import/pipeline/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Protocol, TypeVar, Union
from app.data_import.connectors.base import Connector
from app.data_import.connectors.file_connector import FileConnector
from app.data_import.connectors.filemaker_connector import FileMakerConnector
from app.data_import.importers.base import Importer
from app.data_import.processors.base import Processor
```

## Global Variables
```python
T = T = TypeVar("T")
```

## Classes

| Class | Description |
| --- | --- |
| `Pipeline` |  |

### Class: `Pipeline`
**Inherits from:** Protocol[T]

#### Methods

| Method | Description |
| --- | --- |
| `run` `async` |  |

##### `run`
```python
async def run(self, query, **params) -> Dict[(str, Any)]:
```
