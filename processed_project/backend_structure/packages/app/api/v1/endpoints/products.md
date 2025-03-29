# Module: app.api.v1.endpoints.products

**Path:** `app/api/v1/endpoints/products.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination
from app.domains.products.models import Brand, Product, ProductActivity, ProductBrandHistory, ProductDescription, ProductMarketing, ProductMeasurement, ProductStock, ProductSupersession
from app.domains.products.schemas import Brand as BrandSchema, BrandCreate, BrandUpdate, Product as ProductSchema, ProductCreate, ProductDescription as ProductDescriptionSchema, ProductDescriptionCreate, ProductDescriptionUpdate, ProductListResponse, ProductMarketing as ProductMarketingSchema, ProductMarketingCreate, ProductMarketingUpdate, ProductMeasurement as ProductMeasurementSchema, ProductMeasurementCreate, ProductStatus, ProductStock as ProductStockSchema, ProductStockCreate, ProductStockUpdate, ProductSupersession as ProductSupersessionSchema, ProductSupersessionCreate, ProductUpdate
from app.domains.reference.models import Warehouse
from app.domains.users.models import User
```

## Global Variables
```python
router = router = APIRouter()
```

## Functions

| Function | Description |
| --- | --- |
| `create_brand` |  |
| `create_product` |  |
| `create_product_description` |  |
| `create_product_marketing` |  |
| `create_product_measurement` |  |
| `create_product_stock` |  |
| `create_product_supersession` |  |
| `delete_brand` |  |
| `delete_product` |  |
| `delete_product_description` |  |
| `delete_product_marketing` |  |
| `delete_product_stock` |  |
| `delete_product_supersession` |  |
| `read_brand` |  |
| `read_brands` |  |
| `read_product` |  |
| `read_products` |  |
| `update_brand` |  |
| `update_product` |  |
| `update_product_description` |  |
| `update_product_marketing` |  |
| `update_product_stock` |  |

### `create_brand`
```python
@router.post('/brands/', response_model=BrandSchema, status_code=status.HTTP_201_CREATED)
async def create_brand(db, brand_in, current_user) -> Any:
```

### `create_product`
```python
@router.post('/', response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(db, product_in, current_user) -> Any:
```

### `create_product_description`
```python
@router.post('/{product_id}/descriptions', response_model=ProductDescriptionSchema)
async def create_product_description(product_id, description_in, db, current_user) -> Any:
```

### `create_product_marketing`
```python
@router.post('/{product_id}/marketing', response_model=ProductMarketingSchema)
async def create_product_marketing(product_id, marketing_in, db, current_user) -> Any:
```

### `create_product_measurement`
```python
@router.post('/{product_id}/measurements', response_model=ProductMeasurementSchema)
async def create_product_measurement(product_id, measurement_in, db, current_user) -> Any:
```

### `create_product_stock`
```python
@router.post('/{product_id}/stock', response_model=ProductStockSchema)
async def create_product_stock(product_id, stock_in, db, current_user) -> Any:
```

### `create_product_supersession`
```python
@router.post('/{product_id}/supersessions', response_model=ProductSupersessionSchema)
async def create_product_supersession(product_id, supersession_in, db, current_user) -> Any:
```

### `delete_brand`
```python
@router.delete('/brands/{brand_id}')
async def delete_brand(brand_id, db, current_user) -> dict:
```

### `delete_product`
```python
@router.delete('/{product_id}')
async def delete_product(product_id, db, current_user) -> dict:
```

### `delete_product_description`
```python
@router.delete('/{product_id}/descriptions/{description_id}')
async def delete_product_description(product_id, description_id, db, current_user) -> dict:
```

### `delete_product_marketing`
```python
@router.delete('/{product_id}/marketing/{marketing_id}')
async def delete_product_marketing(product_id, marketing_id, db, current_user) -> dict:
```

### `delete_product_stock`
```python
@router.delete('/{product_id}/stock/{stock_id}')
async def delete_product_stock(product_id, stock_id, db, current_user) -> dict:
```

### `delete_product_supersession`
```python
@router.delete('/{product_id}/supersessions/{supersession_id}')
async def delete_product_supersession(product_id, supersession_id, db, current_user) -> dict:
```

### `read_brand`
```python
@router.get('/brands/{brand_id}', response_model=BrandSchema)
async def read_brand(brand_id, db, current_user) -> Any:
```

### `read_brands`
```python
@router.get('/brands/', response_model=List[BrandSchema])
async def read_brands(db, current_user, skip, limit) -> Any:
```

### `read_product`
```python
@router.get('/{product_id}', response_model=ProductSchema)
async def read_product(product_id, db, current_user) -> Any:
```

### `read_products`
```python
@router.get('/', response_model=ProductListResponse)
async def read_products(db, current_user, search, vintage, late_model, soft, universal, is_active, skip, limit, page, page_size) -> Any:
```

### `update_brand`
```python
@router.put('/brands/{brand_id}', response_model=BrandSchema)
async def update_brand(brand_id, brand_in, db, current_user) -> Any:
```

### `update_product`
```python
@router.put('/{product_id}', response_model=ProductSchema)
async def update_product(product_id, product_in, db, current_user) -> Any:
```

### `update_product_description`
```python
@router.put('/{product_id}/descriptions/{description_id}', response_model=ProductDescriptionSchema)
async def update_product_description(product_id, description_id, description_in, db, current_user) -> Any:
```

### `update_product_marketing`
```python
@router.put('/{product_id}/marketing/{marketing_id}', response_model=ProductMarketingSchema)
async def update_product_marketing(product_id, marketing_id, marketing_in, db, current_user) -> Any:
```

### `update_product_stock`
```python
@router.put('/{product_id}/stock/{stock_id}', response_model=ProductStockSchema)
async def update_product_stock(product_id, stock_id, stock_in, db, current_user) -> Any:
```
