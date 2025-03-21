# Module: app.services.media.service

**Path:** `app/services/media/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from fastapi import HTTPException, UploadFile, status
from app.core.config import settings
from app.core.logging import get_logger
from app.models.media import MediaType, MediaVisibility
from app.services.interfaces import ServiceInterface
from app.services.media.base import FileNotFoundError, MediaStorageBackend, MediaStorageError, StorageBackendType
from app.services.media.factory import StorageBackendFactory
```

## Global Variables
```python
logger = logger = get_logger(__name__)
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
