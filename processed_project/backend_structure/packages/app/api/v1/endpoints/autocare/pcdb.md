# Module: app.api.v1.endpoints.autocare.pcdb

**Path:** `app/api/v1/endpoints/autocare/pcdb.py`

[Back to Project Index](../../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Annotated, Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db, get_pagination
from app.api.responses import paginated_response, success_response
from app.domains.autocare.pcdb.service import PCdbService
from app.domains.users.models import User
```

## Global Variables
```python
router = router = APIRouter()
```

## Functions

| Function | Description |
| --- | --- |
| `get_categories` |  |
| `get_part_details` |  |
| `get_part_positions` |  |
| `get_part_supersessions` |  |
| `get_parts_by_category` |  |
| `get_pcdb_stats` |  |
| `get_positions` |  |
| `get_subcategories_by_category` |  |
| `get_version` |  |
| `search_categories` |  |
| `search_parts` |  |

### `get_categories`
```python
@router.get('/categories')
async def get_categories(db) -> List[Dict[(str, Any)]]:
```

### `get_part_details`
```python
@router.get('/parts/{part_terminology_id}')
async def get_part_details(part_terminology_id, db) -> Dict[(str, Any)]:
```

### `get_part_positions`
```python
@router.get('/parts/{part_terminology_id}/positions')
async def get_part_positions(part_terminology_id, db) -> List[Dict[(str, Any)]]:
```

### `get_part_supersessions`
```python
@router.get('/parts/{part_terminology_id}/supersessions')
async def get_part_supersessions(part_terminology_id, db) -> Dict[(str, List[Dict[(str, Any)]])]:
```

### `get_parts_by_category`
```python
@router.get('/categories/{category_id}/parts')
async def get_parts_by_category(db, category_id, page, page_size) -> Dict[(str, Any)]:
```

### `get_pcdb_stats`
```python
@router.get('/stats')
async def get_pcdb_stats(db) -> Dict[(str, Any)]:
```

### `get_positions`
```python
@router.get('/positions')
async def get_positions(db) -> List[Dict[(str, Any)]]:
```

### `get_subcategories_by_category`
```python
@router.get('/categories/{category_id}/subcategories')
async def get_subcategories_by_category(category_id, db) -> List[Dict[(str, Any)]]:
```

### `get_version`
```python
@router.get('/version')
async def get_version(db) -> str:
```

### `search_categories`
```python
@router.get('/categories/search')
async def search_categories(db, search_term) -> List[Dict[(str, Any)]]:
```

### `search_parts`
```python
@router.get('/parts/search')
async def search_parts(db, search_term, category_id, subcategory_id, position_id, page, page_size) -> Dict[(str, Any)]:
```
