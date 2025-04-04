# Module: tests.api.v1.test_products

**Path:** `tests/api/v1/test_products.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.products.models import Product
from app.domains.users.models import User
from tests.utils import make_authenticated_request, create_random_string
```

## Functions

| Function | Description |
| --- | --- |
| `test_create_product_admin` |  |
| `test_create_product_duplicate_sku` |  |
| `test_create_product_non_admin` |  |
| `test_delete_product_admin` |  |
| `test_delete_product_non_admin` |  |
| `test_read_product` |  |
| `test_read_product_not_found` |  |
| `test_read_products` |  |
| `test_read_products_with_filters` |  |
| `test_update_product_admin` |  |
| `test_update_product_non_admin` |  |

### `test_create_product_admin`
```python
@pytest.mark.asyncio
async def test_create_product_admin(client, admin_token) -> None:
```

### `test_create_product_duplicate_sku`
```python
@pytest.mark.asyncio
async def test_create_product_duplicate_sku(client, admin_token, test_product) -> None:
```

### `test_create_product_non_admin`
```python
@pytest.mark.asyncio
async def test_create_product_non_admin(client, user_token) -> None:
```

### `test_delete_product_admin`
```python
@pytest.mark.asyncio
async def test_delete_product_admin(client, admin_token, db) -> None:
```

### `test_delete_product_non_admin`
```python
@pytest.mark.asyncio
async def test_delete_product_non_admin(client, user_token, test_product) -> None:
```

### `test_read_product`
```python
@pytest.mark.asyncio
async def test_read_product(client, user_token, test_product) -> None:
```

### `test_read_product_not_found`
```python
@pytest.mark.asyncio
async def test_read_product_not_found(client, user_token) -> None:
```

### `test_read_products`
```python
@pytest.mark.asyncio
async def test_read_products(client, normal_user, user_token, test_product) -> None:
```

### `test_read_products_with_filters`
```python
@pytest.mark.asyncio
async def test_read_products_with_filters(client, admin_token, test_product) -> None:
```

### `test_update_product_admin`
```python
@pytest.mark.asyncio
async def test_update_product_admin(client, admin_token, test_product) -> None:
```

### `test_update_product_non_admin`
```python
@pytest.mark.asyncio
async def test_update_product_non_admin(client, user_token, test_product) -> None:
```
