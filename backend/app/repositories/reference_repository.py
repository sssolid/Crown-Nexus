from __future__ import annotations

"""Reference repository implementation.

This module provides data access and persistence operations for reference entities.
"""

import uuid
from typing import List, Optional, Dict, Any

from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reference import (
    Color,
    ConstructionType,
    Texture,
    PackagingType,
    Hardware,
    TariffCode,
    UnspscCode,
    Warehouse,
)
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException


class ColorRepository(BaseRepository[Color, uuid.UUID]):
    """Repository for Color entity operations.

    Provides methods for querying, creating, updating, and deleting
    Color entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the color repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Color, db=db)

    async def find_by_name(self, name: str) -> Optional[Color]:
        """Find a color by name.

        Args:
            name: The color name to search for.

        Returns:
            The color if found, None otherwise.
        """
        query = select(Color).where(Color.name.ilike(name), Color.is_deleted == False)

        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_hex(self, hex_code: str) -> Optional[Color]:
        """Find a color by hex code.

        Args:
            hex_code: The hex code to search for.

        Returns:
            The color if found, None otherwise.
        """
        # Normalize hex code (add # if missing)
        if hex_code and not hex_code.startswith("#"):
            hex_code = f"#{hex_code}"

        query = select(Color).where(
            Color.hex_code == hex_code, Color.is_deleted == False
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def ensure_exists(self, color_id: uuid.UUID) -> Color:
        """Ensure a color exists by ID, raising an exception if not found.

        Args:
            color_id: The color ID to check.

        Returns:
            The color if found.

        Raises:
            ResourceNotFoundException: If the color is not found.
        """
        color = await self.get_by_id(color_id)
        if not color:
            raise ResourceNotFoundException(
                resource_type="Color", resource_id=str(color_id)
            )
        return color


class WarehouseRepository(BaseRepository[Warehouse, uuid.UUID]):
    """Repository for Warehouse entity operations.

    Provides methods for querying, creating, updating, and deleting
    Warehouse entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the warehouse repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Warehouse, db=db)

    async def find_by_name(self, name: str) -> Optional[Warehouse]:
        """Find a warehouse by name.

        Args:
            name: The warehouse name to search for.

        Returns:
            The warehouse if found, None otherwise.
        """
        query = select(Warehouse).where(
            Warehouse.name.ilike(name), Warehouse.is_deleted == False
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_active_warehouses(self) -> List[Warehouse]:
        """Get all active warehouses.

        Returns:
            List of active warehouses.
        """
        query = (
            select(Warehouse)
            .where(Warehouse.is_active == True, Warehouse.is_deleted == False)
            .order_by(Warehouse.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def ensure_exists(self, warehouse_id: uuid.UUID) -> Warehouse:
        """Ensure a warehouse exists by ID, raising an exception if not found.

        Args:
            warehouse_id: The warehouse ID to check.

        Returns:
            The warehouse if found.

        Raises:
            ResourceNotFoundException: If the warehouse is not found.
        """
        warehouse = await self.get_by_id(warehouse_id)
        if not warehouse:
            raise ResourceNotFoundException(
                resource_type="Warehouse", resource_id=str(warehouse_id)
            )
        return warehouse


class TariffCodeRepository(BaseRepository[TariffCode, uuid.UUID]):
    """Repository for TariffCode entity operations.

    Provides methods for querying, creating, updating, and deleting
    TariffCode entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the tariff code repository.

        Args:
            db: The database session.
        """
        super().__init__(model=TariffCode, db=db)

    async def find_by_code(self, code: str) -> List[TariffCode]:
        """Find tariff codes by code string.

        Args:
            code: The tariff code to search for.

        Returns:
            List of matching tariff codes.
        """
        query = (
            select(TariffCode)
            .where(TariffCode.code.ilike(f"%{code}%"), TariffCode.is_deleted == False)
            .order_by(TariffCode.code)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_country(self, country_id: uuid.UUID) -> List[TariffCode]:
        """Get tariff codes for a specific country.

        Args:
            country_id: The country ID to filter by.

        Returns:
            List of tariff codes for the country.
        """
        query = (
            select(TariffCode)
            .where(TariffCode.country_id == country_id, TariffCode.is_deleted == False)
            .order_by(TariffCode.code)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def ensure_exists(self, tariff_code_id: uuid.UUID) -> TariffCode:
        """Ensure a tariff code exists by ID, raising an exception if not found.

        Args:
            tariff_code_id: The tariff code ID to check.

        Returns:
            The tariff code if found.

        Raises:
            ResourceNotFoundException: If the tariff code is not found.
        """
        tariff_code = await self.get_by_id(tariff_code_id)
        if not tariff_code:
            raise ResourceNotFoundException(
                resource_type="TariffCode", resource_id=str(tariff_code_id)
            )
        return tariff_code


class UnspscCodeRepository(BaseRepository[UnspscCode, uuid.UUID]):
    """Repository for UnspscCode entity operations.

    Provides methods for querying, creating, updating, and deleting
    UnspscCode entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the UNSPSC code repository.

        Args:
            db: The database session.
        """
        super().__init__(model=UnspscCode, db=db)

    async def find_by_code(self, code: str) -> Optional[UnspscCode]:
        """Find a UNSPSC code by exact code.

        Args:
            code: The UNSPSC code to search for.

        Returns:
            The UNSPSC code if found, None otherwise.
        """
        query = select(UnspscCode).where(
            UnspscCode.code == code, UnspscCode.is_deleted == False
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_segment(self, segment: str) -> List[UnspscCode]:
        """Find UNSPSC codes by segment.

        Args:
            segment: The segment to filter by.

        Returns:
            List of UNSPSC codes in the segment.
        """
        query = (
            select(UnspscCode)
            .where(
                UnspscCode.segment.ilike(f"%{segment}%"), UnspscCode.is_deleted == False
            )
            .order_by(UnspscCode.code)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def find_by_description(self, description: str) -> List[UnspscCode]:
        """Find UNSPSC codes by description (partial match).

        Args:
            description: The description text to search for.

        Returns:
            List of UNSPSC codes with matching descriptions.
        """
        query = (
            select(UnspscCode)
            .where(
                UnspscCode.description.ilike(f"%{description}%"),
                UnspscCode.is_deleted == False,
            )
            .order_by(UnspscCode.code)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def ensure_exists(self, unspsc_code_id: uuid.UUID) -> UnspscCode:
        """Ensure a UNSPSC code exists by ID, raising an exception if not found.

        Args:
            unspsc_code_id: The UNSPSC code ID to check.

        Returns:
            The UNSPSC code if found.

        Raises:
            ResourceNotFoundException: If the UNSPSC code is not found.
        """
        unspsc_code = await self.get_by_id(unspsc_code_id)
        if not unspsc_code:
            raise ResourceNotFoundException(
                resource_type="UnspscCode", resource_id=str(unspsc_code_id)
            )
        return unspsc_code
