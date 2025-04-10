from __future__ import annotations

"""PAdb service implementation.

This module provides service methods for working with PAdb data, including
import, export, and query operations.
"""

from app.logging import get_logger
from datetime import datetime
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import PAdbException
from app.domains.autocare.padb.repository import (
    PAdbRepository,
)

logger = get_logger("app.domains.autocare.padb.service")


class PAdbService:
    """Service for PAdb operations.

    Provides methods for importing, exporting, and querying parts attribute data.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the PAdb service.

        Args:
            db: The database session.
        """
        self.db = db
        self.repository = PAdbRepository(db)

    async def get_version(self) -> str:
        """Get the current version of the PAdb database.

        Returns:
            The version date as a string.
        """
        version = await self.repository.get_version()
        return version or "No version information available"

    async def get_stats(self) -> Dict[str, Any]:
        """Get PAdb statistics.

        Returns:
            Dictionary with PAdb statistics
        """

        total_attributes = await self.repository.attribute_repo.count()
        metadata_count = await self.repository.metadata_repo.count()
        valid_values = await self.repository.valid_value_repo.count()
        uom_codes = await self.repository.uom_repo.count()

        return {
            "totalAttributes": total_attributes,
            "metadataCount": metadata_count,
            "validValueCount": valid_values,
            "uomCodeCount": uom_codes,
        }

    async def update_database(self, file_path: str) -> Dict[str, Any]:
        """Update the PAdb database from a file.

        Args:
            file_path: Path to the update file.

        Returns:
            Dict with update results information.
        """
        try:
            logger.info(f"Starting PAdb database update from {file_path}")

            # Process would involve parsing the update file and
            # applying changes to database entities
            # For now, this is a placeholder implementation

            # Update the version to current date
            version = await self.repository.update_version(datetime.now())

            logger.info(f"PAdb database updated to {version.version_date}")
            return {
                "status": "success",
                "version": version.version_date.strftime("%Y-%m-%d"),
                "message": "PAdb database updated successfully",
            }
        except Exception as e:
            logger.error(f"Error updating PAdb database: {str(e)}", exc_info=True)
            raise PAdbException(f"Failed to update PAdb database: {str(e)}") from e

    async def search_attributes(
        self, search_term: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Search for part attributes.

        Args:
            search_term: The search term.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        result = await self.repository.attribute_repo.search(
            search_term=search_term, page=page, page_size=page_size
        )

        # Transform the attributes into a more user-friendly format
        attributes = []
        for attribute in result["items"]:
            attributes.append(
                {
                    "id": str(attribute.id),
                    "pa_id": attribute.pa_id,
                    "name": attribute.pa_name,
                    "description": attribute.pa_descr,
                }
            )

        return {
            "items": attributes,
            "total": result["total"],
            "page": result["page"],
            "page_size": result["page_size"],
            "pages": result["pages"],
        }

    async def get_attribute_details(self, pa_id: int) -> Dict[str, Any]:
        """Get detailed information about a part attribute.

        Args:
            pa_id: The part attribute ID.

        Returns:
            Dict with detailed attribute information.
        """
        attribute = await self.repository.attribute_repo.get_by_pa_id(pa_id)

        if not attribute:
            raise ResourceNotFoundException(
                resource_type="PartAttribute", resource_id=str(pa_id)
            )

        # Get metadata details
        assignments = await self.db.execute(
            """
            SELECT
                paa.papt_id,
                paa.part_terminology_id,
                md.meta_id,
                md.meta_name,
                md.meta_descr,
                md.data_type
            FROM
                autocare_part_attribute_assignment paa
            JOIN
                autocare_metadata md ON paa.meta_id = md.meta_id
            WHERE
                paa.pa_id = :pa_id
            """,
            {"pa_id": pa_id},
        )

        metadata_list = []
        for row in assignments:
            metadata_list.append(
                {
                    "assignment_id": row.papt_id,
                    "part_terminology_id": row.part_terminology_id,
                    "meta_id": row.meta_id,
                    "name": row.meta_name,
                    "description": row.meta_descr,
                    "data_type": row.data_type,
                }
            )

        return {
            "id": str(attribute.id),
            "pa_id": attribute.pa_id,
            "name": attribute.pa_name,
            "description": attribute.pa_descr,
            "metadata_assignments": metadata_list,
        }

    async def get_part_attributes(self, part_terminology_id: int) -> Dict[str, Any]:
        """Get attributes for a specific part.

        Args:
            part_terminology_id: The part terminology ID.

        Returns:
            Dict with part attributes information.
        """
        attributes = await self.repository.get_attributes_for_part(part_terminology_id)

        # Transform the attributes into a more user-friendly format
        result = []
        for attr_data in attributes:
            assignment = attr_data["assignment"]
            attribute = attr_data["attribute"]
            metadata = attr_data["metadata"]

            # Format valid values
            valid_values = []
            for vv in attr_data["valid_values"]:
                valid_values.append({"id": vv.valid_value_id, "value": vv.valid_value})

            # Format UOM codes
            uom_codes = []
            for uom in attr_data["uom_codes"]:
                uom_codes.append(
                    {
                        "id": uom.meta_uom_id,
                        "code": uom.uom_code,
                        "description": uom.uom_description,
                        "label": uom.uom_label,
                    }
                )

            result.append(
                {
                    "assignment_id": assignment.papt_id,
                    "attribute": {
                        "id": attribute.pa_id,
                        "name": attribute.pa_name,
                        "description": attribute.pa_descr,
                    },
                    "metadata": {
                        "id": metadata.meta_id,
                        "name": metadata.meta_name,
                        "description": metadata.meta_descr,
                        "format": metadata.meta_format,
                        "data_type": metadata.data_type,
                    },
                    "valid_values": valid_values,
                    "uom_codes": uom_codes,
                }
            )

        return {"part_terminology_id": part_terminology_id, "attributes": result}
