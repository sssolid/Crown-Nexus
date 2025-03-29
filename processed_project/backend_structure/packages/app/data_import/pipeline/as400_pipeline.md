# Module: app.data_import.pipeline.as400_pipeline

**Path:** `app/data_import/pipeline/as400_pipeline.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import time
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel
from app.core.exceptions import AppException
from app.logging import get_logger
from app.data_import.connectors.as400_connector import AS400Connector
from app.data_import.importers.base import Importer
from app.data_import.processors.as400_processor import AS400BaseProcessor
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.pipeline.as400_pipeline")
T = T = TypeVar("T", bound=BaseModel)
```

## Classes

| Class | Description |
| --- | --- |
| `AS400Pipeline` |  |
| `ParallelAS400Pipeline` |  |

### Class: `AS400Pipeline`
**Inherits from:** Generic[T]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `run` `async` |  |

##### `__init__`
```python
def __init__(self, connector, processor, importer, dry_run, chunk_size) -> None:
```

##### `run`
```python
async def run(self, query, limit, **params) -> Dict[(str, Any)]:
```

### Class: `ParallelAS400Pipeline`
**Inherits from:** Generic[T]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `run` `async` |  |

##### `__init__`
```python
def __init__(self, pipelines, max_workers) -> None:
```

##### `run`
```python
async def run(self) -> Dict[(str, Any)]:
```
