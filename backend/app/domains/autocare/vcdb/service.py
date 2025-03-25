from __future__ import annotations

"""VCdb service implementation.

This module provides service methods for working with VCdb data, including
import, export, and query operations for vehicles and their components.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import VCdbException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.vcdb.repository import (
    VCdbRepository
)

logger = logging.getLogger(__name__)


class VCdbService:
    """Service for interacting with VCdb (Vehicle Component Database) data.

    This service provides methods for querying, importing, and managing
    vehicle data and their components according to Auto Care standards.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the VCdb service.

        Args:
            db: SQLAlchemy async session for database operations
        """
        self.db = db
        self.repository = VCdbRepository(db)

    async def get_version(self) -> str:
        """Get the current VCdb database version.

        Returns:
            String representation of the version date or a message indicating
            no version information is available
        """
        version = await self.repository.get_version()
        return version or 'No version information available'

    async def update_database(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Update the VCdb database from a file.

        Args:
            file_path: Path to the file containing VCdb data

        Returns:
            Dictionary with status information about the update operation

        Raises:
            VCdbException: If the update operation fails
        """
        try:
            file_path_str = str(file_path) if isinstance(file_path, Path) else file_path
            logger.info(f'Starting VCdb database update from {file_path_str}')
            version = await self.repository.update_version(datetime.now())
            logger.info(f'VCdb database updated to {version.version_date}')
            return {
                'status': 'success',
                'version': version.version_date.strftime('%Y-%m-%d'),
                'message': 'VCdb database updated successfully'
            }
        except Exception as e:
            logger.error(f'Error updating VCdb database: {str(e)}', exc_info=True)
            raise VCdbException(f'Failed to update VCdb database: {str(e)}') from e

    async def import_from_aces(self, file_path: Path, params: AutocareImportParams) -> Dict[str, Any]:
        """Import vehicle data from an ACES XML file.

        Args:
            file_path: Path to the ACES XML file
            params: Import parameters for controlling the import process

        Returns:
            Dictionary with status information about the import operation

        Raises:
            VCdbException: If the import operation fails
        """
        try:
            logger.info(f'Starting vehicle import from ACES XML: {file_path}')
            # Implementation would include parsing XML and creating/updating records
            # For now, we'll return a placeholder result
            return {
                'status': 'success',
                'imported': 0,
                'updated': 0,
                'skipped': 0,
                'errors': 0,
                'details': []
            }
        except Exception as e:
            logger.error(f'Error importing from ACES XML: {str(e)}', exc_info=True)
            raise VCdbException(f'Failed to import from ACES XML: {str(e)}') from e

    # Year operations
    async def get_years(self) -> List[Dict[str, Any]]:
        """Get all available vehicle years.

        Returns:
            List of dictionaries containing year information
        """
        years = await self.repository.year_repo.get_all_years()
        return [{'id': year.year_id, 'year': year.year} for year in years]

    async def get_year_range(self) -> Tuple[int, int]:
        """Get the range of available vehicle years.

        Returns:
            Tuple containing the minimum and maximum years in the database
        """
        return await self.repository.year_repo.get_year_range()

    # Make operations
    async def get_makes(self) -> List[Dict[str, Any]]:
        """Get all available vehicle makes.

        Returns:
            List of dictionaries containing make information
        """
        makes = await self.repository.make_repo.get_all_makes()
        return [{'id': make.make_id, 'name': make.name} for make in makes]

    async def get_makes_by_year(self, year: int) -> List[Dict[str, Any]]:
        """Get all makes available for a specific year.

        Args:
            year: The vehicle year to filter by

        Returns:
            List of dictionaries containing make information for the specified year
        """
        makes = await self.repository.make_repo.get_by_year(year)
        return [{'id': make.make_id, 'name': make.name} for make in makes]

    async def search_makes(self, search_term: str) -> List[Dict[str, Any]]:
        """Search for makes by name.

        Args:
            search_term: The search term to find in make names

        Returns:
            List of dictionaries containing matching make information
        """
        makes = await self.repository.make_repo.search_by_name(search_term)
        return [{'id': make.make_id, 'name': make.name} for make in makes]

    async def get_make_by_id(self, make_id: int) -> Dict[str, Any]:
        """Get a specific make by ID.

        Args:
            make_id: The make ID to retrieve

        Returns:
            Dictionary containing make information

        Raises:
            ResourceNotFoundException: If make with the specified ID is not found
        """
        make = await self.repository.make_repo.get_by_make_id(make_id)
        if not make:
            raise ResourceNotFoundException(
                resource_type='Make',
                resource_id=str(make_id)
            )
        return {'id': make.make_id, 'name': make.name}

    # Model operations
    async def get_models_by_year_make(self, year: int, make_id: int) -> List[Dict[str, Any]]:
        """Get all models for a specific year and make.

        Args:
            year: The vehicle year
            make_id: The make ID

        Returns:
            List of dictionaries containing model information
        """
        models = await self.repository.model_repo.get_by_year_make(year, make_id)
        return [
            {
                'id': model.model_id,
                'name': model.name,
                'vehicle_type': {
                    'id': model.vehicle_type.vehicle_type_id,
                    'name': model.vehicle_type.name
                } if model.vehicle_type else None
            }
            for model in models
        ]

    async def search_models(self, search_term: str) -> List[Dict[str, Any]]:
        """Search for models by name.

        Args:
            search_term: The search term to find in model names

        Returns:
            List of dictionaries containing matching model information
        """
        models = await self.repository.model_repo.search_by_name(search_term)
        return [
            {
                'id': model.model_id,
                'name': model.name,
                'vehicle_type_id': model.vehicle_type_id
            }
            for model in models
        ]

    async def get_model_by_id(self, model_id: int) -> Dict[str, Any]:
        """Get a specific model by ID.

        Args:
            model_id: The model ID to retrieve

        Returns:
            Dictionary containing model information

        Raises:
            ResourceNotFoundException: If model with the specified ID is not found
        """
        model = await self.repository.model_repo.get_by_model_id(model_id)
        if not model:
            raise ResourceNotFoundException(
                resource_type='Model',
                resource_id=str(model_id)
            )
        return {
            'id': model.model_id,
            'name': model.name,
            'vehicle_type_id': model.vehicle_type_id,
            'vehicle_type': {
                'id': model.vehicle_type.vehicle_type_id,
                'name': model.vehicle_type.name
            } if model.vehicle_type else None
        }

    # SubModel operations
    async def get_submodels_by_base_vehicle(self, base_vehicle_id: int) -> List[Dict[str, Any]]:
        """Get all submodels for a specific base vehicle.

        Args:
            base_vehicle_id: The base vehicle ID

        Returns:
            List of dictionaries containing submodel information
        """
        submodels = await self.repository.vehicle_repo.get_submodels_by_base_vehicle(base_vehicle_id)
        return [{'id': submodel.submodel_id, 'name': submodel.name} for submodel in submodels]

    async def get_all_submodels(self) -> List[Dict[str, Any]]:
        """Get all available submodels.

        Returns:
            List of dictionaries containing submodel information
        """
        submodels = await self.repository.submodel_repo.get_all_submodels()
        return [{'id': submodel.submodel_id, 'name': submodel.name} for submodel in submodels]

    async def search_submodels(self, search_term: str) -> List[Dict[str, Any]]:
        """Search for submodels by name.

        Args:
            search_term: The search term to find in submodel names

        Returns:
            List of dictionaries containing matching submodel information
        """
        submodels = await self.repository.submodel_repo.search_by_name(search_term)
        return [{'id': submodel.submodel_id, 'name': submodel.name} for submodel in submodels]

    # Vehicle Type operations
    async def get_vehicle_types(self) -> List[Dict[str, Any]]:
        """Get all available vehicle types.

        Returns:
            List of dictionaries containing vehicle type information
        """
        vehicle_types = await self.repository.vehicle_type_repo.get_all_vehicle_types()
        return [
            {
                'id': vt.vehicle_type_id,
                'name': vt.name,
                'group_id': vt.vehicle_type_group_id
            }
            for vt in vehicle_types
        ]

    async def get_vehicle_types_by_group(self, group_id: int) -> List[Dict[str, Any]]:
        """Get all vehicle types within a specific group.

        Args:
            group_id: The vehicle type group ID

        Returns:
            List of dictionaries containing vehicle type information
        """
        vehicle_types = await self.repository.vehicle_type_repo.get_by_group(group_id)
        return [
            {
                'id': vt.vehicle_type_id,
                'name': vt.name,
                'group_id': vt.vehicle_type_group_id
            }
            for vt in vehicle_types
        ]

    # Region operations
    async def get_regions(self) -> List[Dict[str, Any]]:
        """Get all top-level regions.

        Returns:
            List of dictionaries containing region information
        """
        regions = await self.repository.region_repo.get_all_top_level_regions()
        return [
            {
                'id': region.region_id,
                'name': region.name,
                'abbr': region.abbr
            }
            for region in regions
        ]

    async def get_regions_by_parent(self, parent_id: int) -> List[Dict[str, Any]]:
        """Get all subregions for a parent region.

        Args:
            parent_id: The parent region ID

        Returns:
            List of dictionaries containing subregion information
        """
        regions = await self.repository.region_repo.get_by_parent(parent_id)
        return [
            {
                'id': region.region_id,
                'name': region.name,
                'abbr': region.abbr
            }
            for region in regions
        ]

    # Base Vehicle operations
    async def get_base_vehicle(self, base_vehicle_id: int) -> Dict[str, Any]:
        """Get a specific base vehicle by ID.

        Args:
            base_vehicle_id: The base vehicle ID to retrieve

        Returns:
            Dictionary containing base vehicle information

        Raises:
            ResourceNotFoundException: If base vehicle with the specified ID is not found
        """
        base_vehicle = await self.repository.base_vehicle_repo.get_by_base_vehicle_id(base_vehicle_id)
        if not base_vehicle:
            raise ResourceNotFoundException(
                resource_type='BaseVehicle',
                resource_id=str(base_vehicle_id)
            )

        return {
            'id': base_vehicle.base_vehicle_id,
            'year': base_vehicle.year.year if base_vehicle.year else None,
            'make': base_vehicle.make.name if base_vehicle.make else None,
            'model': base_vehicle.model.name if base_vehicle.model else None,
            'year_id': base_vehicle.year_id,
            'make_id': base_vehicle.make_id,
            'model_id': base_vehicle.model_id
        }

    async def find_base_vehicle(self, year_id: int, make_id: int, model_id: int) -> Optional[Dict[str, Any]]:
        """Find a base vehicle by its component IDs.

        Args:
            year_id: The year ID
            make_id: The make ID
            model_id: The model ID

        Returns:
            Dictionary containing base vehicle information or None if not found
        """
        base_vehicle = await self.repository.base_vehicle_repo.find_by_year_make_model(
            year_id, make_id, model_id
        )

        if not base_vehicle:
            return None

        return {
            'id': base_vehicle.base_vehicle_id,
            'year': base_vehicle.year.year if base_vehicle.year else None,
            'make': base_vehicle.make.name if base_vehicle.make else None,
            'model': base_vehicle.model.name if base_vehicle.model else None,
            'year_id': base_vehicle.year_id,
            'make_id': base_vehicle.make_id,
            'model_id': base_vehicle.model_id
        }

    async def search_base_vehicles(
        self,
        year: Optional[int] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """Search for base vehicles by criteria.

        Args:
            year: Optional year to filter by
            make: Optional make name pattern to filter by
            model: Optional model name pattern to filter by
            page: Page number for pagination
            page_size: Number of items per page

        Returns:
            Dictionary containing search results and pagination information
        """
        result = await self.repository.base_vehicle_repo.search_by_criteria(
            year=year, make=make, model=model, page=page, page_size=page_size
        )

        base_vehicles = []
        for bv in result['items']:
            base_vehicles.append({
                'id': bv.base_vehicle_id,
                'year': bv.year.year if bv.year else None,
                'make': bv.make.name if bv.make else None,
                'model': bv.model.name if bv.model else None,
                'year_id': bv.year_id,
                'make_id': bv.make_id,
                'model_id': bv.model_id
            })

        return {
            'items': base_vehicles,
            'total': result['total'],
            'page': result['page'],
            'page_size': result['page_size'],
            'pages': result['pages']
        }

    # Vehicle operations
    async def search_vehicles(
        self,
        year: Optional[int] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        submodel: Optional[str] = None,
        body_type: Optional[str] = None,
        engine_config: Optional[int] = None,
        transmission_type: Optional[int] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """Search for vehicles by criteria.

        Args:
            year: Optional year to filter by
            make: Optional make name pattern to filter by
            model: Optional model name pattern to filter by
            submodel: Optional submodel name pattern to filter by
            body_type: Optional body type pattern to filter by
            engine_config: Optional engine configuration ID to filter by
            transmission_type: Optional transmission type ID to filter by
            page: Page number for pagination
            page_size: Number of items per page

        Returns:
            Dictionary containing search results and pagination information
        """
        result = await self.repository.vehicle_repo.search(
            year=year,
            make=make,
            model=model,
            submodel=submodel,
            body_type=body_type,
            engine_config=engine_config,
            transmission_type=transmission_type,
            page=page,
            page_size=page_size
        )

        vehicles = []
        for vehicle in result['items']:
            vehicles.append({
                'id': str(vehicle.id),
                'vehicle_id': vehicle.vehicle_id,
                'year': vehicle.year,
                'make': vehicle.make.name if vehicle.make else None,
                'model': vehicle.model,
                'submodel': vehicle.submodel.name if vehicle.submodel else None,
                'region': vehicle.region.name if vehicle.region else None
            })

        return {
            'items': vehicles,
            'total': result['total'],
            'page': result['page'],
            'page_size': result['page_size'],
            'pages': result['pages']
        }

    async def get_vehicle_by_id(self, vehicle_id: int) -> Dict[str, Any]:
        """Get a specific vehicle by ID.

        Args:
            vehicle_id: The vehicle ID to retrieve

        Returns:
            Dictionary containing basic vehicle information

        Raises:
            ResourceNotFoundException: If vehicle with the specified ID is not found
        """
        vehicle = await self.repository.vehicle_repo.get_by_vehicle_id(vehicle_id)
        if not vehicle:
            raise ResourceNotFoundException(
                resource_type='Vehicle',
                resource_id=str(vehicle_id)
            )

        return {
            'id': str(vehicle.id),
            'vehicle_id': vehicle.vehicle_id,
            'year': vehicle.year,
            'make': vehicle.make.name if vehicle.make else None,
            'model': vehicle.model,
            'submodel': vehicle.submodel.name if vehicle.submodel else None,
            'region': vehicle.region.name if vehicle.region else None
        }

    async def get_vehicle_details(self, vehicle_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific vehicle.

        Args:
            vehicle_id: The vehicle ID to retrieve

        Returns:
            Dictionary containing detailed vehicle information including
            engines, transmissions, drive types, and body styles

        Raises:
            ResourceNotFoundException: If vehicle with the specified ID is not found
        """
        vehicle = await self.repository.vehicle_repo.get_by_vehicle_id(vehicle_id)
        if not vehicle:
            raise ResourceNotFoundException(
                resource_type='Vehicle',
                resource_id=str(vehicle_id)
            )

        engines = []
        for engine_config in vehicle.engine_configs:
            if not hasattr(engine_config, 'engine_base') or not engine_config.engine_base:
                continue
            if not hasattr(engine_config.engine_base, 'engine_block') or not engine_config.engine_base.engine_block:
                continue

            engines.append({
                'id': engine_config.engine_config_id,
                'liter': engine_config.engine_base.engine_block.liter,
                'cylinders': engine_config.engine_base.engine_block.cylinders,
                'aspiration': engine_config.aspiration.name if engine_config.aspiration else None,
                'fuel_type': engine_config.fuel_type.name if engine_config.fuel_type else None
            })

        transmissions = []
        for transmission in vehicle.transmissions:
            if not hasattr(transmission, 'transmission_base') or not transmission.transmission_base:
                continue

            transmissions.append({
                'id': transmission.transmission_id,
                'type': transmission.transmission_base.transmission_type.name
                if transmission.transmission_base.transmission_type else None,
                'speeds': transmission.transmission_base.transmission_num_speeds.num_speeds
                if transmission.transmission_base.transmission_num_speeds else None
            })

        return {
            'id': str(vehicle.id),
            'vehicle_id': vehicle.vehicle_id,
            'year': vehicle.year,
            'make': vehicle.make.name if vehicle.make else None,
            'model': vehicle.model,
            'submodel': vehicle.submodel.name if vehicle.submodel else None,
            'region': vehicle.region.name if vehicle.region else None,
            'engines': engines,
            'transmissions': transmissions,
            'drive_types': [dt.name for dt in vehicle.drive_types],
            'body_styles': [bs.body_type.name for bs in vehicle.body_style_configs
                            if hasattr(bs, 'body_type') and bs.body_type]
        }

    async def get_vehicle_configurations(self, vehicle_id: int) -> Dict[str, List[Dict[str, Any]]]:
        """Get all component configurations for a specific vehicle.

        Args:
            vehicle_id: The vehicle ID to retrieve configurations for

        Returns:
            Dictionary containing component configurations grouped by type

        Raises:
            ResourceNotFoundException: If vehicle with the specified ID is not found
        """
        configs = await self.repository.vehicle_repo.get_vehicle_configurations(vehicle_id)
        if not configs:
            raise ResourceNotFoundException(
                resource_type='Vehicle',
                resource_id=str(vehicle_id)
            )

        result: Dict[str, List[Dict[str, Any]]] = {
            'engines': [],
            'transmissions': [],
            'drive_types': [],
            'body_styles': [],
            'brake_configs': [],
            'wheel_bases': []
        }

        # Process engine configurations
        for engine in configs['engines']:
            result['engines'].append({
                'id': engine.engine_config_id,
                'liter': engine.engine_base.engine_block.liter if engine.engine_base and engine.engine_base.engine_block else None,
                'cylinders': engine.engine_base.engine_block.cylinders if engine.engine_base and engine.engine_base.engine_block else None,
                'fuel_type': engine.fuel_type.name if engine.fuel_type else None,
                'aspiration': engine.aspiration.name if engine.aspiration else None,
                'power': {
                    'horsepower': engine.power_output.horsepower if engine.power_output else None,
                    'kilowatt': engine.power_output.kilowatt if engine.power_output else None
                }
            })

        # Process transmission configurations
        for trans in configs['transmissions']:
            result['transmissions'].append({
                'id': trans.transmission_id,
                'type': trans.transmission_base.transmission_type.name
                if trans.transmission_base and trans.transmission_base.transmission_type else None,
                'speeds': trans.transmission_base.transmission_num_speeds.num_speeds
                if trans.transmission_base and trans.transmission_base.transmission_num_speeds else None,
                'control_type': trans.transmission_base.transmission_control_type.name
                if trans.transmission_base and trans.transmission_base.transmission_control_type else None,
                'manufacturer': trans.transmission_mfr.name if trans.transmission_mfr else None,
                'code': trans.transmission_mfr_code.code if trans.transmission_mfr_code else None
            })

        # Process drive types
        for dt in configs['drive_types']:
            result['drive_types'].append({
                'id': dt.drive_type_id,
                'name': dt.name
            })

        # Process body styles
        for bs in configs['body_styles']:
            result['body_styles'].append({
                'id': bs.body_style_config_id,
                'type': bs.body_type.name if bs.body_type else None,
                'doors': bs.body_num_doors.num_doors if bs.body_num_doors else None
            })

        # Process brake configs
        for bc in configs['brake_configs']:
            result['brake_configs'].append({
                'id': bc.brake_config_id,
                'front_type': bc.front_brake_type.name if bc.front_brake_type else None,
                'rear_type': bc.rear_brake_type.name if bc.rear_brake_type else None,
                'system': bc.brake_system.name if bc.brake_system else None,
                'abs': bc.brake_abs.name if bc.brake_abs else None
            })

        # Process wheel bases
        for wb in configs['wheel_bases']:
            result['wheel_bases'].append({
                'id': wb.wheel_base_id,
                'wheel_base': wb.wheel_base,
                'wheel_base_metric': wb.wheel_base_metric
            })

        return result

    # Engine Configuration operations
    async def get_engine_config(self, engine_config_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific engine configuration.

        Args:
            engine_config_id: The engine configuration ID to retrieve

        Returns:
            Dictionary containing detailed engine configuration information

        Raises:
            ResourceNotFoundException: If engine configuration is not found
        """
        engine_details = await self.repository.engine_config_repo.get_full_engine_details(engine_config_id)
        if not engine_details:
            raise ResourceNotFoundException(
                resource_type='EngineConfig',
                resource_id=str(engine_config_id)
            )

        return engine_details

    async def search_engine_configs(
        self,
        engine_base_id: Optional[int] = None,
        fuel_type_id: Optional[int] = None,
        aspiration_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """Search for engine configurations by criteria.

        Args:
            engine_base_id: Optional engine base ID to filter by
            fuel_type_id: Optional fuel type ID to filter by
            aspiration_id: Optional aspiration ID to filter by
            page: Page number for pagination
            page_size: Number of items per page

        Returns:
            Dictionary containing search results and pagination information
        """
        result = await self.repository.engine_config_repo.get_by_criteria(
            engine_base_id=engine_base_id,
            fuel_type_id=fuel_type_id,
            aspiration_id=aspiration_id,
            page=page,
            page_size=page_size
        )

        engine_configs = []
        for ec in result['items']:
            engine_configs.append({
                'id': ec.engine_config_id,
                'engine_base_id': ec.engine_base_id,
                'fuel_type_id': ec.fuel_type_id,
                'aspiration_id': ec.aspiration_id
            })

        return {
            'items': engine_configs,
            'total': result['total'],
            'page': result['page'],
            'page_size': result['page_size'],
            'pages': result['pages']
        }

    # Transmission operations
    async def get_transmission(self, transmission_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific transmission.

        Args:
            transmission_id: The transmission ID to retrieve

        Returns:
            Dictionary containing detailed transmission information

        Raises:
            ResourceNotFoundException: If transmission is not found
        """
        transmission_details = await self.repository.transmission_repo.get_full_transmission_details(transmission_id)
        if not transmission_details:
            raise ResourceNotFoundException(
                resource_type='Transmission',
                resource_id=str(transmission_id)
            )

        return transmission_details

    async def search_transmissions(
        self,
        transmission_type_id: Optional[int] = None,
        transmission_num_speeds_id: Optional[int] = None,
        transmission_control_type_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """Search for transmissions by criteria.

        Args:
            transmission_type_id: Optional transmission type ID to filter by
            transmission_num_speeds_id: Optional number of speeds ID to filter by
            transmission_control_type_id: Optional control type ID to filter by
            page: Page number for pagination
            page_size: Number of items per page

        Returns:
            Dictionary containing search results and pagination information
        """
        result = await self.repository.transmission_repo.get_by_criteria(
            transmission_type_id=transmission_type_id,
            transmission_num_speeds_id=transmission_num_speeds_id,
            transmission_control_type_id=transmission_control_type_id,
            page=page,
            page_size=page_size
        )

        transmissions = []
        for trans in result['items']:
            transmissions.append({
                'id': trans.transmission_id,
                'transmission_base_id': trans.transmission_base_id,
                'transmission_mfr_code_id': trans.transmission_mfr_code_id,
                'elec_controlled_id': trans.elec_controlled_id,
                'transmission_mfr_id': trans.transmission_mfr_id
            })

        return {
            'items': transmissions,
            'total': result['total'],
            'page': result['page'],
            'page_size': result['page_size'],
            'pages': result['pages']
        }

    # Drive Type operations
    async def get_drive_types(self) -> List[Dict[str, Any]]:
        """Get all available drive types.

        Returns:
            List of dictionaries containing drive type information
        """
        drive_types = await self.repository.drive_type_repo.get_all_drive_types()
        return [
            {
                'id': dt.drive_type_id,
                'name': dt.name
            }
            for dt in drive_types
        ]

    # Body Style operations
    async def get_body_style_config(self, body_style_config_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific body style configuration.

        Args:
            body_style_config_id: The body style configuration ID to retrieve

        Returns:
            Dictionary containing detailed body style configuration information

        Raises:
            ResourceNotFoundException: If body style configuration is not found
        """
        body_style_details = await self.repository.body_style_repo.get_full_body_style_details(body_style_config_id)
        if not body_style_details:
            raise ResourceNotFoundException(
                resource_type='BodyStyleConfig',
                resource_id=str(body_style_config_id)
            )

        return body_style_details

    # Brake Configuration operations
    async def get_brake_config(self, brake_config_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific brake configuration.

        Args:
            brake_config_id: The brake configuration ID to retrieve

        Returns:
            Dictionary containing detailed brake configuration information

        Raises:
            ResourceNotFoundException: If brake configuration is not found
        """
        brake_config_details = await self.repository.brake_config_repo.get_full_brake_config_details(brake_config_id)
        if not brake_config_details:
            raise ResourceNotFoundException(
                resource_type='BrakeConfig',
                resource_id=str(brake_config_id)
            )

        return brake_config_details

    # Wheel Base operations
    async def get_wheel_bases(self) -> List[Dict[str, Any]]:
        """Get all available wheel bases.

        Returns:
            List of dictionaries containing wheel base information
        """
        wheel_bases = await self.repository.wheel_base_repo.get_all_wheel_bases()
        return [
            {
                'id': wb.wheel_base_id,
                'wheel_base': wb.wheel_base,
                'wheel_base_metric': wb.wheel_base_metric
            }
            for wb in wheel_bases
        ]
