# Module: app.data_import.pipeline.product_pipeline

**Path:** `app/data_import/pipeline/product_pipeline.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import time
from typing import Any, Dict, Optional, Union
from app.core.exceptions import AppException
from app.logging import get_logger
from app.data_import.connectors.base import Connector
from app.data_import.connectors.file_connector import FileConnector
from app.data_import.connectors.filemaker_connector import FileMakerConnector
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.processors.product_processor import ProductProcessor
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.pipeline.product_pipeline")
```

## Classes

| Class | Description |
| --- | --- |
| `ProductPipeline` |  |

### Class: `ProductPipeline`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `run` `async` |  |

##### `__init__`
```python
def __init__(self, connector, processor, importer, dry_run) -> None:
```

##### `run`
```python
async def run(self, query, limit, **params) -> Dict[(str, Any)]:
```
