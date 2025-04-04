# Module: app.domains.media.service.base

**Path:** `app/domains/media/service/base.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from enum import Enum
from typing import BinaryIO, Optional, Protocol, TypedDict, Union
from fastapi import UploadFile
```

## Classes

| Class | Description |
| --- | --- |
| `FileMetadata` |  |
| `FileNotFoundError` |  |
| `MediaStorageBackend` |  |
| `MediaStorageError` |  |
| `StorageBackendType` |  |
| `StorageConnectionError` |  |

### Class: `FileMetadata`
**Inherits from:** TypedDict

### Class: `FileNotFoundError`
**Inherits from:** MediaStorageError

### Class: `MediaStorageBackend`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `delete_file` `async` |  |
| `file_exists` `async` |  |
| `generate_thumbnail` `async` |  |
| `get_file_url` `async` |  |
| `initialize` `async` |  |
| `save_file` `async` |  |

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

### Class: `MediaStorageError`
**Inherits from:** Exception

### Class: `StorageBackendType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `LOCAL` | `'local'` |
| `S3` | `'s3'` |
| `AZURE` | `'azure'` |

### Class: `StorageConnectionError`
**Inherits from:** MediaStorageError
