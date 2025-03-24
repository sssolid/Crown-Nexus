from __future__ import annotations

"""Product domain exceptions.

This module defines exceptions specific to the products domain.
"""

from app.core.exceptions import BusinessException, ResourceNotFoundException


class ProductNotFoundException(ResourceNotFoundException):
    """Raised when a product cannot be found."""

    def __init__(self, product_id: str) -> None:
        """Initialize the exception.

        Args:
            product_id: ID of the product that wasn't found
        """
        super().__init__(
            resource_type="Product",
            resource_id=product_id,
            message=f"Product with ID {product_id} not found",
        )


class DuplicatePartNumberException(BusinessException):
    """Raised when attempting to create a product with an existing part number."""

    def __init__(self, part_number: str) -> None:
        """Initialize the exception.

        Args:
            part_number: The duplicate part number
        """
        super().__init__(
            message="Product with this part number already exists",
            details={"part_number": part_number},
        )


class ProductInactiveException(BusinessException):
    """Raised when attempting operations on an inactive product."""

    def __init__(self, product_id: str) -> None:
        """Initialize the exception.

        Args:
            product_id: ID of the inactive product
        """
        super().__init__(
            message="Cannot perform operation on inactive product",
            details={"product_id": product_id},
        )


class BrandNotFoundException(ResourceNotFoundException):
    """Raised when a brand cannot be found."""

    def __init__(self, brand_id: str) -> None:
        """Initialize the exception.

        Args:
            brand_id: ID of the brand that wasn't found
        """
        super().__init__(
            resource_type="Brand",
            resource_id=brand_id,
            message=f"Brand with ID {brand_id} not found",
        )


class DuplicateBrandNameException(BusinessException):
    """Raised when attempting to create a brand with an existing name."""

    def __init__(self, name: str) -> None:
        """Initialize the exception.

        Args:
            name: The duplicate brand name
        """
        super().__init__(
            message="Brand with this name already exists", details={"name": name}
        )
