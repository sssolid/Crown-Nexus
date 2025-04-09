from __future__ import annotations

"""VCdb repository implementation.

This module provides data access and persistence operations for VCdb entities.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.repositories.base import BaseRepository
from app.domains.autocare.vcdb.models import (
    Vehicle,
    BaseVehicle,
    Make,
    Model,
    Year,
    SubModel,
    VehicleType,
    Region,
    VCdbVersion,
    DriveType,
    BrakeType,
    BrakeSystem,
    BrakeABS,
    BrakeConfig,
    BodyType,
    BodyNumDoors,
    BodyStyleConfig,
    EngineBlock,
    EngineBoreStroke,
    EngineBase,
    EngineBase2,
    Aspiration,
    FuelType,
    CylinderHeadType,
    FuelDeliveryType,
    FuelDeliverySubType,
    FuelSystemControlType,
    FuelSystemDesign,
    FuelDeliveryConfig,
    EngineDesignation,
    EngineVIN,
    EngineVersion,
    Valves,
    Mfr,
    IgnitionSystemType,
    PowerOutput,
    EngineConfig,
    EngineConfig2,
    TransmissionType,
    TransmissionNumSpeeds,
    TransmissionControlType,
    TransmissionBase,
    TransmissionMfrCode,
    ElecControlled,
    Transmission,
    WheelBase,
)


class VCdbRepository:
    """Repository for VCdb entity operations.

    Provides methods for querying VCdb data and managing database updates.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the VCdb repository.

        Args:
            db: The database session.
        """
        self.db = db
        self.vehicle_repo = VehicleRepository(db)
        self.base_vehicle_repo = BaseVehicleRepository(db)
        self.make_repo = MakeRepository(db)
        self.model_repo = ModelRepository(db)
        self.year_repo = YearRepository(db)
        self.submodel_repo = SubModelRepository(db)
        self.vehicle_type_repo = VehicleTypeRepository(db)
        self.region_repo = RegionRepository(db)
        self.engine_config_repo = EngineConfigRepository(db)
        self.transmission_repo = TransmissionRepository(db)
        self.drive_type_repo = DriveTypeRepository(db)
        self.body_style_repo = BodyStyleConfigRepository(db)
        self.brake_config_repo = BrakeConfigRepository(db)
        self.wheel_base_repo = WheelBaseRepository(db)

    async def get_version(self) -> Optional[str]:
        """Get the current version of the VCdb database.

        Returns:
            The version date as a string or None if no version is set.
        """
        query = select(VCdbVersion).where(VCdbVersion.is_current == True)
        result = await self.db.execute(query)
        version = result.scalars().first()

        if version:
            return version.version_date.strftime("%Y-%m-%d")
        return None

    async def update_version(self, version_date: datetime) -> VCdbVersion:
        """Update the current version of the VCdb database.

        Args:
            version_date: The new version date.

        Returns:
            The updated version entity.
        """
        # Set all existing versions to not current
        update_query = select(VCdbVersion).where(VCdbVersion.is_current == True)
        result = await self.db.execute(update_query)
        old_versions = result.scalars().all()

        for version in old_versions:
            version.is_current = False

        # Create new current version
        version = VCdbVersion(version_date=version_date, is_current=True)
        self.db.add(version)
        await self.db.flush()

        return version


class VehicleRepository(BaseRepository[Vehicle, uuid.UUID]):
    """Repository for Vehicle entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the vehicle repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Vehicle, db=db)

    async def get_by_vehicle_id(self, vehicle_id: int) -> Optional[Vehicle]:
        """Get a vehicle by its VCdb ID.

        Args:
            vehicle_id: The vehicle ID.

        Returns:
            The vehicle if found, None otherwise.
        """
        query = select(Vehicle).where(Vehicle.vehicle_id == vehicle_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def search(
        self,
        year: Optional[int] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        submodel: Optional[str] = None,
        body_type: Optional[str] = None,
        engine_config: Optional[int] = None,
        transmission_type: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Search for vehicles with optional filters.

        Args:
            year: Optional vehicle year to filter by.
            make: Optional make name to filter by.
            model: Optional model name to filter by.
            submodel: Optional submodel name to filter by.
            body_type: Optional body type name to filter by.
            engine_config: Optional engine configuration ID to filter by.
            transmission_type: Optional transmission type ID to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        # Start with a join to get the related entities
        query = (
            select(Vehicle)
            .join(BaseVehicle, Vehicle.base_vehicle_id == BaseVehicle.base_vehicle_id)
            .join(Year, BaseVehicle.year_id == Year.year_id)
            .join(Make, BaseVehicle.make_id == Make.make_id)
            .join(Model, BaseVehicle.model_id == Model.model_id)
            .join(SubModel, Vehicle.submodel_id == SubModel.submodel_id)
            .options(
                selectinload(Vehicle.base_vehicle)
                .selectinload(BaseVehicle.make),
                selectinload(Vehicle.base_vehicle)
                .selectinload(BaseVehicle.year),
                selectinload(Vehicle.base_vehicle)
                .selectinload(BaseVehicle.model),
                selectinload(Vehicle.submodel),
                selectinload(Vehicle.region),
            )

        )

        # Add filters
        conditions = []

        if year:
            conditions.append(Year.year_id == year)

        if make:
            conditions.append(Make.name.ilike(f"%{make}%"))

        if model:
            conditions.append(Model.name.ilike(f"%{model}%"))

        if submodel:
            conditions.append(SubModel.name.ilike(f"%{submodel}%"))

        if body_type:
            # Add join for body type
            query = query.join(
                Vehicle.body_style_configs
            ).join(BodyType, BodyStyleConfig.body_type_id == BodyType.body_type_id)
            conditions.append(BodyType.name.ilike(f"%{body_type}%"))

        if engine_config:
            # Add join for engine config
            query = query.join(Vehicle.engine_configs)
            conditions.append(EngineConfig2.engine_config_id == engine_config)

        if transmission_type:
            # Add join for transmission
            query = query.join(Vehicle.transmissions).join(TransmissionBase)
            conditions.append(TransmissionBase.transmission_type_id == transmission_type)

        if conditions:
            query = query.where(and_(*conditions))

        # Order by latest year, then make, then model
        query = query.order_by(desc(Year.year_id), Make.name, Model.name)

        return await self.paginate(query, page, page_size)

    async def get_submodels_by_base_vehicle(
        self, base_vehicle_id: int
    ) -> List[SubModel]:
        """Get submodels available for a specific base vehicle.

        Args:
            base_vehicle_id: Base vehicle ID.

        Returns:
            List of submodels for the base vehicle.
        """
        query = (
            select(SubModel)
            .join(Vehicle, SubModel.submodel_id == Vehicle.submodel_id)
            .where(Vehicle.base_vehicle_id == base_vehicle_id)
            .distinct()
            .order_by(SubModel.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_vehicle_configurations(self, vehicle_id: int) -> Dict[str, List[Any]]:
        """Get all configurations for a specific vehicle.

        Args:
            vehicle_id: Vehicle ID.

        Returns:
            Dict containing lists of configurations by type.
        """
        vehicle_query = (
            select(Vehicle)
            .where(Vehicle.vehicle_id == vehicle_id)
            .options(selectinload(Vehicle.engine_configs))
        )
        result = await self.db.execute(vehicle_query)
        vehicle = result.scalars().first()

        if not vehicle:
            return {
                "engines": [],
                "transmissions": [],
                "drive_types": [],
                "body_styles": [],
                "brake_configs": [],
                "wheel_bases": [],
            }

        # Engines
        engine_config_ids = [ec.engine_config_id for ec in vehicle.engine_configs]

        engine_query = (
            select(EngineConfig2)
            .join(EngineBase2, EngineConfig2.engine_base_id == EngineBase2.engine_base_id)
            .join(EngineBlock, EngineBase2.engine_block_id == EngineBlock.engine_block_id)
            .join(FuelType, EngineConfig2.fuel_type_id == FuelType.fuel_type_id)
            .join(Aspiration, EngineConfig2.aspiration_id == Aspiration.aspiration_id)
            .where(EngineConfig2.engine_config_id.in_(engine_config_ids))
            .options(
                selectinload(EngineConfig2.engine_base),
                selectinload(EngineConfig2.engine_block),
                selectinload(EngineConfig2.fuel_type),
                selectinload(EngineConfig2.aspiration),
            )
        )

        engines_result = await self.db.execute(engine_query)
        engines = engines_result.unique().all()

        # Transmissions
        transmission_query = (
            select(Transmission)
            .join(
                TransmissionBase,
                Transmission.transmission_base_id
                == TransmissionBase.transmission_base_id,
            )
            .join(
                TransmissionType,
                TransmissionBase.transmission_type_id
                == TransmissionType.transmission_type_id,
            )
            .join(
                TransmissionNumSpeeds,
                TransmissionBase.transmission_num_speeds_id
                == TransmissionNumSpeeds.transmission_num_speeds_id,
            )
            .where(
                Transmission.transmission_id.in_(
                    [t.transmission_id for t in vehicle.transmissions]
                )
            )
        )

        transmissions_result = await self.db.execute(transmission_query)
        transmissions = transmissions_result.unique().all()

        # Return all configurations
        return {
            "engines": engines,
            "transmissions": transmissions,
            "drive_types": vehicle.drive_types,
            "body_styles": vehicle.body_style_configs,
            "brake_configs": vehicle.brake_configs,
            "wheel_bases": vehicle.wheel_bases,
        }


class BaseVehicleRepository(BaseRepository[BaseVehicle, uuid.UUID]):
    """Repository for BaseVehicle entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the base vehicle repository.

        Args:
            db: The database session.
        """
        super().__init__(model=BaseVehicle, db=db)

    async def get_by_base_vehicle_id(
        self, base_vehicle_id: int
    ) -> Optional[BaseVehicle]:
        """Get a base vehicle by its VCdb ID.

        Args:
            base_vehicle_id: The base vehicle ID.

        Returns:
            The base vehicle if found, None otherwise.
        """
        query = select(BaseVehicle).where(
            BaseVehicle.base_vehicle_id == base_vehicle_id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_year_make_model(
        self, year_id: int, make_id: int, model_id: int
    ) -> Optional[BaseVehicle]:
        """Find a base vehicle by year, make, and model IDs.

        Args:
            year_id: Year ID.
            make_id: Make ID.
            model_id: Model ID.

        Returns:
            The base vehicle if found, None otherwise.
        """
        query = select(BaseVehicle).where(
            BaseVehicle.year_id == year_id,
            BaseVehicle.make_id == make_id,
            BaseVehicle.model_id == model_id,
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def search_by_criteria(
        self,
        year: Optional[int] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Search for base vehicles by various criteria.

        Args:
            year: Optional year to filter by.
            make: Optional make name to filter by.
            model: Optional model name to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        # Join with related entities
        query = (
            select(BaseVehicle)
            .join(Year, BaseVehicle.year_id == Year.year_id)
            .join(Make, BaseVehicle.make_id == Make.make_id)
            .join(Model, BaseVehicle.model_id == Model.model_id)
        )

        # Add filters
        conditions = []

        if year:
            conditions.append(Year.year_id == year)

        if make:
            conditions.append(Make.name.ilike(f"%{make}%"))

        if model:
            conditions.append(Model.name.ilike(f"%{model}%"))

        if conditions:
            query = query.where(and_(*conditions))

        # Order by latest year, then make, then model
        query = query.order_by(desc(Year.year_id), Make.name, Model.name)

        return await self.paginate(query, page, page_size)


class MakeRepository(BaseRepository[Make, uuid.UUID]):
    """Repository for Make entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the make repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Make, db=db)

    async def get_by_make_id(self, make_id: int) -> Optional[Make]:
        """Get a make by its VCdb ID.

        Args:
            make_id: The make ID.

        Returns:
            The make if found, None otherwise.
        """
        query = select(Make).where(Make.make_id == make_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def search_by_name(self, name: str) -> List[Make]:
        """Search makes by name.

        Args:
            name: The make name to search for.

        Returns:
            List of makes matching the search.
        """
        query = select(Make).where(Make.name.ilike(f"%{name}%")).order_by(Make.name)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_year(self, year: int) -> List[Make]:
        """Get all makes available for a specific year.

        Args:
            year: Vehicle year.

        Returns:
            List of makes available for the year.
        """
        query = (
            select(Make)
            .join(BaseVehicle, Make.make_id == BaseVehicle.make_id)
            .join(Year, BaseVehicle.year_id == Year.year_id)
            .where(Year.year_id == year)
            .distinct()
            .order_by(Make.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_makes(self) -> List[Make]:
        """Get all makes.

        Returns:
            List of all makes.
        """
        query = select(Make).order_by(Make.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())


class ModelRepository(BaseRepository[Model, uuid.UUID]):
    """Repository for Model entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the model repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Model, db=db)

    async def get_by_model_id(self, model_id: int) -> Optional[Model]:
        """Get a model by its VCdb ID.

        Args:
            model_id: The model ID.

        Returns:
            The model if found, None otherwise.
        """
        query = select(Model).where(Model.model_id == model_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def search_by_name(self, name: str) -> List[Model]:
        """Search models by name.

        Args:
            name: The model name to search for.

        Returns:
            List of models matching the search.
        """
        query = select(Model).where(Model.name.ilike(f"%{name}%")).order_by(Model.name)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_year_make(self, year: int, make_id: int) -> List[Model]:
        """Get all models available for a specific year and make.

        Args:
            year: Vehicle year.
            make_id: Make ID.

        Returns:
            List of models available for the year and make.
        """
        query = (
            select(Model)
            .join(BaseVehicle, Model.model_id == BaseVehicle.model_id)
            .join(Year, BaseVehicle.year_id == Year.year_id)
            .where(Year.year_id == year, BaseVehicle.make_id == make_id)
            .options(selectinload(Model.vehicle_type))
            .distinct()
            .order_by(Model.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_vehicle_type(self, vehicle_type_id: int) -> List[Model]:
        """Get models for a specific vehicle type.

        Args:
            vehicle_type_id: Vehicle type ID.

        Returns:
            List of models for the vehicle type.
        """
        query = (
            select(Model)
            .where(Model.vehicle_type_id == vehicle_type_id)
            .order_by(Model.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())


class YearRepository(BaseRepository[Year, uuid.UUID]):
    """Repository for Year entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the year repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Year, db=db)

    async def get_by_year_id(self, year_id: int) -> Optional[Year]:
        """Get a year by its VCdb ID.

        Args:
            year_id: The year ID.

        Returns:
            The year if found, None otherwise.
        """
        query = select(Year).where(Year.year_id == year_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_year(self, year: int) -> Optional[Year]:
        """Get a year entity by the year value.

        Args:
            year: The year value.

        Returns:
            The year entity if found, None otherwise.
        """
        query = select(Year).where(Year.year_id == year)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all_years(self) -> List[Year]:
        """Get all available years.

        Returns:
            List of all year entities.
        """
        query = select(Year).order_by(desc(Year.year_id))
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_year_range(self) -> Tuple[int, int]:
        """Get the minimum and maximum years in the database.

        Returns:
            Tuple containing (min_year, max_year).
        """
        min_query = select(func.min(Year.year_id))
        max_query = select(func.max(Year.year_id))

        min_result = await self.db.execute(min_query)
        max_result = await self.db.execute(max_query)

        min_year = min_result.scalar() or datetime.now().year
        max_year = max_result.scalar() or datetime.now().year

        return min_year, max_year


class SubModelRepository(BaseRepository[SubModel, uuid.UUID]):
    """Repository for SubModel entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the submodel repository.

        Args:
            db: The database session.
        """
        super().__init__(model=SubModel, db=db)

    async def get_by_submodel_id(self, submodel_id: int) -> Optional[SubModel]:
        """Get a submodel by its VCdb ID.

        Args:
            submodel_id: The submodel ID.

        Returns:
            The submodel if found, None otherwise.
        """
        query = select(SubModel).where(SubModel.submodel_id == submodel_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def search_by_name(self, name: str) -> List[SubModel]:
        """Search submodels by name.

        Args:
            name: The submodel name to search for.

        Returns:
            List of submodels matching the search.
        """
        query = (
            select(SubModel)
            .where(SubModel.name.ilike(f"%{name}%"))
            .order_by(SubModel.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_submodels(self) -> List[SubModel]:
        """Get all submodels.

        Returns:
            List of all submodels.
        """
        query = select(SubModel).order_by(SubModel.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())


class VehicleTypeRepository(BaseRepository[VehicleType, uuid.UUID]):
    """Repository for VehicleType entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the vehicle type repository.

        Args:
            db: The database session.
        """
        super().__init__(model=VehicleType, db=db)

    async def get_by_vehicle_type_id(
        self, vehicle_type_id: int
    ) -> Optional[VehicleType]:
        """Get a vehicle type by its VCdb ID.

        Args:
            vehicle_type_id: The vehicle type ID.

        Returns:
            The vehicle type if found, None otherwise.
        """
        query = select(VehicleType).where(
            VehicleType.vehicle_type_id == vehicle_type_id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_group(self, vehicle_type_group_id: int) -> List[VehicleType]:
        """Get vehicle types by group.

        Args:
            vehicle_type_group_id: The vehicle type group ID.

        Returns:
            List of vehicle types in the group.
        """
        query = (
            select(VehicleType)
            .where(VehicleType.vehicle_type_group_id == vehicle_type_group_id)
            .order_by(VehicleType.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_vehicle_types(self) -> List[VehicleType]:
        """Get all vehicle types.

        Returns:
            List of all vehicle types.
        """
        query = select(VehicleType).order_by(VehicleType.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())


class RegionRepository(BaseRepository[Region, uuid.UUID]):
    """Repository for Region entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the region repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Region, db=db)

    async def get_by_region_id(self, region_id: int) -> Optional[Region]:
        """Get a region by its VCdb ID.

        Args:
            region_id: The region ID.

        Returns:
            The region if found, None otherwise.
        """
        query = select(Region).where(Region.region_id == region_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_parent(self, parent_id: int) -> List[Region]:
        """Get regions by parent.

        Args:
            parent_id: The parent region ID.

        Returns:
            List of regions with the specified parent.
        """
        query = (
            select(Region).where(Region.parent_id == parent_id).order_by(Region.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_top_level_regions(self) -> List[Region]:
        """Get all top-level regions (no parent).

        Returns:
            List of all top-level regions.
        """
        query = select(Region).where(Region.parent_id == None).order_by(Region.name)

        result = await self.db.execute(query)
        return list(result.scalars().all())


class EngineConfigRepository(BaseRepository[EngineConfig2, uuid.UUID]):
    """Repository for EngineConfig entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the engine config repository.

        Args:
            db: The database session.
        """
        super().__init__(model=EngineConfig2, db=db)

    async def get_by_engine_config_id(
        self, engine_config_id: int
    ) -> Optional[EngineConfig2]:
        """Get an engine configuration by its VCdb ID.

        Args:
            engine_config_id: The engine config ID.

        Returns:
            The engine config if found, None otherwise.
        """
        query = select(EngineConfig2).where(
            EngineConfig2.engine_config_id == engine_config_id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_criteria(
        self,
        engine_base_id: Optional[int] = None,
        fuel_type_id: Optional[int] = None,
        aspiration_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Get engine configurations by various criteria.

        Args:
            engine_base_id: Optional engine base ID to filter by.
            fuel_type_id: Optional fuel type ID to filter by.
            aspiration_id: Optional aspiration ID to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = select(EngineConfig2)

        # Add filters
        conditions = []

        if engine_base_id:
            conditions.append(EngineConfig2.engine_base_id == engine_base_id)

        if fuel_type_id:
            conditions.append(EngineConfig2.fuel_type_id == fuel_type_id)

        if aspiration_id:
            conditions.append(EngineConfig2.aspiration_id == aspiration_id)

        if conditions:
            query = query.where(and_(*conditions))

        return await self.paginate(query, page, page_size)

    async def get_full_engine_details(self, engine_config_id: int) -> Dict[str, Any]:
        """Get full details for an engine configuration.

        Args:
            engine_config_id: The engine config ID.

        Returns:
            Dict with detailed engine information.
        """
        # Get the engine config with all related entities
        query = (
            select(EngineConfig2)
            .options(
                selectinload(EngineConfig2.engine_base),
                selectinload(EngineConfig2.engine_block),
                selectinload(EngineConfig2.engine_bore_stroke),
                selectinload(EngineConfig2.aspiration),
                selectinload(EngineConfig2.fuel_type),
                selectinload(EngineConfig2.cylinder_head_type),
                selectinload(EngineConfig2.fuel_delivery_config),
                selectinload(EngineConfig2.engine_designation),
                selectinload(EngineConfig2.engine_vin),
                selectinload(EngineConfig2.valves),
                selectinload(EngineConfig2.engine_mfr),
                selectinload(EngineConfig2.ignition_system_type),
                selectinload(EngineConfig2.engine_version),
                selectinload(EngineConfig2.power_output),
                selectinload(EngineConfig2.fuel_delivery_config).selectinload(
                    FuelDeliveryConfig.fuel_delivery_type
                ),
                selectinload(EngineConfig2.fuel_delivery_config).selectinload(
                    FuelDeliveryConfig.fuel_delivery_subtype
                ),
                selectinload(EngineConfig2.fuel_delivery_config).selectinload(
                    FuelDeliveryConfig.fuel_system_control_type
                ),
                selectinload(EngineConfig2.fuel_delivery_config).selectinload(
                    FuelDeliveryConfig.fuel_system_design
                ),
            )
            .where(EngineConfig2.engine_config_id == engine_config_id)
        )

        result = await self.db.execute(query)
        engine_config = result.scalars().first()

        if not engine_config:
            return {}

        # Construct the detailed response
        return {
            "engine_config": {
                "id": engine_config.engine_config_id,
                "engine_base_id": engine_config.engine_base_id,
                "engine_designation_id": engine_config.engine_designation_id,
                "engine_vin_id": engine_config.engine_vin_id,
                "valves_id": engine_config.valves_id,
                "fuel_delivery_config_id": engine_config.fuel_delivery_config_id,
                "aspiration_id": engine_config.aspiration_id,
                "cylinder_head_type_id": engine_config.cylinder_head_type_id,
                "fuel_type_id": engine_config.fuel_type_id,
                "ignition_system_type_id": engine_config.ignition_system_type_id,
                "engine_mfr_id": engine_config.engine_mfr_id,
                "engine_version_id": engine_config.engine_version_id,
                "power_output_id": engine_config.power_output_id,
            },
            "engine_block": {
                "id": engine_config.engine_block.engine_block_id if engine_config.engine_block else None,
                "liter": engine_config.engine_block.liter if engine_config.engine_block else None,
                "cc": engine_config.engine_block.cc if engine_config.engine_block else None,
                "cid": engine_config.engine_block.cid if engine_config.engine_block else None,
                "cylinders": engine_config.engine_block.cylinders if engine_config.engine_block else None,
                "block_type": engine_config.engine_block.block_type if engine_config.engine_block else None,
            },
            "engine_bore_stroke": {
                "id": engine_config.engine_bore_stroke.engine_bore_stroke_id if engine_config.engine_bore_stroke else None,
                "bore_in": engine_config.engine_bore_stroke.bore_in if engine_config.engine_bore_stroke else None,
                "bore_metric": engine_config.engine_bore_stroke.bore_metric if engine_config.engine_bore_stroke else None,
                "stroke_in": engine_config.engine_bore_stroke.stroke_in if engine_config.engine_bore_stroke else None,
                "stroke_metric": engine_config.engine_bore_stroke.stroke_metric if engine_config.engine_bore_stroke else None,
            },
            "aspiration": {"id": engine_config.aspiration.aspiration_id,
                           "name": engine_config.aspiration.name} if engine_config.aspiration else None,
            "fuel_type": {"id": engine_config.fuel_type.fuel_type_id,
                          "name": engine_config.fuel_type.name} if engine_config.fuel_type else None,
            "cylinder_head_type": {
                "id": engine_config.cylinder_head_type.cylinder_head_type_id,
                "name": engine_config.cylinder_head_type.name,
            } if engine_config.cylinder_head_type else None,
            "fuel_delivery": {
                "type": engine_config.fuel_delivery_config.fuel_delivery_type.name
                    if engine_config.fuel_delivery_config and engine_config.fuel_delivery_config.fuel_delivery_type else None,
                "subtype": engine_config.fuel_delivery_config.fuel_delivery_subtype.name
                    if engine_config.fuel_delivery_config and engine_config.fuel_delivery_config.fuel_delivery_subtype else None,
                "control_type": engine_config.fuel_delivery_config.fuel_system_control_type.name
                    if engine_config.fuel_delivery_config and engine_config.fuel_delivery_config.fuel_system_control_type else None,
                "design": engine_config.fuel_delivery_config.fuel_system_design.name
                    if engine_config.fuel_delivery_config and engine_config.fuel_delivery_config.fuel_system_design else None,
            },
            "engine_designation": {
                "id": engine_config.engine_designation.engine_designation_id,
                "name": engine_config.engine_designation.name,
            } if engine_config.engine_designation else None,
            "engine_vin": {"id": engine_config.engine_vin.engine_vin_id,
                           "code": engine_config.engine_vin.code} if engine_config.engine_vin else None,
            "valves": {
                "id": engine_config.valves.valves_id,
                "valves_per_engine": engine_config.valves.valves_per_engine,
            } if engine_config.valves else None,
            "manufacturer": {"id": engine_config.engine_mfr.mfr_id,
                            "name": engine_config.engine_mfr.name} if engine_config.engine_mfr else None,
            "ignition_system_type": {
                "id": engine_config.ignition_system_type.ignition_system_type_id,
                "name": engine_config.ignition_system_type.name,
            } if engine_config.ignition_system_type else None,
            "engine_version": {
                "id": engine_config.engine_version.engine_version_id,
                "version": engine_config.engine_version.version,
            } if engine_config.engine_version else None,
            "power_output": {
                "id": engine_config.power_output.power_output_id,
                "horsepower": engine_config.power_output.horsepower,
                "kilowatt": engine_config.power_output.kilowatt,
            } if engine_config.power_output else None,
        }


class TransmissionRepository(BaseRepository[Transmission, uuid.UUID]):
    """Repository for Transmission entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the transmission repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Transmission, db=db)

    async def get_by_transmission_id(
        self, transmission_id: int
    ) -> Optional[Transmission]:
        """Get a transmission by its VCdb ID.

        Args:
            transmission_id: The transmission ID.

        Returns:
            The transmission if found, None otherwise.
        """
        query = select(Transmission).where(
            Transmission.transmission_id == transmission_id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_criteria(
        self,
        transmission_type_id: Optional[int] = None,
        transmission_num_speeds_id: Optional[int] = None,
        transmission_control_type_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Get transmissions by various criteria.

        Args:
            transmission_type_id: Optional transmission type ID to filter by.
            transmission_num_speeds_id: Optional number of speeds ID to filter by.
            transmission_control_type_id: Optional control type ID to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        # Join with TransmissionBase to access type, speeds, and control type
        query = select(Transmission).join(
            TransmissionBase,
            Transmission.transmission_base_id == TransmissionBase.transmission_base_id,
        )

        # Add filters
        conditions = []

        if transmission_type_id:
            conditions.append(
                TransmissionBase.transmission_type_id == transmission_type_id
            )

        if transmission_num_speeds_id:
            conditions.append(
                TransmissionBase.transmission_num_speeds_id
                == transmission_num_speeds_id
            )

        if transmission_control_type_id:
            conditions.append(
                TransmissionBase.transmission_control_type_id
                == transmission_control_type_id
            )

        if conditions:
            query = query.where(and_(*conditions))

        return await self.paginate(query, page, page_size)

    async def get_full_transmission_details(
        self, transmission_id: int
    ) -> Dict[str, Any]:
        """Get full details for a transmission.

        Args:
            transmission_id: The transmission ID.

        Returns:
            Dict with detailed transmission information.
        """
        # Get the transmission with all related entities
        query = (
            select(Transmission)
            .options(
                selectinload(Transmission.transmission_base)
                .selectinload(TransmissionBase.transmission_type),
                selectinload(Transmission.transmission_base)
                .selectinload(TransmissionBase.transmission_num_speeds),
                selectinload(Transmission.transmission_base)
                .selectinload(TransmissionBase.transmission_control_type),
                selectinload(Transmission.transmission_mfr_code),
                selectinload(Transmission.elec_controlled),
                selectinload(Transmission.transmission_mfr),
            )
            .where(Transmission.transmission_id == transmission_id)
        )

        result = await self.db.execute(query)
        transmission = result.scalars().first()

        if not transmission:
            return {}

        # Construct the detailed response
        return {
            "transmission": {
                "id": transmission.transmission_id,
                "transmission_base_id": transmission.transmission_base_id,
                "transmission_mfr_code_id": transmission.transmission_mfr_code_id,
                "elec_controlled_id": transmission.elec_controlled_id,
                "transmission_mfr_id": transmission.transmission_mfr_id,
            },
            "type": {
                "id": transmission.transmission_base.transmission_type.transmission_type_id,
                "name": transmission.transmission_base.transmission_type.name,
            } if transmission.transmission_base and transmission.transmission_base.transmission_type else None,
            "num_speeds": {
                "id": transmission.transmission_base.transmission_num_speeds.transmission_num_speeds_id,
                "num_speeds": transmission.transmission_base.transmission_num_speeds.num_speeds,
            } if transmission.transmission_base and transmission.transmission_base.transmission_num_speeds else None,
            "control_type": {
                "id": transmission.transmission_base.transmission_control_type.transmission_control_type_id,
                "name": transmission.transmission_base.transmission_control_type.name,
            } if transmission.transmission_base and transmission.transmission_base.transmission_control_type else None,
            "mfr_code": {
                "id": transmission.transmission_mfr_code.transmission_mfr_code_id,
                "code": transmission.transmission_mfr_code.code,
            } if transmission.transmission_mfr_code else None,
            "elec_controlled": {
                "id": transmission.elec_controlled.elec_controlled_id,
                "value": transmission.elec_controlled.value,
            } if transmission.elec_controlled else None,
            "manufacturer": {"id": transmission.transmission_mfr.mfr_id,
                            "name": transmission.transmission_mfr.name} if transmission.transmission_mfr else None,
        }


class DriveTypeRepository(BaseRepository[DriveType, uuid.UUID]):
    """Repository for DriveType entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the drive type repository.

        Args:
            db: The database session.
        """
        super().__init__(model=DriveType, db=db)

    async def get_by_drive_type_id(self, drive_type_id: int) -> Optional[DriveType]:
        """Get a drive type by its VCdb ID.

        Args:
            drive_type_id: The drive type ID.

        Returns:
            The drive type if found, None otherwise.
        """
        query = select(DriveType).where(DriveType.drive_type_id == drive_type_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all_drive_types(self) -> List[DriveType]:
        """Get all drive types.

        Returns:
            List of all drive types.
        """
        query = select(DriveType).order_by(DriveType.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())


class BodyStyleConfigRepository(BaseRepository[BodyStyleConfig, uuid.UUID]):
    """Repository for BodyStyleConfig entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the body style config repository.

        Args:
            db: The database session.
        """
        super().__init__(model=BodyStyleConfig, db=db)

    async def get_by_body_style_config_id(
        self, body_style_config_id: int
    ) -> Optional[BodyStyleConfig]:
        """Get a body style config by its VCdb ID.

        Args:
            body_style_config_id: The body style config ID.

        Returns:
            The body style config if found, None otherwise.
        """
        query = select(BodyStyleConfig).where(
            BodyStyleConfig.body_style_config_id == body_style_config_id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_body_type(self, body_type_id: int) -> List[BodyStyleConfig]:
        """Get body style configs by body type.

        Args:
            body_type_id: The body type ID.

        Returns:
            List of body style configs with the specified body type.
        """
        query = select(BodyStyleConfig).where(
            BodyStyleConfig.body_type_id == body_type_id
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_full_body_style_details(
        self, body_style_config_id: int
    ) -> Dict[str, Any]:
        """Get full details for a body style configuration.

        Args:
            body_style_config_id: The body style config ID.

        Returns:
            Dict with detailed body style information.
        """
        # Get the body style config with all related entities
        query = (
            select(BodyStyleConfig)
            .options(
                selectinload(BodyStyleConfig.body_type),
                selectinload(BodyStyleConfig.body_num_doors),
            )
            .where(BodyStyleConfig.body_style_config_id == body_style_config_id)
        )

        result = await self.db.execute(query)
        body_style_config = result.scalars().first()

        if not body_style_config:
            return {}

        # Construct the detailed response
        return {
            "body_style_config": {
                "id": body_style_config.body_style_config_id,
                "body_type_id": body_style_config.body_type_id,
                "body_num_doors_id": body_style_config.body_num_doors_id,
            },
            "body_type": {"id": body_style_config.body_type.body_type_id,
                         "name": body_style_config.body_type.name} if body_style_config.body_type else None,
            "body_num_doors": {
                "id": body_style_config.body_num_doors.body_num_doors_id,
                "num_doors": body_style_config.body_num_doors.num_doors,
            } if body_style_config.body_num_doors else None,
        }


class BrakeConfigRepository(BaseRepository[BrakeConfig, uuid.UUID]):
    """Repository for BrakeConfig entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the brake config repository.

        Args:
            db: The database session.
        """
        super().__init__(model=BrakeConfig, db=db)

    async def get_by_brake_config_id(
        self, brake_config_id: int
    ) -> Optional[BrakeConfig]:
        """Get a brake config by its VCdb ID.

        Args:
            brake_config_id: The brake config ID.

        Returns:
            The brake config if found, None otherwise.
        """
        query = select(BrakeConfig).where(
            BrakeConfig.brake_config_id == brake_config_id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_full_brake_config_details(
        self, brake_config_id: int
    ) -> Dict[str, Any]:
        """Get full details for a brake configuration.

        Args:
            brake_config_id: The brake config ID.

        Returns:
            Dict with detailed brake configuration information.
        """
        # Get the brake config with all related entities
        query = (
            select(BrakeConfig)
            .options(
                selectinload(BrakeConfig.front_brake_type),
                selectinload(BrakeConfig.rear_brake_type),
                selectinload(BrakeConfig.brake_system),
                selectinload(BrakeConfig.brake_abs),
            )
            .where(BrakeConfig.brake_config_id == brake_config_id)
        )

        result = await self.db.execute(query)
        brake_config = result.scalars().first()

        if not brake_config:
            return {}

        # Construct the detailed response
        return {
            "brake_config": {
                "id": brake_config.brake_config_id,
                "front_brake_type_id": brake_config.front_brake_type_id,
                "rear_brake_type_id": brake_config.rear_brake_type_id,
                "brake_system_id": brake_config.brake_system_id,
                "brake_abs_id": brake_config.brake_abs_id,
            },
            "front_brake_type": {
                "id": brake_config.front_brake_type.brake_type_id,
                "name": brake_config.front_brake_type.name,
            } if brake_config.front_brake_type else None,
            "rear_brake_type": {
                "id": brake_config.rear_brake_type.brake_type_id,
                "name": brake_config.rear_brake_type.name,
            } if brake_config.rear_brake_type else None,
            "brake_system": {
                "id": brake_config.brake_system.brake_system_id,
                "name": brake_config.brake_system.name,
            } if brake_config.brake_system else None,
            "brake_abs": {
                "id": brake_config.brake_abs.brake_abs_id,
                "name": brake_config.brake_abs.name,
            } if brake_config.brake_abs else None,
        }


class WheelBaseRepository(BaseRepository[WheelBase, uuid.UUID]):
    """Repository for WheelBase entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the wheel base repository.

        Args:
            db: The database session.
        """
        super().__init__(model=WheelBase, db=db)

    async def get_by_wheel_base_id(self, wheel_base_id: int) -> Optional[WheelBase]:
        """Get a wheel base by its VCdb ID.

        Args:
            wheel_base_id: The wheel base ID.

        Returns:
            The wheel base if found, None otherwise.
        """
        query = select(WheelBase).where(WheelBase.wheel_base_id == wheel_base_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all_wheel_bases(self) -> List[WheelBase]:
        """Get all wheel bases.

        Returns:
            List of all wheel bases.
        """
        query = select(WheelBase).order_by(WheelBase.wheel_base)
        result = await self.db.execute(query)
        return list(result.scalars().all())
