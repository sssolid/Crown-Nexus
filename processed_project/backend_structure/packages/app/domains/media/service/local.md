# Module: app.domains.media.service.local

**Path:** `app/domains/media/service/local.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO, Dict, Optional, Set, Tuple, Union
import aiofiles
from app.domains.media.service.base import FileNotFoundError, MediaStorageError
from app.domains.media.service.thumbnails import ThumbnailGenerator
from fastapi import UploadFile
from app.core.config import settings
from app.logging import get_logger
from app.domains.media.models import MediaType
```

## Global Variables
```python
logger = logger = get_logger("app.domains.media.service.local")
```

## Classes

| Class | Description |
| --- | --- |
| `LocalMediaStorage` |  |

### Class: `LocalMediaStorage`
**Decorators:**
- `@dataclass`

#### Methods

| Method | Description |
| --- | --- |
| `__post_init__` |  |
| `delete_file` `async` |  |
| `file_exists` `async` |  |
| `generate_thumbnail` `async` |  |
| `get_file_url` `async` |  |
| `initialize` `async` |  |
| `save_file` `async` |  |

##### `__post_init__`
```python
def __post_init__(self) -> None:
```

##### `delete_file`
```python
async def delete_file(self, file_path) -> bool:
```

##### `file_exists`
```python
async def file_exists(self, file_path) -> bool:
```

##### `generate_thumbnail`
```python
async def generate_thumbnail(self, file_path, width, height) -> Optional[str]:
```

##### `get_file_url`
```python
async def get_file_url(self, file_path) -> str:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `save_file`
```python
async def save_file(self, file, destination, media_type, content_type) -> str:
```
