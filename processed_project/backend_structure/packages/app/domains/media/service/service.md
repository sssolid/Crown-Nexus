# Module: app.domains.media.service.service

**Path:** `app/domains/media/service/service.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from app.domains.media.service.base import FileNotFoundError, MediaStorageBackend, MediaStorageError, StorageBackendType
from app.domains.media.service.factory import StorageBackendFactory
from fastapi import HTTPException, UploadFile, status
from app.core.config import settings
from app.logging import get_logger
from app.domains.media.models import MediaType, MediaVisibility
from app.services.interfaces import ServiceInterface
```

## Global Variables
```python
logger = logger = get_logger("app.domains.media.service.service")
```

## Classes

| Class | Description |
| --- | --- |
| `MediaService` |  |

### Class: `MediaService`
**Inherits from:** ServiceInterface

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `delete_file` `async` |  |
| `ensure_initialized` `async` |  |
| `initialize` `async` |  |
| `shutdown` `async` |  |
| `upload_file` `async` |  |

##### `__init__`
```python
def __init__(self, storage_type):
```

##### `delete_file`
```python
async def delete_file(self, file_url) -> bool:
```

##### `ensure_initialized`
```python
async def ensure_initialized(self) -> None:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

##### `upload_file`
```python
async def upload_file(self, file, media_type, product_id, filename, visibility, generate_thumbnail) -> Tuple[(str, Dict[(str, Any)], Optional[str])]:
```
