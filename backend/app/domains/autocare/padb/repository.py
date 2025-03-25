from __future__ import annotations

"""PAdb repository implementation.

This module provides data access and persistence operations for PAdb entities.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundException
from app.repositories.base import BaseRepository
from app.domains.autocare.padb.models import (
    PartAttribute,
    MetaData,
    MeasurementGroup,
    MetaUOMCode,
    PartAttributeAssignment,
    MetaUomCodeAssignment,
    ValidValue,
    ValidValueAssignment,
    Style,
    PAdbVersion,
)


class PAdbRepository:
    """Repository for PAdb entity operations.

    Provides methods for querying PAdb data and managing database updates.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the PAdb repository.

        Args:
            db: The database session.
        """
        self.db = db
        self.attribute_repo = PartAttributeRepository(db)
        self.metadata_repo = MetaDataRepository(db)
        self.valid_value_repo = ValidValueRepository(db)
        self.uom_repo = MetaUOMCodeRepository(db)

    async def get_version(self) -> Optional[str]:
        """Get the current version of the PAdb database.

        Returns:
            The version date as a string or None if no version is set.
        """
        query = select(PAdbVersion).where(PAdbVersion.is_current == True)
        result = await self.db.execute(query)
        version = result.scalars().first()

        if version:
            return version.version_date.strftime("%Y-%m-%d")
        return None

    async def update_version(self, version_date: datetime) -> PAdbVersion:
        """Update the current version of the PAdb database.

        Args:
            version_date: The new version date.

        Returns:
            The updated version entity.
        """
        # Set all existing versions to not current
        await self.db.execute(
            select(PAdbVersion)
            .where(PAdbVersion.is_current == True)
            .update({PAdbVersion.is_current: False})
        )

        # Create new current version
        version = PAdbVersion(version_date=version_date, is_current=True)
        self.db.add(version)
        await self.db.flush()

        return version

    async def get_attributes_for_part(
        self, part_terminology_id: int
    ) -> List[Dict[str, Any]]:
        """Get all attributes for a specific part.

        Args:
            part_terminology_id: The part terminology ID.

        Returns:
            List of attribute assignments with related attribute information.
        """
        query = (
            select(PartAttributeAssignment, PartAttribute, MetaData)
            .join(PartAttribute, PartAttributeAssignment.pa_id == PartAttribute.pa_id)
            .join(MetaData, PartAttributeAssignment.meta_id == MetaData.meta_id)
            .where(PartAttributeAssignment.part_terminology_id == part_terminology_id)
        )

        result = await self.db.execute(query)
        attributes = []

        for assignment, attribute, metadata in result:
            # Get valid values for this attribute
            valid_values = await self.valid_value_repo.get_for_attribute_assignment(
                assignment.papt_id
            )

            # Get UOM codes for this attribute
            uom_codes = await self.uom_repo.get_for_attribute_assignment(
                assignment.papt_id
            )

            attributes.append(
                {
                    "assignment": assignment,
                    "attribute": attribute,
                    "metadata": metadata,
                    "valid_values": valid_values,
                    "uom_codes": uom_codes,
                }
            )

        return attributes


class PartAttributeRepository(BaseRepository[PartAttribute, uuid.UUID]):
    """Repository for PartAttribute entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the part attribute repository.

        Args:
            db: The database session.
        """
        super().__init__(model=PartAttribute, db=db)

    async def get_by_pa_id(self, pa_id: int) -> Optional[PartAttribute]:
        """Get an attribute by its ID.

        Args:
            pa_id: The attribute ID.

        Returns:
            The attribute if found, None otherwise.
        """
        query = select(PartAttribute).where(PartAttribute.pa_id == pa_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def search(
        self, search_term: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Search for attributes by name.

        Args:
            search_term: The search term.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(PartAttribute)
            .where(PartAttribute.pa_name.ilike(f"%{search_term}%"))
            .order_by(PartAttribute.pa_name)
        )

        return await self.paginate(query, page, page_size)


class MetaDataRepository(BaseRepository[MetaData, uuid.UUID]):
    """Repository for MetaData entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the metadata repository.

        Args:
            db: The database session.
        """
        super().__init__(model=MetaData, db=db)

    async def get_by_meta_id(self, meta_id: int) -> Optional[MetaData]:
        """Get metadata by its ID.

        Args:
            meta_id: The metadata ID.

        Returns:
            The metadata if found, None otherwise.
        """
        query = select(MetaData).where(MetaData.meta_id == meta_id)
        result = await self.db.execute(query)
        return result.scalars().first()


class ValidValueRepository(BaseRepository[ValidValue, uuid.UUID]):
    """Repository for ValidValue entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the valid value repository.

        Args:
            db: The database session.
        """
        super().__init__(model=ValidValue, db=db)

    async def get_by_valid_value_id(self, valid_value_id: int) -> Optional[ValidValue]:
        """Get a valid value by its ID.

        Args:
            valid_value_id: The valid value ID.

        Returns:
            The valid value if found, None otherwise.
        """
        query = select(ValidValue).where(ValidValue.valid_value_id == valid_value_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_for_attribute_assignment(self, papt_id: int) -> List[ValidValue]:
        """Get valid values for a specific attribute assignment.

        Args:
            papt_id: The part attribute assignment ID.

        Returns:
            List of valid values for the specified assignment.
        """
        query = (
            select(ValidValue)
            .join(
                ValidValueAssignment,
                ValidValue.valid_value_id == ValidValueAssignment.valid_value_id,
            )
            .where(ValidValueAssignment.papt_id == papt_id)
            .order_by(ValidValue.valid_value)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())


class MetaUOMCodeRepository(BaseRepository[MetaUOMCode, uuid.UUID]):
    """Repository for MetaUOMCode entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the UOM code repository.

        Args:
            db: The database session.
        """
        super().__init__(model=MetaUOMCode, db=db)

    async def get_by_meta_uom_id(self, meta_uom_id: int) -> Optional[MetaUOMCode]:
        """Get a UOM code by its ID.

        Args:
            meta_uom_id: The UOM code ID.

        Returns:
            The UOM code if found, None otherwise.
        """
        query = select(MetaUOMCode).where(MetaUOMCode.meta_uom_id == meta_uom_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_for_attribute_assignment(self, papt_id: int) -> List[MetaUOMCode]:
        """Get UOM codes for a specific attribute assignment.

        Args:
            papt_id: The part attribute assignment ID.

        Returns:
            List of UOM codes for the specified assignment.
        """
        query = (
            select(MetaUOMCode)
            .join(
                MetaUomCodeAssignment,
                MetaUOMCode.meta_uom_id == MetaUomCodeAssignment.meta_uom_id,
            )
            .where(MetaUomCodeAssignment.papt_id == papt_id)
            .order_by(MetaUOMCode.uom_code)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())
