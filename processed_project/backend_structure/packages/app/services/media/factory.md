# Module: app.services.media.factory

**Path:** `app/services/media/factory.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Optional, Type
from app.core.config import settings
from app.core.logging import get_logger
from app.services.media.base import MediaStorageBackend, StorageBackendType
from app.services.media.local import LocalMediaStorage
from app.services.media.s3 import S3MediaStorage
```

## Global Variables
```python
logger = logger = get_logger(__name__)
```

## Classes

| Class | Description |
| --- | --- |
| `StorageBackendFactory` |  |

### Class: `StorageBackendFactory`

#### Methods

| Method | Description |
| --- | --- |
| `get_backend` |  |

##### `get_backend`
```python
@staticmethod
def get_backend(backend_type) -> MediaStorageBackend:
```
