from __future__ import annotations

"""Model mapping repository implementation.

This module provides data access and persistence operations for ModelMapping entities.
"""

import re
from typing import List, Optional, Dict, Any

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.model_mapping.models import ModelMapping
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException


class ModelMappingRepository(BaseRepository[ModelMapping, int]):
    """Repository for ModelMapping entity operations.

    Provides methods for querying, creating, updating, and deleting
    ModelMapping entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the model mapping repository.

        Args:
            db: The database session.
        """
        super().__init__(model=ModelMapping, db=db)

    async def find_by_pattern(self, pattern: str) -> List[ModelMapping]:
        """Find model mappings by pattern.

        Args:
            pattern: The pattern to search for.

        Returns:
            List of model mappings matching the pattern.
        """
        query = (
            select(ModelMapping)
            .where(
                ModelMapping.pattern.ilike(f"%{pattern}%"),
                ModelMapping.active == True,
                ModelMapping.is_deleted == False,
            )
            .order_by(desc(ModelMapping.priority), ModelMapping.pattern)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def find_by_make_model(self, make: str, model: str) -> List[ModelMapping]:
        """Find model mappings by make and model.

        Args:
            make: The make to search for.
            model: The model to search for.

        Returns:
            List of model mappings for the make and model.
        """
        query = (
            select(ModelMapping)
            .where(
                ModelMapping.active == True,
                ModelMapping.is_deleted == False,
                func.split_part(ModelMapping.mapping, "|", 1).ilike(f"%{make}%"),
                func.split_part(ModelMapping.mapping, "|", 3).ilike(f"%{model}%"),
            )
            .order_by(desc(ModelMapping.priority))
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def match_vehicle_string(
        self, vehicle_string: str
    ) -> Optional[Dict[str, str]]:
        """Match a vehicle string against patterns to find the correct mapping.

        Args:
            vehicle_string: The vehicle string to match.

        Returns:
            Dictionary with make, code, and model if matched, None otherwise.
        """
        # Get all active mappings, ordered by priority
        query = (
            select(ModelMapping)
            .where(ModelMapping.active == True, ModelMapping.is_deleted == False)
            .order_by(desc(ModelMapping.priority))
        )

        result = await self.db.execute(query)
        mappings = list(result.scalars().all())

        # Try to match each pattern
        for mapping in mappings:
            pattern = mapping.pattern
            if re.search(pattern, vehicle_string, re.IGNORECASE):
                parts = mapping.mapping.split("|")
                return {
                    "make": parts[0] if len(parts) > 0 else "",
                    "code": parts[1] if len(parts) > 1 else "",
                    "model": parts[2] if len(parts) > 2 else "",
                }

        return None

    async def get_by_make(self, make: str) -> List[ModelMapping]:
        """Get model mappings for a specific make.

        Args:
            make: The make to filter by.

        Returns:
            List of model mappings for the make.
        """
        query = (
            select(ModelMapping)
            .where(
                ModelMapping.active == True,
                ModelMapping.is_deleted == False,
                func.split_part(ModelMapping.mapping, "|", 1).ilike(f"%{make}%"),
            )
            .order_by(func.split_part(ModelMapping.mapping, "|", 3))
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_active_mappings(
        self, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated list of active model mappings.

        Args:
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(ModelMapping)
            .where(ModelMapping.active == True, ModelMapping.is_deleted == False)
            .order_by(desc(ModelMapping.priority), ModelMapping.pattern)
        )

        return await self.paginate(query, page, page_size)

    async def ensure_exists(self, mapping_id: int) -> ModelMapping:
        """Ensure a model mapping exists by ID, raising an exception if not found.

        Args:
            mapping_id: The model mapping ID to check.

        Returns:
            The model mapping if found.

        Raises:
            ResourceNotFoundException: If the model mapping is not found.
        """
        mapping = await self.get_by_id(mapping_id)
        if not mapping:
            raise ResourceNotFoundException(
                resource_type="ModelMapping", resource_id=str(mapping_id)
            )
        return mapping
