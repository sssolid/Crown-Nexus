from __future__ import annotations
'Product domain initialization.\n\nThis file serves as the public interface for the products domain.\nIt exports key functionality while hiding implementation details.\n'
from app.domains.products.models import Product, Brand, ProductBrandHistory, ProductDescription, ProductMarketing, ProductActivity, ProductSupersession, AttributeDefinition, ProductAttribute, PriceType, ProductPricing, Manufacturer, ProductMeasurement, ProductStock, Fitment
from app.domains.products.schemas import ProductCreate, ProductUpdate, Product as ProductSchema, Brand as BrandSchema
from app.domains.products.service import ProductService
from app.domains.products.exceptions import ProductNotFoundException, DuplicatePartNumberException, ProductInactiveException
from app.domains.products import handlers
__all__ = ['Product', 'Brand', 'ProductBrandHistory', 'ProductDescription', 'ProductMarketing', 'ProductActivity', 'ProductSupersession', 'AttributeDefinition', 'ProductAttribute', 'PriceType', 'ProductPricing', 'Manufacturer', 'ProductMeasurement', 'ProductStock', 'Fitment', 'ProductCreate', 'ProductUpdate', 'ProductSchema', 'BrandSchema', 'ProductService', 'ProductNotFoundException', 'DuplicatePartNumberException', 'ProductInactiveException']