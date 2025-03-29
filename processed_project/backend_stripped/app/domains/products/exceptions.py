from __future__ import annotations
'Product domain exceptions.\n\nThis module defines exceptions specific to the products domain.\n'
from app.core.exceptions import BusinessException, ResourceNotFoundException
class ProductNotFoundException(ResourceNotFoundException):
    def __init__(self, product_id: str) -> None:
        super().__init__(resource_type='Product', resource_id=product_id, message=f'Product with ID {product_id} not found')
class DuplicatePartNumberException(BusinessException):
    def __init__(self, part_number: str) -> None:
        super().__init__(message='Product with this part number already exists', details={'part_number': part_number})
class ProductInactiveException(BusinessException):
    def __init__(self, product_id: str) -> None:
        super().__init__(message='Cannot perform operation on inactive product', details={'product_id': product_id})
class BrandNotFoundException(ResourceNotFoundException):
    def __init__(self, brand_id: str) -> None:
        super().__init__(resource_type='Brand', resource_id=brand_id, message=f'Brand with ID {brand_id} not found')
class DuplicateBrandNameException(BusinessException):
    def __init__(self, name: str) -> None:
        super().__init__(message='Brand with this name already exists', details={'name': name})