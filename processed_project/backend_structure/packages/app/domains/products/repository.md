# Module: app.domains.products.repository

**Path:** `app/domains/products/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.products.models import Product, Brand, Fitment, ProductActivity, ProductSupersession
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, BusinessException
```

## Classes

| Class | Description |
| --- | --- |
| `BrandRepository` |  |
| `FitmentRepository` |  |
| `ProductRepository` |  |

### Class: `BrandRepository`
**Inherits from:** BaseRepository[(Brand, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_name` `async` |  |
| `find_by_name_partial` `async` |  |
| `get_by_company` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, brand_id) -> Brand:
```

##### `find_by_name`
```python
async def find_by_name(self, name) -> Optional[Brand]:
```

##### `find_by_name_partial`
```python
async def find_by_name_partial(self, name) -> List[Brand]:
```

##### `get_by_company`
```python
async def get_by_company(self, company_id) -> List[Brand]:
```

### Class: `FitmentRepository`
**Inherits from:** BaseRepository[(Fitment, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_vehicle` `async` |  |
| `get_makes_by_year` `async` |  |
| `get_models_by_year_make` `async` |  |
| `get_years_range` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, fitment_id) -> Fitment:
```

##### `find_by_vehicle`
```python
async def find_by_vehicle(self, year, make, model, engine, transmission) -> List[Fitment]:
```

##### `get_makes_by_year`
```python
async def get_makes_by_year(self, year) -> List[str]:
```

##### `get_models_by_year_make`
```python
async def get_models_by_year_make(self, year, make) -> List[str]:
```

##### `get_years_range`
```python
async def get_years_range(self) -> Tuple[(int, int)]:
```

### Class: `ProductRepository`
**Inherits from:** BaseRepository[(Product, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `create_supersession` `async` |  |
| `ensure_exists` `async` |  |
| `find_by_part_number` `async` |  |
| `find_by_part_number_stripped` `async` |  |
| `get_active_products` `async` |  |
| `get_by_fitment` `async` |  |
| `search` `async` |  |
| `update_status` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `create_supersession`
```python
async def create_supersession(self, old_product_id, new_product_id, reason) -> ProductSupersession:
```

##### `ensure_exists`
```python
async def ensure_exists(self, product_id) -> Product:
```

##### `find_by_part_number`
```python
async def find_by_part_number(self, part_number) -> Optional[Product]:
```

##### `find_by_part_number_stripped`
```python
async def find_by_part_number_stripped(self, part_number) -> List[Product]:
```

##### `get_active_products`
```python
async def get_active_products(self, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_fitment`
```python
async def get_by_fitment(self, year, make, model, engine, transmission, page, page_size) -> Dict[(str, Any)]:
```

##### `search`
```python
async def search(self, search_term, page, page_size) -> Dict[(str, Any)]:
```

##### `update_status`
```python
async def update_status(self, product_id, status, reason, user_id) -> Tuple[(Product, ProductActivity)]:
```
