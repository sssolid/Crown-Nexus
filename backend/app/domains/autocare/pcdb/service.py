from __future__ import annotations

"""PCdb service implementation.

This module provides service methods for working with PCdb data, including
import, export, and query operations.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, ResourceNotFoundException
from app.domains.autocare.exceptions import AutocareException, PCdbException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.pcdb.repository import (
    PCdbRepository,
    PartsRepository,
    CategoryRepository,
    SubCategoryRepository,
    PositionRepository,
)

logger = logging.getLogger(__name__)


class PCdbService:
    """Service for PCdb operations.

    Provides methods for importing, exporting, and querying parts data.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the PCdb service.

        Args:
            db: The database session.
        """
        self.db = db
        self.repository = PCdbRepository(db)

    async def get_version(self) -> str:
        """Get the current version of the PCdb database.

        Returns:
            The version date as a string.
        """
        version = await self.repository.get_version()
        return version or "No version information available"

    async def update_database(self, file_path: str) -> Dict[str, Any]:
        """Update the PCdb database from a file.

        Args:
            file_path: Path to the update file.

        Returns:
            Dict with update results information.
        """
        try:
            logger.info(f"Starting PCdb database update from {file_path}")

            # Process would involve parsing the update file and
            # applying changes to database entities
            # For now, this is a placeholder implementation

            # Update the version to current date
            version = await self.repository.update_version(datetime.now())

            logger.info(f"PCdb database updated to {version.version_date}")
            return {
                "status": "success",
                "version": version.version_date.strftime("%Y-%m-%d"),
                "message": "PCdb database updated successfully",
            }
        except Exception as e:
            logger.error(f"Error updating PCdb database: {str(e)}", exc_info=True)
            raise PCdbException(f"Failed to update PCdb database: {str(e)}") from e

    async def import_from_pies(
        self, file_path: Path, params: AutocareImportParams
    ) -> Dict[str, Any]:
        """Import parts data from a PIES XML file.

        Args:
            file_path: Path to the PIES XML file.
            params: Import parameters.

        Returns:
            Dict with import results information.
        """
        try:
            logger.info(f"Starting parts import from PIES XML: {file_path}")

            # Process would involve parsing PIES XML and creating/updating
            # parts entities and their relationships
            # For now, this is a placeholder implementation

            return {
                "status": "success",
                "imported": 0,
                "updated": 0,
                "skipped": 0,
                "errors": 0,
                "details": [],
            }
        except Exception as e:
            logger.error(f"Error importing from PIES XML: {str(e)}", exc_info=True)
            raise PCdbException(f"Failed to import from PIES XML: {str(e)}") from e

    async def get_categories(self) -> List[Dict[str, Any]]:
        """Get all parts categories.

        Returns:
            List of categories with their IDs and names.
        """
        categories = await self.repository.category_repo.get_all_categories()

        return [
            {"id": category.category_id, "name": category.category_name}
            for category in categories
        ]

    async def get_subcategories_by_category(
        self, category_id: int
    ) -> List[Dict[str, Any]]:
        """Get subcategories for a specific category.

        Args:
            category_id: The category ID.

        Returns:
            List of subcategories with their IDs and names.
        """
        subcategories = await self.repository.subcategory_repo.get_by_category(
            category_id
        )

        return [
            {"id": subcategory.subcategory_id, "name": subcategory.subcategory_name}
            for subcategory in subcategories
        ]

    async def search_parts(
        self,
        search_term: str,
        categories: Optional[List[int]] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Search for parts with optional category filters.

        Args:
            search_term: The search term.
            categories: Optional list of category IDs to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        result = await self.repository.search_parts(
            search_term=search_term,
            categories=categories,
            page=page,
            page_size=page_size,
        )

        # Transform the parts into a more user-friendly format
        parts = []
        for part in result["items"]:
            parts.append(
                {
                    "id": str(part.id),
                    "part_terminology_id": part.part_terminology_id,
                    "name": part.part_terminology_name,
                    "description": (
                        part.description.parts_description if part.description else None
                    ),
                }
            )

        return {
            "items": parts,
            "total": result["total"],
            "page": result["page"],
            "page_size": result["page_size"],
            "pages": result["pages"],
        }

    async def get_part_details(self, part_terminology_id: int) -> Dict[str, Any]:
        """Get detailed information about a part.

        Args:
            part_terminology_id: The part terminology ID.

        Returns:
            Dict with detailed part information.
        """
        part = await self.repository.parts_repo.get_by_terminology_id(
            part_terminology_id
        )

        if not part:
            raise ResourceNotFoundException(
                resource_type="Part", resource_id=str(part_terminology_id)
            )

        # Get categories and positions for the part
        categories = []
        for part_category in part.categories:
            categories.append(
                {
                    "category": {
                        "id": part_category.category.category_id,
                        "name": part_category.category.category_name,
                    },
                    "subcategory": {
                        "id": part_category.subcategory.subcategory_id,
                        "name": part_category.subcategory.subcategory_name,
                    },
                }
            )

        positions = []
        for part_position in part.positions:
            positions.append(
                {
                    "id": part_position.position.position_id,
                    "name": part_position.position.position,
                }
            )

        # Get supersession information
        supersessions = await self.repository.parts_repo.get_supersessions(
            part_terminology_id
        )

        superseded_by = []
        for superseded in supersessions["superseded_by"]:
            superseded_by.append(
                {
                    "id": superseded.part_terminology_id,
                    "name": superseded.part_terminology_name,
                }
            )

        supersedes = []
        for supersede in supersessions["supersedes"]:
            supersedes.append(
                {
                    "id": supersede.part_terminology_id,
                    "name": supersede.part_terminology_name,
                }
            )

        return {
            "id": str(part.id),
            "part_terminology_id": part.part_terminology_id,
            "name": part.part_terminology_name,
            "description": (
                part.description.parts_description if part.description else None
            ),
            "categories": categories,
            "positions": positions,
            "superseded_by": superseded_by,
            "supersedes": supersedes,
        }
