from __future__ import annotations

"""VCdb service implementation.

This module provides service methods for working with VCdb data, including
import, export, and query operations.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, ResourceNotFoundException
from app.domains.autocare.exceptions import AutocareException, VCdbException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.vcdb.repository import (
    VehicleRepository,
    MakeRepository,
    ModelRepository,
    YearRepository,
    VCdbRepository,
)

logger = logging.getLogger(__name__)


class VCdbService:
    """Service for VCdb operations.

    Provides methods for importing, exporting, and querying vehicle data.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the VCdb service.

        Args:
            db: The database session.
        """
        self.db = db
        self.repository = VCdbRepository(db)

    async def get_version(self) -> str:
        """Get the current version of the VCdb database.

        Returns:
            The version date as a string.
        """
        version = await self.repository.get_version()
        return version or "No version information available"

    async def update_database(self, file_path: str) -> Dict[str, Any]:
        """Update the VCdb database from a file.

        Args:
            file_path: Path to the update file.

        Returns:
            Dict with update results information.
        """
        try:
            logger.info(f"Starting VCdb database update from {file_path}")

            # Process would involve parsing the update file and
            # applying changes to database entities
            # For now, this is a placeholder implementation

            # Update the version to current date
            version = await self.repository.update_version(datetime.now())

            logger.info(f"VCdb database updated to {version.version_date}")
            return {
                "status": "success",
                "version": version.version_date.strftime("%Y-%m-%d"),
                "message": "VCdb database updated successfully",
            }
        except Exception as e:
            logger.error(f"Error updating VCdb database: {str(e)}", exc_info=True)
            raise VCdbException(f"Failed to update VCdb database: {str(e)}") from e

    async def import_from_aces(
        self, file_path: Path, params: AutocareImportParams
    ) -> Dict[str, Any]:
        """Import vehicle data from an ACES XML file.

        Args:
            file_path: Path to the ACES XML file.
            params: Import parameters.

        Returns:
            Dict with import results information.
        """
        try:
            logger.info(f"Starting vehicle import from ACES XML: {file_path}")

            # Process would involve parsing ACES XML and creating/updating
            # vehicle entities and their relationships
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
            logger.error(f"Error importing from ACES XML: {str(e)}", exc_info=True)
            raise VCdbException(f"Failed to import from ACES XML: {str(e)}") from e

    async def get_makes_by_year(self, year: int) -> List[Dict[str, Any]]:
        """Get all makes available for a specific year.

        Args:
            year: Vehicle year.

        Returns:
            List of makes with their IDs and names.
        """
        makes = await self.repository.make_repo.get_by_year(year)

        return [{"id": make.make_id, "name": make.name} for make in makes]

    async def get_models_by_year_make(
        self, year: int, make_id: int
    ) -> List[Dict[str, Any]]:
        """Get all models available for a specific year and make.

        Args:
            year: Vehicle year.
            make_id: Make ID.

        Returns:
            List of models with their IDs and names.
        """
        models = await self.repository.model_repo.get_by_year_make(year, make_id)

        return [
            {
                "id": model.model_id,
                "name": model.name,
                "vehicle_type": {
                    "id": model.vehicle_type.vehicle_type_id,
                    "name": model.vehicle_type.name,
                },
            }
            for model in models
        ]

    async def get_submodels_by_base_vehicle(
        self, base_vehicle_id: int
    ) -> List[Dict[str, Any]]:
        """Get all submodels available for a specific base vehicle.

        Args:
            base_vehicle_id: Base vehicle ID.

        Returns:
            List of submodels with their IDs and names.
        """
        submodels = await self.repository.vehicle_repo.get_submodels_by_base_vehicle(
            base_vehicle_id
        )

        return [
            {"id": submodel.submodel_id, "name": submodel.name}
            for submodel in submodels
        ]

    async def search_vehicles(
        self,
        year: Optional[int] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Search for vehicles with optional filters.

        Args:
            year: Optional vehicle year to filter by.
            make: Optional make name to filter by.
            model: Optional model name to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        result = await self.repository.vehicle_repo.search(
            year=year, make=make, model=model, page=page, page_size=page_size
        )

        # Transform the vehicles into a more user-friendly format
        vehicles = []
        for vehicle in result["items"]:
            vehicles.append(
                {
                    "id": str(vehicle.id),
                    "vehicle_id": vehicle.vehicle_id,
                    "year": vehicle.year,
                    "make": vehicle.make.name,
                    "model": vehicle.model.name,
                    "submodel": vehicle.submodel.name,
                    "region": vehicle.region.name,
                }
            )

        return {
            "items": vehicles,
            "total": result["total"],
            "page": result["page"],
            "page_size": result["page_size"],
            "pages": result["pages"],
        }

    async def get_vehicle_details(self, vehicle_id: int) -> Dict[str, Any]:
        """Get detailed information about a vehicle.

        Args:
            vehicle_id: The vehicle ID.

        Returns:
            Dict with detailed vehicle information.
        """
        vehicle = await self.repository.vehicle_repo.get_by_vehicle_id(vehicle_id)

        if not vehicle:
            raise ResourceNotFoundException(
                resource_type="Vehicle", resource_id=str(vehicle_id)
            )

        # Get various configurations for the vehicle
        engines = []
        for engine_config in vehicle.engine_configs:
            engines.append(
                {
                    "id": engine_config.engine_config_id,
                    "liter": engine_config.engine_base.engine_block.liter,
                    "cylinders": engine_config.engine_base.engine_block.cylinders,
                    "aspiration": engine_config.aspiration.name,
                    "fuel_type": engine_config.fuel_type.name,
                }
            )

        transmissions = []
        for transmission in vehicle.transmissions:
            transmissions.append(
                {
                    "id": transmission.transmission_id,
                    "type": transmission.transmission_base.transmission_type.name,
                    "speeds": transmission.transmission_base.transmission_num_speeds.num_speeds,
                }
            )

        return {
            "id": str(vehicle.id),
            "vehicle_id": vehicle.vehicle_id,
            "year": vehicle.year,
            "make": vehicle.make.name,
            "model": vehicle.model.name,
            "submodel": vehicle.submodel.name,
            "region": vehicle.region.name,
            "engines": engines,
            "transmissions": transmissions,
            "drive_types": [dt.name for dt in vehicle.drive_types],
            "body_styles": [bs.body_type.name for bs in vehicle.body_style_configs],
        }
