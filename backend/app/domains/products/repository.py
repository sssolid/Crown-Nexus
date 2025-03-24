from __future__ import annotations

"""Product repository implementation.

This module provides data access and persistence operations for Product entities.
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple

from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.products.models import (
    Product,
    Brand,
    Fitment,
    ProductActivity,
    ProductSupersession,
)
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, BusinessException


class ProductRepository(BaseRepository[Product, uuid.UUID]):
    """Repository for Product entity operations.

    Provides methods for querying, creating, updating, and deleting
    Product entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the product repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Product, db=db)

    async def find_by_part_number(self, part_number: str) -> Optional[Product]:
        """Find a product by exact part number.

        Args:
            part_number: The part number to search for.

        Returns:
            The product if found, None otherwise.
        """
        query = select(Product).where(
            Product.part_number == part_number, Product.is_deleted == False
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_part_number_stripped(self, part_number: str) -> List[Product]:
        """Find products by normalized part number.

        Args:
            part_number: The part number to search for.

        Returns:
            List of products with matching normalized part number.
        """
        # Normalize the part number (remove non-alphanumeric, uppercase)
        stripped = "".join(c for c in part_number if c.isalnum()).upper()

        query = select(Product).where(
            Product.part_number_stripped == stripped, Product.is_deleted == False
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def search(
        self, search_term: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Search products by various fields.

        Args:
            search_term: The term to search for.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        # Try to find by exact part number first
        exact_match = await self.find_by_part_number(search_term)
        if exact_match:
            return {
                "items": [exact_match],
                "total": 1,
                "page": 1,
                "page_size": page_size,
                "pages": 1,
            }

        # Otherwise do a more general search
        search_term_stripped = "".join(c for c in search_term if c.isalnum()).upper()

        query = (
            select(Product)
            .where(
                or_(
                    Product.part_number.ilike(f"%{search_term}%"),
                    Product.part_number_stripped.ilike(f"%{search_term_stripped}%"),
                    Product.search_vector.op("@@")(func.plainto_tsquery(search_term)),
                ),
                Product.is_deleted == False,
            )
            .order_by(
                # Order by exact match first, then by part number
                func.case(
                    (Product.part_number == search_term, 0),
                    (Product.part_number_stripped == search_term_stripped, 1),
                    else_=2,
                ),
                Product.part_number,
            )
        )

        return await self.paginate(query, page, page_size)

    async def get_active_products(
        self, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated list of active products.

        Args:
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(Product)
            .where(Product.is_active == True, Product.is_deleted == False)
            .order_by(Product.part_number)
        )

        return await self.paginate(query, page, page_size)

    async def get_by_fitment(
        self,
        year: int,
        make: str,
        model: str,
        engine: Optional[str] = None,
        transmission: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Get products compatible with a specific vehicle fitment.

        Args:
            year: Vehicle year.
            make: Vehicle make.
            model: Vehicle model.
            engine: Optional engine specification.
            transmission: Optional transmission specification.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        from app.models.associations import product_fitment_association

        # Build fitment conditions
        conditions = [
            Fitment.year == year,
            Fitment.make.ilike(make),
            Fitment.model.ilike(model),
        ]

        if engine:
            conditions.append(Fitment.engine.ilike(engine))

        if transmission:
            conditions.append(Fitment.transmission.ilike(transmission))

        # Join Product to Fitment via association table
        query = (
            select(Product)
            .join(
                product_fitment_association,
                Product.id == product_fitment_association.c.product_id,
            )
            .join(
                Fitment,
                and_(
                    Fitment.id == product_fitment_association.c.fitment_id, *conditions
                ),
            )
            .where(Product.is_deleted == False, Product.is_active == True)
            .order_by(Product.part_number)
        )

        return await self.paginate(query, page, page_size)

    async def update_status(
        self,
        product_id: uuid.UUID,
        status: str,
        reason: Optional[str] = None,
        user_id: Optional[uuid.UUID] = None,
    ) -> Tuple[Product, ProductActivity]:
        """Update a product's status and create an activity record.

        Args:
            product_id: ID of the product to update.
            status: New status value.
            reason: Optional reason for the status change.
            user_id: Optional ID of the user making the change.

        Returns:
            Tuple containing (updated product, activity record).

        Raises:
            ResourceNotFoundException: If the product is not found.
        """
        product = await self.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundException(
                resource_type="Product", resource_id=str(product_id)
            )

        # Create activity record
        activity = ProductActivity(
            product_id=product_id,
            status=status,
            reason=reason,
            changed_by_id=user_id,
            changed_at=datetime.now(),
        )

        # Update product status based on the activity
        is_active = status == "active"
        data = {"is_active": is_active}
        product = await self.update(product_id, data, user_id)

        self.db.add(activity)
        await self.db.flush()

        return product, activity

    async def create_supersession(
        self,
        old_product_id: uuid.UUID,
        new_product_id: uuid.UUID,
        reason: Optional[str] = None,
    ) -> ProductSupersession:
        """Create a product supersession (one product replacing another).

        Args:
            old_product_id: ID of the product being replaced.
            new_product_id: ID of the replacement product.
            reason: Optional reason for the supersession.

        Returns:
            The created supersession record.

        Raises:
            ResourceNotFoundException: If either product is not found.
            BusinessException: If trying to supersede a product with itself.
        """
        # Check that products exist
        old_product = await self.get_by_id(old_product_id)
        if not old_product:
            raise ResourceNotFoundException(
                resource_type="Product", resource_id=str(old_product_id)
            )

        new_product = await self.get_by_id(new_product_id)
        if not new_product:
            raise ResourceNotFoundException(
                resource_type="Product", resource_id=str(new_product_id)
            )

        # Prevent self-supersession
        if old_product_id == new_product_id:
            raise BusinessException(
                message="A product cannot supersede itself",
                details={"product_id": str(old_product_id)},
            )

        # Create supersession record
        supersession = ProductSupersession(
            old_product_id=old_product_id, new_product_id=new_product_id, reason=reason
        )

        self.db.add(supersession)
        await self.db.flush()
        await self.db.refresh(supersession)

        return supersession

    async def ensure_exists(self, product_id: uuid.UUID) -> Product:
        """Ensure a product exists by ID, raising an exception if not found.

        Args:
            product_id: The product ID to check.

        Returns:
            The product if found.

        Raises:
            ResourceNotFoundException: If the product is not found.
        """
        product = await self.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundException(
                resource_type="Product", resource_id=str(product_id)
            )
        return product


class BrandRepository(BaseRepository[Brand, uuid.UUID]):
    """Repository for Brand entity operations.

    Provides methods for querying, creating, updating, and deleting
    Brand entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the brand repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Brand, db=db)

    async def find_by_name(self, name: str) -> Optional[Brand]:
        """Find a brand by exact name.

        Args:
            name: The brand name to search for.

        Returns:
            The brand if found, None otherwise.
        """
        query = select(Brand).where(Brand.name == name, Brand.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_name_partial(self, name: str) -> List[Brand]:
        """Find brands by partial name match.

        Args:
            name: The brand name to search for.

        Returns:
            List of brands with matching names.
        """
        query = (
            select(Brand)
            .where(Brand.name.ilike(f"%{name}%"), Brand.is_deleted == False)
            .order_by(Brand.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_company(self, company_id: uuid.UUID) -> List[Brand]:
        """Get brands owned by a specific company.

        Args:
            company_id: The company ID to filter by.

        Returns:
            List of brands owned by the specified company.
        """
        query = (
            select(Brand)
            .where(Brand.parent_company_id == company_id, Brand.is_deleted == False)
            .order_by(Brand.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def ensure_exists(self, brand_id: uuid.UUID) -> Brand:
        """Ensure a brand exists by ID, raising an exception if not found.

        Args:
            brand_id: The brand ID to check.

        Returns:
            The brand if found.

        Raises:
            ResourceNotFoundException: If the brand is not found.
        """
        brand = await self.get_by_id(brand_id)
        if not brand:
            raise ResourceNotFoundException(
                resource_type="Brand", resource_id=str(brand_id)
            )
        return brand


class FitmentRepository(BaseRepository[Fitment, uuid.UUID]):
    """Repository for Fitment entity operations.

    Provides methods for querying, creating, updating, and deleting
    Fitment entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the fitment repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Fitment, db=db)

    async def find_by_vehicle(
        self,
        year: int,
        make: str,
        model: str,
        engine: Optional[str] = None,
        transmission: Optional[str] = None,
    ) -> List[Fitment]:
        """Find fitments matching a specific vehicle.

        Args:
            year: Vehicle year.
            make: Vehicle make.
            model: Vehicle model.
            engine: Optional engine specification.
            transmission: Optional transmission specification.

        Returns:
            List of matching fitments.
        """
        # Build conditions
        conditions = [
            Fitment.year == year,
            Fitment.make.ilike(make),
            Fitment.model.ilike(model),
            Fitment.is_deleted == False,
        ]

        if engine:
            conditions.append(Fitment.engine.ilike(engine))

        if transmission:
            conditions.append(Fitment.transmission.ilike(transmission))

        query = select(Fitment).where(and_(*conditions))

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_makes_by_year(self, year: int) -> List[str]:
        """Get all makes available for a specific year.

        Args:
            year: Vehicle year.

        Returns:
            List of unique make names.
        """
        query = (
            select(Fitment.make)
            .distinct()
            .where(Fitment.year == year, Fitment.is_deleted == False)
            .order_by(Fitment.make)
        )

        result = await self.db.execute(query)
        return [row[0] for row in result.all()]

    async def get_models_by_year_make(self, year: int, make: str) -> List[str]:
        """Get all models available for a specific year and make.

        Args:
            year: Vehicle year.
            make: Vehicle make.

        Returns:
            List of unique model names.
        """
        query = (
            select(Fitment.model)
            .distinct()
            .where(
                Fitment.year == year,
                Fitment.make.ilike(make),
                Fitment.is_deleted == False,
            )
            .order_by(Fitment.model)
        )

        result = await self.db.execute(query)
        return [row[0] for row in result.all()]

    async def get_years_range(self) -> Tuple[int, int]:
        """Get the minimum and maximum years in the fitment data.

        Returns:
            Tuple containing (min_year, max_year).
        """
        min_query = select(func.min(Fitment.year)).where(Fitment.is_deleted == False)
        max_query = select(func.max(Fitment.year)).where(Fitment.is_deleted == False)

        min_result = await self.db.execute(min_query)
        max_result = await self.db.execute(max_query)

        min_year = min_result.scalar() or datetime.now().year
        max_year = max_result.scalar() or datetime.now().year

        return min_year, max_year

    async def ensure_exists(self, fitment_id: uuid.UUID) -> Fitment:
        """Ensure a fitment exists by ID, raising an exception if not found.

        Args:
            fitment_id: The fitment ID to check.

        Returns:
            The fitment if found.

        Raises:
            ResourceNotFoundException: If the fitment is not found.
        """
        fitment = await self.get_by_id(fitment_id)
        if not fitment:
            raise ResourceNotFoundException(
                resource_type="Fitment", resource_id=str(fitment_id)
            )
        return fitment
