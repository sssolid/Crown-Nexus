# Module: app.domains.media.repository

**Path:** `app/domains/media/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.media.models import Media, MediaType, MediaVisibility
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

## Classes

| Class | Description |
| --- | --- |
| `MediaRepository` |  |

### Class: `MediaRepository`
**Inherits from:** BaseRepository[(Media, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `approve` `async` |  |
| `ensure_exists` `async` |  |
| `find_by_filename` `async` |  |
| `find_by_media_type` `async` |  |
| `get_by_product` `async` |  |
| `get_by_visibility` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `approve`
```python
async def approve(self, media_id, approver_id) -> Optional[Media]:
```

##### `ensure_exists`
```python
async def ensure_exists(self, media_id) -> Media:
```

##### `find_by_filename`
```python
async def find_by_filename(self, filename) -> List[Media]:
```

##### `find_by_media_type`
```python
async def find_by_media_type(self, media_type) -> List[Media]:
```

##### `get_by_product`
```python
async def get_by_product(self, product_id, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_visibility`
```python
async def get_by_visibility(self, visibility, page, page_size) -> Dict[(str, Any)]:
```
