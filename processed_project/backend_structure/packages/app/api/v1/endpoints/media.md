# Module: app.api.v1.endpoints.media

**Path:** `app/api/v1/endpoints/media.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import json
import os
from datetime import datetime
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination, get_optional_user
from app.domains.media.models import Media, MediaType, MediaVisibility
from app.domains.media.schemas import FileUploadResponse, Media as MediaSchema, MediaListResponse, MediaUpdate
from app.domains.products.models import Product, product_media_association
from app.domains.users.models import User
from app.utils.file import get_file_path, get_thumbnail_path, save_upload_file, validate_file
```

## Global Variables
```python
router = router = APIRouter()
```

## Functions

| Function | Description |
| --- | --- |
| `associate_media_with_product` |  |
| `delete_media` |  |
| `get_media_file` |  |
| `get_media_thumbnail` |  |
| `get_product_media` |  |
| `read_media` |  |
| `read_media_item` |  |
| `remove_media_from_product` |  |
| `update_media` |  |
| `upload_file` |  |

### `associate_media_with_product`
```python
@router.post('/{media_id}/products/{product_id}')
async def associate_media_with_product(media_id, product_id, db, current_user) -> dict:
```

### `delete_media`
```python
@router.delete('/{media_id}')
async def delete_media(media_id, db, current_user) -> dict:
```

### `get_media_file`
```python
@router.get('/file/{media_id}')
async def get_media_file(media_id, db, current_user) -> Any:
```

### `get_media_thumbnail`
```python
@router.get('/thumbnail/{media_id}')
async def get_media_thumbnail(media_id, db, current_user) -> Any:
```

### `get_product_media`
```python
@router.get('/products/{product_id}', response_model=List[MediaSchema])
async def get_product_media(product_id, db, current_user, media_type) -> Any:
```

### `read_media`
```python
@router.get('/', response_model=MediaListResponse)
async def read_media(db, current_user, media_type, visibility, is_approved, product_id, page, page_size) -> Any:
```

### `read_media_item`
```python
@router.get('/{media_id}', response_model=MediaSchema)
async def read_media_item(media_id, db, current_user) -> Any:
```

### `remove_media_from_product`
```python
@router.delete('/{media_id}/products/{product_id}')
async def remove_media_from_product(media_id, product_id, db, current_user) -> dict:
```

### `update_media`
```python
@router.put('/{media_id}', response_model=MediaSchema)
async def update_media(media_id, media_in, db, current_user) -> Any:
```

### `upload_file`
```python
@router.post('/upload', response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(background_tasks, db, current_user, file, media_type, visibility, metadata, product_id) -> Any:
```
