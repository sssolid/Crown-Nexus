# Module: app.services.media.thumbnails

**Path:** `app/services/media/thumbnails.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
from pathlib import Path
from typing import Optional, Tuple
from app.core.logging import get_logger
from app.services.media.base import FileNotFoundError, MediaStorageError
```

## Global Variables
```python
logger = logger = get_logger(__name__)
```

## Classes

| Class | Description |
| --- | --- |
| `ThumbnailGenerator` |  |

### Class: `ThumbnailGenerator`

#### Methods

| Method | Description |
| --- | --- |
| `can_generate_thumbnail` |  |
| `generate_thumbnail` `async` |  |
| `get_supported_formats` |  |
| `get_thumbnail_path` |  |

##### `can_generate_thumbnail`
```python
@staticmethod
def can_generate_thumbnail(file_path) -> bool:
```

##### `generate_thumbnail`
```python
@staticmethod
async def generate_thumbnail(file_path, output_path, width, height, quality) -> None:
```

##### `get_supported_formats`
```python
@staticmethod
def get_supported_formats() -> Tuple[(str, Ellipsis)]:
```

##### `get_thumbnail_path`
```python
@staticmethod
def get_thumbnail_path(original_path, width, height, thumbnails_dir) -> str:
```
