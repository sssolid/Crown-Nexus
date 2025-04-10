# Module: app.api.v1.endpoints.autocare.padb

**Path:** `app/api/v1/endpoints/autocare/padb.py`

[Back to Project Index](../../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Annotated, Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db, get_pagination
from app.api.responses import paginated_response, success_response
from app.domains.autocare.padb.service import PAdbService
from app.domains.users.models import User
```

## Global Variables
```python
router = router = APIRouter()
```

## Functions

| Function | Description |
| --- | --- |
| `get_attribute_details` |  |
| `get_measurement_groups` |  |
| `get_padb_stats` |  |
| `get_part_attributes` |  |
| `get_uom_codes_by_measurement_group` |  |
| `get_valid_values_for_attribute` |  |
| `get_version` |  |
| `search_attributes` |  |

### `get_attribute_details`
```python
@router.get('/attributes/{pa_id}')
async def get_attribute_details(pa_id, db) -> Dict[(str, Any)]:
```

### `get_measurement_groups`
```python
@router.get('/measurement-groups')
async def get_measurement_groups(db) -> List[Dict[(str, Any)]]:
```

### `get_padb_stats`
```python
@router.get('/stats')
async def get_padb_stats(db) -> Dict[(str, Any)]:
```

### `get_part_attributes`
```python
@router.get('/parts/{part_terminology_id}/attributes')
async def get_part_attributes(part_terminology_id, db) -> Dict[(str, Any)]:
```

### `get_uom_codes_by_measurement_group`
```python
@router.get('/measurement-groups/{measurement_group_id}/uom-codes')
async def get_uom_codes_by_measurement_group(measurement_group_id, db) -> List[Dict[(str, Any)]]:
```

### `get_valid_values_for_attribute`
```python
@router.get('/attribute-assignments/{papt_id}/valid-values')
async def get_valid_values_for_attribute(papt_id, db) -> List[Dict[(str, Any)]]:
```

### `get_version`
```python
@router.get('/version')
async def get_version(db) -> str:
```

### `search_attributes`
```python
@router.get('/attributes/search')
async def search_attributes(db, search_term, part_terminology_id, page, page_size) -> Dict[(str, Any)]:
```
