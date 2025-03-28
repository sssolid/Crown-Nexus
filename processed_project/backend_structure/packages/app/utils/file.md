# Module: app.utils.file

**Path:** `app/utils/file.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import os
import secrets
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Protocol, Set, Tuple, Union
from PIL import Image, UnidentifiedImageError
from fastapi import HTTPException, UploadFile, status
from app.core.config import settings
from app.core.exceptions import ErrorCode, SecurityException, ValidationException
from app.logging import get_logger
from app.domains.media.models import MediaType
```

## Global Variables
```python
logger = logger = get_logger("app.utils.file")
MediaConstraints = MediaConstraints = Dict[MediaType, Set[str]]
SizeConstraints = SizeConstraints = Dict[MediaType, int]
DimensionsTuple = DimensionsTuple = Tuple[int, int]
```

## Functions

| Function | Description |
| --- | --- |
| `get_file_extension` |  |
| `get_file_path` |  |
| `get_file_url` |  |
| `get_media_type_from_mime` |  |
| `get_thumbnail_path` |  |
| `is_safe_filename` |  |
| `sanitize_filename` |  |
| `save_upload_file` |  |
| `validate_file` |  |

### `get_file_extension`
```python
def get_file_extension(filename) -> str:
```

### `get_file_path`
```python
def get_file_path(file_path) -> Path:
```

### `get_file_url`
```python
def get_file_url(file_path) -> str:
```

### `get_media_type_from_mime`
```python
def get_media_type_from_mime(mime_type) -> MediaType:
```

### `get_thumbnail_path`
```python
def get_thumbnail_path(file_path) -> Optional[Path]:
```

### `is_safe_filename`
```python
def is_safe_filename(filename) -> bool:
```

### `sanitize_filename`
```python
def sanitize_filename(filename) -> str:
```

### `save_upload_file`
```python
def save_upload_file(file, media_id, media_type, is_image) -> Tuple[(str, int, str)]:
```

### `validate_file`
```python
def validate_file(file, allowed_types) -> Tuple[(MediaType, bool)]:
```

## Classes

| Class | Description |
| --- | --- |
| `FileSecurityError` |  |
| `FileValidationError` |  |
| `ImageProcessor` |  |

### Class: `FileSecurityError`
**Inherits from:** SecurityException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details) -> None:
```

### Class: `FileValidationError`
**Inherits from:** ValidationException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, code, details) -> None:
```

### Class: `ImageProcessor`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `open` |  |

##### `open`
```python
def open(self, path) -> 'Image.Image':
```
