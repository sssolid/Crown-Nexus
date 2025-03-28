# Module: app.api.v1.endpoints.fitments

**Path:** `app/api/v1/endpoints/fitments.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination
from app.domains.products.models import Fitment, Product, product_fitment_association
from app.domains.products.schemas import Fitment as FitmentSchema, FitmentCreate, FitmentListResponse, FitmentUpdate, Product as ProductSchema
from app.domains.users.models import User
```

## Global Variables
```python
router = router = APIRouter()
```

## Functions

| Function | Description |
| --- | --- |
| `associate_product_with_fitment` |  |
| `create_fitment` |  |
| `delete_fitment` |  |
| `read_fitment` |  |
| `read_fitment_products` |  |
| `read_fitments` |  |
| `remove_product_from_fitment` |  |
| `update_fitment` |  |

### `associate_product_with_fitment`
```python
@router.post('/{fitment_id}/products/{product_id}')
async def associate_product_with_fitment(fitment_id, product_id, db, current_user) -> dict:
```

### `create_fitment`
```python
@router.post('/', response_model=FitmentSchema, status_code=status.HTTP_201_CREATED)
async def create_fitment(db, fitment_in, current_user) -> Any:
```

### `delete_fitment`
```python
@router.delete('/{fitment_id}')
async def delete_fitment(fitment_id, db, current_user) -> dict:
```

### `read_fitment`
```python
@router.get('/{fitment_id}', response_model=FitmentSchema)
async def read_fitment(fitment_id, db, current_user) -> Any:
```

### `read_fitment_products`
```python
@router.get('/{fitment_id}/products', response_model=List[ProductSchema])
async def read_fitment_products(fitment_id, db, current_user, skip, limit) -> Any:
```

### `read_fitments`
```python
@router.get('/', response_model=FitmentListResponse)
async def read_fitments(db, current_user, year, make, model, engine, transmission, page, page_size) -> Any:
```

### `remove_product_from_fitment`
```python
@router.delete('/{fitment_id}/products/{product_id}')
async def remove_product_from_fitment(fitment_id, product_id, db, current_user) -> dict:
```

### `update_fitment`
```python
@router.put('/{fitment_id}', response_model=FitmentSchema)
async def update_fitment(fitment_id, fitment_in, db, current_user) -> Any:
```
