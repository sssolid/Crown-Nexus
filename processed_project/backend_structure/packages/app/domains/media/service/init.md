# Module: app.domains.media.service

**Path:** `app/domains/media/service/__init__.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from typing import Optional
from app.domains.media.service.service import MediaService
```

## Functions

| Function | Description |
| --- | --- |
| `get_media_service` |  |
| `get_media_service_factory` |  |

### `get_media_service`
```python
async def get_media_service(storage_type) -> MediaService:
```

### `get_media_service_factory`
```python
def get_media_service_factory(storage_type) -> MediaService:
```
