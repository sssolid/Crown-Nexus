from __future__ import annotations

"""Product domain initialization.

This file serves as the public interface for the products domain.
It exports key functionality while hiding implementation details.
"""

# Re-export public interfaces
from app.domains.products.models import Product, Brand, ProductBrandHistory, ProductDescription, ProductMarketing, \
    ProductActivity, ProductSupersession, AttributeDefinition, ProductAttribute, PriceType, ProductPricing, \
    Manufacturer, ProductMeasurement, ProductStock, Fitment
from app.domains.products.schemas import (
    ProductCreate,
    ProductUpdate,
    Product as ProductSchema,
    Brand as BrandSchema,
)
from app.domains.products.service import ProductService
from app.domains.products.exceptions import (
    ProductNotFoundException,
    DuplicatePartNumberException,
    ProductInactiveException,
)

# Initialize domain event handlers
from app.domains.products import handlers

__all__ = [
    # Models
    "Product",
    "Brand",
    "ProductBrandHistory",
    "ProductDescription",
    "ProductMarketing",
    "ProductActivity",
    "ProductSupersession",
    "AttributeDefinition",
    "ProductAttribute",
    "PriceType",
    "ProductPricing",
    "Manufacturer",
    "ProductMeasurement",
    "ProductStock",
    "Fitment",
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
