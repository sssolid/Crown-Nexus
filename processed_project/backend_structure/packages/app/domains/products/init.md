# Module: app.domains.products

**Path:** `app/domains/products/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.domains.products.models import Product, Brand, ProductDescription
from app.domains.products.schemas import ProductCreate, ProductUpdate, Product as ProductSchema, Brand as BrandSchema
from app.domains.products.service import ProductService
from app.domains.products.exceptions import ProductNotFoundException, DuplicatePartNumberException, ProductInactiveException
from app.domains.products import handlers
```

## Global Variables
```python
__all__ = __all__ = [
    # Models
    "Product",
    "Brand",
    "ProductDescription",
    # Schemas
    "ProductCreate",
    "ProductUpdate",
    "ProductSchema",
    "BrandSchema",
    # Services
    "ProductService",
    # Exceptions
    "ProductNotFoundException",
    "DuplicatePartNumberException",
    "ProductInactiveException",
]
```
