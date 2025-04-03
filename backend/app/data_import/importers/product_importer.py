# app/data_import/importers/product_importer.py
from __future__ import annotations

"""
Product data importer.

This module provides a product data importer that inserts or updates
product data in the application database.
"""

from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DatabaseException
from app.logging import get_logger
from app.domains.products.models import Product, ProductDescription, ProductMarketing
from app.domains.products.schemas import ProductCreate

logger = get_logger("app.data_import.importers.product_importer")


class ProductImporter:
    """Importer for product data."""

    def __init__(self, db: AsyncSession) -> None:
        """
        Initialize the product importer.

        Args:
            db: Database session
        """
        self.db = db
        logger.debug("ProductImporter initialized")

    async def _get_existing_products(
        self, part_numbers: List[str]
    ) -> Dict[str, Product]:
        """
        Get existing products by part numbers.

        Args:
            part_numbers: List of part numbers to look up

        Returns:
            Dictionary mapping part numbers to existing products

        Raises:
            DatabaseException: If database query fails
        """
        if not part_numbers:
            return {}

        try:
            query = select(Product).where(Product.part_number.in_(part_numbers))
            result = await self.db.execute(query)
            existing_products = {p.part_number: p for p in result.scalars().all()}
            logger.debug(
                f"Found {len(existing_products)} existing products out of {len(part_numbers)} requested"
            )
            return existing_products
        except Exception as e:
            logger.error(f"Error fetching existing products: {str(e)}")
            raise DatabaseException(
                message=f"Failed to fetch existing products: {str(e)}",
                original_exception=e,
            ) from e

    async def _create_or_update_product(self, product_data: ProductCreate,
                                        existing_product: Optional[Product] = None) -> Tuple[Product, bool]:
        """Create or update a product and its related data.

        This method handles both the base product fields and complex fields like
        descriptions and marketing.

        Args:
            product_data: The product data to create or update
            existing_product: The existing product to update, or None to create new

        Returns:
            Tuple of (updated product, whether product is new)

        Raises:
            DatabaseException: If there's an error creating or updating the product
        """
        try:
            is_new = existing_product is None

            if is_new:
                # Create new product
                product = Product(
                    part_number=product_data.part_number,
                    part_number_stripped=product_data.part_number_stripped,
                    application=product_data.application,
                    vintage=product_data.vintage,
                    late_model=product_data.late_model,
                    soft=product_data.soft,
                    universal=product_data.universal,
                    is_active=product_data.is_active
                )
                self.db.add(product)
                await self.db.flush()
                logger.debug(f'Created new product: {product_data.part_number}')
            else:
                # Update existing product
                product = existing_product
                product.application = product_data.application
                product.vintage = product_data.vintage
                product.late_model = product_data.late_model
                product.soft = product_data.soft
                product.universal = product_data.universal
                product.is_active = product_data.is_active
                self.db.add(product)
                await self.db.flush()
                logger.debug(f'Updated existing product: {product_data.part_number}')

            # Add debugging for descriptions
            if hasattr(product_data, 'descriptions') and product_data.descriptions:
                logger.debug(f"Processing {len(product_data.descriptions)} descriptions for {product_data.part_number}")

                # Delete existing descriptions if updating
                if not is_new:
                    from app.domains.products.models import ProductDescription
                    await self.db.execute(delete(ProductDescription).where(ProductDescription.product_id == product.id))
                    logger.debug(f"Deleted existing descriptions for {product_data.part_number}")

                # Add new descriptions
                for desc in product_data.descriptions:
                    from app.domains.products.models import ProductDescription
                    description = ProductDescription(
                        product_id=product.id,
                        description_type=desc.description_type,
                        description=desc.description
                    )
                    self.db.add(description)
                    logger.debug(
                        f"Added {desc.description_type} description for {product_data.part_number}: {desc.description[:30]}...")
            else:
                logger.debug(f"No descriptions for {product_data.part_number}")

            # Add debugging for marketing
            if hasattr(product_data, 'marketing') and product_data.marketing:
                logger.debug(f"Processing {len(product_data.marketing)} marketing items for {product_data.part_number}")

                # Delete existing marketing if updating
                if not is_new:
                    from app.domains.products.models import ProductMarketing
                    await self.db.execute(delete(ProductMarketing).where(ProductMarketing.product_id == product.id))
                    logger.debug(f"Deleted existing marketing for {product_data.part_number}")

                # Add new marketing
                for mkt in product_data.marketing:
                    from app.domains.products.models import ProductMarketing
                    marketing = ProductMarketing(
                        product_id=product.id,
                        marketing_type=mkt.marketing_type,
                        content=mkt.content,
                        position=mkt.position
                    )
                    self.db.add(marketing)
                    logger.debug(
                        f"Added {mkt.marketing_type} marketing for {product_data.part_number}: {mkt.content[:30]}...")
            else:
                logger.debug(f"No marketing for {product_data.part_number}")

            await self.db.flush()
            return (product, is_new)
        except Exception as e:
            logger.error(f'Error creating/updating product {product_data.part_number}: {str(e)}')
            raise DatabaseException(message=f'Failed to create/update product: {str(e)}', original_exception=e) from e

    async def import_data(self, data: List[ProductCreate]) -> Dict[str, Any]:
        """
        Import product data into the database.

        Args:
            data: List of validated product data to import

        Returns:
            Dictionary with import statistics

        Raises:
            DatabaseException: If database operations fail
        """
        if not data:
            return {
                "success": True,
                "created": 0,
                "updated": 0,
                "errors": 0,
                "total": 0,
            }

        try:
            # Get part numbers for lookup
            part_numbers = [p.part_number for p in data]
            existing_products = await self._get_existing_products(part_numbers)

            # Statistics
            stats = {"created": 0, "updated": 0, "errors": 0, "error_details": []}

            # Process each product
            for product_data in data:
                try:
                    existing_product = existing_products.get(product_data.part_number)
                    _, is_new = await self._create_or_update_product(
                        product_data, existing_product
                    )

                    if is_new:
                        stats["created"] += 1
                    else:
                        stats["updated"] += 1

                except Exception as e:
                    logger.error(
                        f"Error importing product {product_data.part_number}: {str(e)}"
                    )
                    stats["errors"] += 1
                    stats["error_details"].append(
                        {"part_number": product_data.part_number, "error": str(e)}
                    )

            # Ensure we've flushed all changes
            await self.db.flush()

            # Commit the transaction
            await self.db.commit()

            logger.info(
                f"Import complete: created {stats['created']}, "
                f"updated {stats['updated']}, "
                f"errors {stats['errors']}, "
                f"total {len(data)}"
            )

            return {
                "success": stats["errors"] == 0,
                "created": stats["created"],
                "updated": stats["updated"],
                "errors": stats["errors"],
                "error_details": stats["error_details"] if stats["errors"] > 0 else [],
                "total": len(data),
            }
        except Exception as e:
            # Roll back the transaction on error
            await self.db.rollback()
            logger.error(f"Transaction failed in import_data: {str(e)}")
            raise DatabaseException(
                message=f"Import transaction failed: {str(e)}", original_exception=e
            ) from e
