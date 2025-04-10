# Module: app.domains.media.service.factory

**Path:** `app/domains/media/service/factory.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Optional
from app.domains.media.service.base import MediaStorageBackend, StorageBackendType
from app.domains.media.service.local import LocalMediaStorage
from app.domains.media.service.s3 import S3MediaStorage
from app.core.config import settings
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.domains.media.service.factory")
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
