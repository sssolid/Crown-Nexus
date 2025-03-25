from __future__ import annotations

"""Fitment mapping repository implementation.

This module provides data access and persistence operations for fitment mapping entities.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import select, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundException
from app.repositories.base import BaseRepository
from app.domains.autocare.fitment.models import FitmentMapping, FitmentMappingHistory


class FitmentMappingRepository(BaseRepository[FitmentMapping, uuid.UUID]):
    """Repository for FitmentMapping entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the fitment mapping repository.

        Args:
            db: The database session.
        """
        super().__init__(model=FitmentMapping, db=db)

    async def find_by_product(
        self, product_id: uuid.UUID, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Find fitment mappings for a specific product.

        Args:
            product_id: The product ID.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(FitmentMapping)
            .where(FitmentMapping.product_id == product_id)
            .order_by(desc(FitmentMapping.updated_at))
        )

        return await self.paginate(query, page, page_size)

    async def find_by_vehicle(
        self, vehicle_id: int, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Find fitment mappings for a specific vehicle.

        Args:
            vehicle_id: The vehicle ID.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(FitmentMapping)
            .where(FitmentMapping.vehicle_id == vehicle_id)
            .order_by(desc(FitmentMapping.updated_at))
        )

        return await self.paginate(query, page, page_size)

    async def find_by_base_vehicle(
        self, base_vehicle_id: int, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Find fitment mappings for a specific base vehicle.

        Args:
            base_vehicle_id: The base vehicle ID.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(FitmentMapping)
            .where(FitmentMapping.base_vehicle_id == base_vehicle_id)
            .order_by(desc(FitmentMapping.updated_at))
        )

        return await self.paginate(query, page, page_size)

    async def find_by_part(
        self, part_terminology_id: int, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Find fitment mappings for a specific part.

        Args:
            part_terminology_id: The part terminology ID.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(FitmentMapping)
            .where(FitmentMapping.part_terminology_id == part_terminology_id)
            .order_by(desc(FitmentMapping.updated_at))
        )

        return await self.paginate(query, page, page_size)

    async def search(
        self,
        product_query: Optional[str] = None,
        is_validated: Optional[bool] = None,
        is_manual: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Search for fitment mappings with various filters.

        Args:
            product_query: Optional product part number or name to search.
            is_validated: Optional validation status filter.
            is_manual: Optional manual entry filter.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        from app.domains.products.models import Product

        # Start building the query
        query = select(FitmentMapping)

        # Add filters
        conditions = []

        if product_query:
            # Join with Product to search by part number
            query = query.join(Product, FitmentMapping.product_id == Product.id)
            conditions.append(
                or_(
                    Product.part_number.ilike(f"%{product_query}%"),
                    Product.part_number_stripped.ilike(f"%{product_query}%"),
                )
            )

        if is_validated is not None:
            conditions.append(FitmentMapping.is_validated == is_validated)

        if is_manual is not None:
            conditions.append(FitmentMapping.is_manual == is_manual)

        if conditions:
            query = query.where(and_(*conditions))

        # Order by most recently updated
        query = query.order_by(desc(FitmentMapping.updated_at))

        return await self.paginate(query, page, page_size)

    async def create_with_history(
        self, data: Dict[str, Any], user_id: Optional[uuid.UUID] = None
    ) -> FitmentMapping:
        """Create a new fitment mapping and record history.

        Args:
            data: The mapping data.
            user_id: Optional ID of the user creating the mapping.

        Returns:
            The created mapping.
        """
        # Create the mapping
        mapping_data = data.copy()
        if user_id:
            mapping_data["created_by_id"] = user_id
            mapping_data["updated_by_id"] = user_id

        mapping = FitmentMapping(**mapping_data)
        self.db.add(mapping)
        await self.db.flush()

        # Create history record
        history = FitmentMappingHistory(
            mapping_id=mapping.id,
            change_type="CREATE",
            new_values=mapping_data,
            changed_by_id=user_id,
        )
        self.db.add(history)
        await self.db.flush()

        return mapping

    async def update_with_history(
        self, id: uuid.UUID, data: Dict[str, Any], user_id: Optional[uuid.UUID] = None
    ) -> FitmentMapping:
        """Update a fitment mapping and record history.

        Args:
            id: The mapping ID.
            data: The updated mapping data.
            user_id: Optional ID of the user updating the mapping.

        Returns:
            The updated mapping.

        Raises:
            ResourceNotFoundException: If the mapping is not found.
        """
        # Get the current mapping
        mapping = await self.get_by_id(id)
        if not mapping:
            raise ResourceNotFoundException(
                resource_type="FitmentMapping", resource_id=str(id)
            )

        # Store previous values
        previous_values = {
            "vehicle_id": mapping.vehicle_id,
            "base_vehicle_id": mapping.base_vehicle_id,
            "part_terminology_id": mapping.part_terminology_id,
            "position_id": mapping.position_id,
            "attributes": mapping.attributes,
            "is_validated": mapping.is_validated,
            "is_manual": mapping.is_manual,
            "notes": mapping.notes,
        }

        # Update the mapping
        update_data = data.copy()
        if user_id:
            update_data["updated_by_id"] = user_id

        # Apply the update
        for key, value in update_data.items():
            setattr(mapping, key, value)

        # Update timestamps
        mapping.updated_at = datetime.now()

        # Create history record
        history = FitmentMappingHistory(
            mapping_id=mapping.id,
            change_type="UPDATE",
            previous_values=previous_values,
            new_values=update_data,
            changed_by_id=user_id,
        )
        self.db.add(history)

        await self.db.flush()
        return mapping

    async def delete_with_history(
        self, id: uuid.UUID, user_id: Optional[uuid.UUID] = None
    ) -> None:
        """Delete a fitment mapping and record history.

        Args:
            id: The mapping ID.
            user_id: Optional ID of the user deleting the mapping.

        Raises:
            ResourceNotFoundException: If the mapping is not found.
        """
        # Get the current mapping
        mapping = await self.get_by_id(id)
        if not mapping:
            raise ResourceNotFoundException(
                resource_type="FitmentMapping", resource_id=str(id)
            )

        # Store all values
        previous_values = {
            "product_id": str(mapping.product_id),
            "vehicle_id": mapping.vehicle_id,
            "base_vehicle_id": mapping.base_vehicle_id,
            "part_terminology_id": mapping.part_terminology_id,
            "position_id": mapping.position_id,
            "attributes": mapping.attributes,
            "is_validated": mapping.is_validated,
            "is_manual": mapping.is_manual,
            "notes": mapping.notes,
        }

        # Create history record
        history = FitmentMappingHistory(
            mapping_id=mapping.id,
            change_type="DELETE",
            previous_values=previous_values,
            changed_by_id=user_id,
        )
        self.db.add(history)

        # Mark as deleted
        await self.soft_delete(id)
        await self.db.flush()

    async def get_mapping_history(
        self, mapping_id: uuid.UUID, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get history for a specific mapping.

        Args:
            mapping_id: The mapping ID.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(FitmentMappingHistory)
            .where(FitmentMappingHistory.mapping_id == mapping_id)
            .order_by(desc(FitmentMappingHistory.changed_at))
        )

        # Execute the paginated query
        total = await self.count(query)

        # Calculate pagination values
        total_pages = (total + page_size - 1) // page_size
        offset = (page - 1) * page_size

        # Apply pagination
        query = query.offset(offset).limit(page_size)

        # Execute query
        result = await self.db.execute(query)
        items = list(result.scalars().all())

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": total_pages,
        }
