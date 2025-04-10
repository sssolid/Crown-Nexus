# Module: app.api.v1.endpoints.autocare.qdb

**Path:** `app/api/v1/endpoints/autocare/qdb.py`

[Back to Project Index](../../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Annotated, Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db, get_pagination
from app.api.responses import paginated_response, success_response
from app.domains.autocare.qdb.service import QdbService
from app.domains.users.models import User
```

## Global Variables
```python
router = router = APIRouter()
```

## Functions

| Function | Description |
| --- | --- |
| `get_group_numbers` |  |
| `get_languages` |  |
| `get_qdb_stats` |  |
| `get_qualifier_details` |  |
| `get_qualifier_groups` |  |
| `get_qualifier_translations` |  |
| `get_qualifier_types` |  |
| `get_qualifiers_by_group` |  |
| `get_version` |  |
| `search_qualifiers` |  |

### `get_group_numbers`
```python
@router.get('/groups')
async def get_group_numbers(db) -> List[Dict[(str, Any)]]:
```

### `get_languages`
```python
@router.get('/languages')
async def get_languages(db) -> List[Dict[(str, Any)]]:
```

### `get_qdb_stats`
```python
@router.get('/stats')
async def get_qdb_stats(db) -> Dict[(str, Any)]:
```

### `get_qualifier_details`
```python
@router.get('/qualifiers/{qualifier_id}')
async def get_qualifier_details(qualifier_id, db) -> Dict[(str, Any)]:
```

### `get_qualifier_groups`
```python
@router.get('/qualifiers/{qualifier_id}/groups')
async def get_qualifier_groups(qualifier_id, db) -> List[Dict[(str, Any)]]:
```

### `get_qualifier_translations`
```python
@router.get('/qualifiers/{qualifier_id}/translations')
async def get_qualifier_translations(db, qualifier_id, language_id) -> List[Dict[(str, Any)]]:
```

### `get_qualifier_types`
```python
@router.get('/qualifier-types')
async def get_qualifier_types(db) -> List[Dict[(str, Any)]]:
```

### `get_qualifiers_by_group`
```python
@router.get('/groups/{group_number_id}/qualifiers')
async def get_qualifiers_by_group(db, group_number_id, page, page_size) -> Dict[(str, Any)]:
```

### `get_version`
```python
@router.get('/version')
async def get_version(db) -> str:
```

### `search_qualifiers`
```python
@router.get('/qualifiers/search')
async def search_qualifiers(db, search_term, qualifier_type_id, language_id, page, page_size) -> Dict[(str, Any)]:
```
