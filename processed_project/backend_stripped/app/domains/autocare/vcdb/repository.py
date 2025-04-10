from __future__ import annotations
'VCdb repository implementation.\n\nThis module provides data access and persistence operations for VCdb entities.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository
from app.domains.autocare.vcdb.models import Vehicle, BaseVehicle, Make, Model, Year, SubModel, VehicleType, Region, VCdbVersion, DriveType, BrakeType, BrakeSystem, BrakeABS, BrakeConfig, BodyType, BodyNumDoors, BodyStyleConfig, EngineBlock, EngineBoreStroke, EngineBase, EngineBase2, Aspiration, FuelType, CylinderHeadType, FuelDeliveryType, FuelDeliverySubType, FuelSystemControlType, FuelSystemDesign, FuelDeliveryConfig, EngineDesignation, EngineVIN, EngineVersion, Valves, Mfr, IgnitionSystemType, PowerOutput, EngineConfig, EngineConfig2, TransmissionType, TransmissionNumSpeeds, TransmissionControlType, TransmissionBase, TransmissionMfrCode, ElecControlled, Transmission, WheelBase, VehicleToEngineConfig, VehicleToTransmission, VehicleToDriveType, VehicleToBodyStyleConfig, VehicleToBrakeConfig, VehicleToWheelBase
class VCdbRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.vehicle_repo = VehicleRepository(db)
        self.base_vehicle_repo = BaseVehicleRepository(db)
        self.make_repo = MakeRepository(db)
        self.model_repo = ModelRepository(db)
        self.year_repo = YearRepository(db)
        self.submodel_repo = SubModelRepository(db)
        self.vehicle_type_repo = VehicleTypeRepository(db)
        self.region_repo = RegionRepository(db)
        self.engine_base_repo = EngineBaseRepository(db)
        self.engine_config_repo = EngineConfigRepository(db)
        self.engine_base2_repo = EngineBase2Repository(db)
        self.engine_config2_repo = EngineConfig2Repository(db)
        self.transmission_repo = TransmissionRepository(db)
        self.drive_type_repo = DriveTypeRepository(db)
        self.body_style_repo = BodyStyleConfigRepository(db)
        self.brake_config_repo = BrakeConfigRepository(db)
        self.wheel_base_repo = WheelBaseRepository(db)
    async def get_version(self) -> Optional[str]:
        query = select(VCdbVersion).where(VCdbVersion.is_current == True)
        result = await self.db.execute(query)
        version = result.scalars().first()
        if version:
            return version.version_date.strftime('%Y-%m-%d')
        return None
    async def update_version(self, version_date: datetime) -> VCdbVersion:
        update_query = select(VCdbVersion).where(VCdbVersion.is_current == True)
        result = await self.db.execute(update_query)
        old_versions = result.scalars().all()
        for version in old_versions:
            version.is_current = False
        version = VCdbVersion(version_date=version_date, is_current=True)
        self.db.add(version)
        await self.db.flush()
        return version
class VehicleRepository(BaseRepository[Vehicle, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Vehicle, db=db)
    async def get_by_vehicle_id(self, vehicle_id: int) -> Optional[Vehicle]:
        query = select(Vehicle).where(Vehicle.vehicle_id == vehicle_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def search(self, year: Optional[int]=None, make: Optional[str]=None, model: Optional[str]=None, submodel: Optional[str]=None, body_type: Optional[str]=None, engine_config: Optional[int]=None, transmission_type: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(Vehicle).join(BaseVehicle, Vehicle.base_vehicle_id == BaseVehicle.base_vehicle_id).join(Year, BaseVehicle.year_id == Year.year_id).join(Make, BaseVehicle.make_id == Make.make_id).join(Model, BaseVehicle.model_id == Model.model_id).join(SubModel, Vehicle.submodel_id == SubModel.submodel_id).options(selectinload(Vehicle.base_vehicle).selectinload(BaseVehicle.make), selectinload(Vehicle.base_vehicle).selectinload(BaseVehicle.year), selectinload(Vehicle.base_vehicle).selectinload(BaseVehicle.model), selectinload(Vehicle.submodel), selectinload(Vehicle.region))
        conditions = []
        if year:
            conditions.append(Year.year_id == year)
        if make:
            conditions.append(Make.name.ilike(f'%{make}%'))
        if model:
            conditions.append(Model.name.ilike(f'%{model}%'))
        if submodel:
            conditions.append(SubModel.name.ilike(f'%{submodel}%'))
        if body_type:
            query = query.join(Vehicle.body_style_configs).join(BodyType, BodyStyleConfig.body_type_id == BodyType.body_type_id)
            conditions.append(BodyType.name.ilike(f'%{body_type}%'))
        if engine_config:
            query = query.join(Vehicle.engine_configs)
            conditions.append(EngineConfig2.engine_config_id == engine_config)
        if transmission_type:
            query = query.join(Vehicle.transmissions).join(TransmissionBase)
            conditions.append(TransmissionBase.transmission_type_id == transmission_type)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.order_by(desc(Year.year_id), Make.name, Model.name)
        return await self.paginate(query, page, page_size)
    async def get_submodels_by_base_vehicle(self, base_vehicle_id: int) -> List[SubModel]:
        query = select(SubModel).join(Vehicle, SubModel.submodel_id == Vehicle.submodel_id).where(Vehicle.base_vehicle_id == base_vehicle_id).distinct().order_by(SubModel.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_vehicle_configurations(self, vehicle_id: int) -> Dict[str, List[Any]]:
        vehicle_query = select(Vehicle).where(Vehicle.vehicle_id == vehicle_id).options(selectinload(Vehicle.engine_configs), selectinload(Vehicle.transmissions), selectinload(Vehicle.drive_types), selectinload(Vehicle.body_style_configs), selectinload(Vehicle.brake_configs), selectinload(Vehicle.wheel_bases))
        result = await self.db.execute(vehicle_query)
        vehicle = result.scalars().first()
        if not vehicle:
            return {'engines': [], 'transmissions': [], 'drive_types': [], 'body_styles': [], 'brake_configs': [], 'wheel_bases': []}
        engine_config_ids = [ec.engine_config_id for ec in vehicle.engine_configs]
        engine_configs = []
        for engine_config_id in engine_config_ids:
            ec_query = select(EngineConfig).where(EngineConfig.engine_config_id == engine_config_id)
            ec_result = await self.db.execute(ec_query)
            ec = ec_result.scalars().first()
            if ec:
                base_query = select(EngineBase).where(EngineBase.engine_base_id == ec.engine_base_id)
                base_result = await self.db.execute(base_query)
                base = base_result.scalars().first()
                fuel_type_query = select(FuelType).where(FuelType.fuel_type_id == ec.fuel_type_id)
                fuel_type_result = await self.db.execute(fuel_type_query)
                fuel_type = fuel_type_result.scalars().first()
                aspiration_query = select(Aspiration).where(Aspiration.aspiration_id == ec.aspiration_id)
                aspiration_result = await self.db.execute(aspiration_query)
                aspiration = aspiration_result.scalars().first()
                power_output_query = select(PowerOutput).where(PowerOutput.power_output_id == ec.power_output_id)
                power_output_result = await self.db.execute(power_output_query)
                power_output = power_output_result.scalars().first()
                engine_combined = {'config': ec, 'base': base, 'fuel_type': fuel_type, 'aspiration': aspiration, 'power_output': power_output}
                engine_configs.append(engine_combined)
        transmission_query = select(Transmission).where(Transmission.transmission_id.in_([t.transmission_id for t in vehicle.transmissions])).options(selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_type), selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_num_speeds), selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_control_type), selectinload(Transmission.transmission_mfr_code), selectinload(Transmission.elec_controlled), selectinload(Transmission.transmission_mfr))
        transmissions_result = await self.db.execute(transmission_query)
        transmissions = transmissions_result.unique().all()
        return {'engines': engine_configs, 'transmissions': transmissions, 'drive_types': vehicle.drive_types, 'body_styles': vehicle.body_style_configs, 'brake_configs': vehicle.brake_configs, 'wheel_bases': vehicle.wheel_bases}
    async def get_vehicle_configurations2(self, vehicle_id: int) -> Dict[str, List[Any]]:
        vehicle_count_query = select(func.count()).where(Vehicle.vehicle_id == vehicle_id)
        vehicle_count_result = await self.db.execute(vehicle_count_query)
        vehicle_exists = vehicle_count_result.scalar() > 0
        if not vehicle_exists:
            return {'engines': [], 'transmissions': [], 'drive_types': [], 'body_styles': [], 'brake_configs': [], 'wheel_bases': []}
        engines_query = select(EngineConfig2).join(VehicleToEngineConfig, EngineConfig2.engine_config_id == VehicleToEngineConfig.engine_config_id).where(VehicleToEngineConfig.vehicle_id == vehicle_id).options(selectinload(EngineConfig2.engine_base).selectinload(EngineBase2.engine_block), selectinload(EngineConfig2.engine_block), selectinload(EngineConfig2.fuel_type), selectinload(EngineConfig2.aspiration), selectinload(EngineConfig2.power_output))
        engines_result = await self.db.execute(engines_query)
        engines = engines_result.scalars().all()
        transmissions_query = select(Transmission).join(VehicleToTransmission, Transmission.transmission_id == VehicleToTransmission.transmission_id).where(VehicleToTransmission.vehicle_id == vehicle_id).options(selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_type), selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_num_speeds), selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_control_type), selectinload(Transmission.transmission_mfr_code), selectinload(Transmission.elec_controlled), selectinload(Transmission.transmission_mfr))
        transmissions_result = await self.db.execute(transmissions_query)
        transmissions = transmissions_result.scalars().all()
        drive_types_query = select(DriveType).join(VehicleToDriveType, DriveType.drive_type_id == VehicleToDriveType.drive_type_id).where(VehicleToDriveType.vehicle_id == vehicle_id)
        drive_types_result = await self.db.execute(drive_types_query)
        drive_types = drive_types_result.scalars().all()
        body_styles_query = select(BodyStyleConfig).join(VehicleToBodyStyleConfig, BodyStyleConfig.body_style_config_id == VehicleToBodyStyleConfig.body_style_config_id).where(VehicleToBodyStyleConfig.vehicle_id == vehicle_id).options(selectinload(BodyStyleConfig.body_type), selectinload(BodyStyleConfig.body_num_doors))
        body_styles_result = await self.db.execute(body_styles_query)
        body_styles = body_styles_result.scalars().all()
        brake_configs_query = select(BrakeConfig).join(VehicleToBrakeConfig, BrakeConfig.brake_config_id == VehicleToBrakeConfig.brake_config_id).where(VehicleToBrakeConfig.vehicle_id == vehicle_id).options(selectinload(BrakeConfig.front_brake_type), selectinload(BrakeConfig.rear_brake_type), selectinload(BrakeConfig.brake_system), selectinload(BrakeConfig.brake_abs))
        brake_configs_result = await self.db.execute(brake_configs_query)
        brake_configs = brake_configs_result.scalars().all()
        wheel_bases_query = select(WheelBase).join(VehicleToWheelBase, WheelBase.wheel_base_id == VehicleToWheelBase.wheel_base_id).where(VehicleToWheelBase.vehicle_id == vehicle_id)
        wheel_bases_result = await self.db.execute(wheel_bases_query)
        wheel_bases = wheel_bases_result.scalars().all()
        return {'engines': engines, 'transmissions': transmissions, 'drive_types': drive_types, 'body_styles': body_styles, 'brake_configs': brake_configs, 'wheel_bases': wheel_bases}
    async def get_vehicle_with_components2(self, vehicle_id: int) -> Dict[str, Any]:
        vehicle_query = select(Vehicle).where(Vehicle.vehicle_id == vehicle_id).options(selectinload(Vehicle.base_vehicle).selectinload(BaseVehicle.make), selectinload(Vehicle.base_vehicle).selectinload(BaseVehicle.model), selectinload(Vehicle.base_vehicle).selectinload(BaseVehicle.year), selectinload(Vehicle.submodel), selectinload(Vehicle.region))
        vehicle_result = await self.db.execute(vehicle_query)
        vehicle = vehicle_result.scalars().first()
        if not vehicle:
            return None
        engine_configs_query = select(EngineConfig2).join(VehicleToEngineConfig, EngineConfig2.engine_config_id == VehicleToEngineConfig.engine_config_id).where(VehicleToEngineConfig.vehicle_id == vehicle_id).options(selectinload(EngineConfig2.engine_base).selectinload(EngineBase2.engine_block), selectinload(EngineConfig2.engine_block), selectinload(EngineConfig2.fuel_type), selectinload(EngineConfig2.aspiration), selectinload(EngineConfig2.power_output))
        engine_configs_result = await self.db.execute(engine_configs_query)
        engine_configs = engine_configs_result.scalars().all()
        transmissions_query = select(Transmission).join(VehicleToTransmission, Transmission.transmission_id == VehicleToTransmission.transmission_id).where(VehicleToTransmission.vehicle_id == vehicle_id).options(selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_type), selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_num_speeds), selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_control_type), selectinload(Transmission.transmission_mfr_code), selectinload(Transmission.elec_controlled), selectinload(Transmission.transmission_mfr))
        transmissions_result = await self.db.execute(transmissions_query)
        transmissions = transmissions_result.scalars().all()
        drive_types_query = select(DriveType).join(VehicleToDriveType, DriveType.drive_type_id == VehicleToDriveType.drive_type_id).where(VehicleToDriveType.vehicle_id == vehicle_id)
        drive_types_result = await self.db.execute(drive_types_query)
        drive_types = drive_types_result.scalars().all()
        body_styles_query = select(BodyStyleConfig).join(VehicleToBodyStyleConfig, BodyStyleConfig.body_style_config_id == VehicleToBodyStyleConfig.body_style_config_id).where(VehicleToBodyStyleConfig.vehicle_id == vehicle_id).options(selectinload(BodyStyleConfig.body_type))
        body_styles_result = await self.db.execute(body_styles_query)
        body_styles = body_styles_result.scalars().all()
        return {'vehicle': vehicle, 'engine_configs': engine_configs, 'transmissions': transmissions, 'drive_types': drive_types, 'body_styles': body_styles}
class BaseVehicleRepository(BaseRepository[BaseVehicle, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=BaseVehicle, db=db)
    async def get_by_base_vehicle_id(self, base_vehicle_id: int) -> Optional[BaseVehicle]:
        query = select(BaseVehicle).where(BaseVehicle.base_vehicle_id == base_vehicle_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def find_by_year_make_model(self, year_id: int, make_id: int, model_id: int) -> Optional[BaseVehicle]:
        query = select(BaseVehicle).where(BaseVehicle.year_id == year_id, BaseVehicle.make_id == make_id, BaseVehicle.model_id == model_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def search_by_criteria(self, year: Optional[int]=None, make: Optional[str]=None, model: Optional[str]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(BaseVehicle).join(Year, BaseVehicle.year_id == Year.year_id).join(Make, BaseVehicle.make_id == Make.make_id).join(Model, BaseVehicle.model_id == Model.model_id)
        conditions = []
        if year:
            conditions.append(Year.year_id == year)
        if make:
            conditions.append(Make.name.ilike(f'%{make}%'))
        if model:
            conditions.append(Model.name.ilike(f'%{model}%'))
        if conditions:
            query = query.where(and_(*conditions))
        query = query.order_by(desc(Year.year_id), Make.name, Model.name)
        return await self.paginate(query, page, page_size)
class MakeRepository(BaseRepository[Make, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Make, db=db)
    async def get_by_make_id(self, make_id: int) -> Optional[Make]:
        query = select(Make).where(Make.make_id == make_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def search_by_name(self, name: str) -> List[Make]:
        query = select(Make).where(Make.name.ilike(f'%{name}%')).order_by(Make.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_year(self, year: int) -> List[Make]:
        query = select(Make).join(BaseVehicle, Make.make_id == BaseVehicle.make_id).join(Year, BaseVehicle.year_id == Year.year_id).where(Year.year_id == year).distinct().order_by(Make.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_all_makes(self) -> List[Make]:
        query = select(Make).order_by(Make.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
class ModelRepository(BaseRepository[Model, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Model, db=db)
    async def get_by_model_id(self, model_id: int) -> Optional[Model]:
        query = select(Model).where(Model.model_id == model_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def search_by_name(self, name: str) -> List[Model]:
        query = select(Model).where(Model.name.ilike(f'%{name}%')).order_by(Model.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_year_make(self, year: int, make_id: int) -> List[Model]:
        query = select(Model).join(BaseVehicle, Model.model_id == BaseVehicle.model_id).join(Year, BaseVehicle.year_id == Year.year_id).where(Year.year_id == year, BaseVehicle.make_id == make_id).options(selectinload(Model.vehicle_type)).distinct().order_by(Model.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_vehicle_type(self, vehicle_type_id: int) -> List[Model]:
        query = select(Model).where(Model.vehicle_type_id == vehicle_type_id).order_by(Model.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
class YearRepository(BaseRepository[Year, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Year, db=db)
    async def get_by_year_id(self, year_id: int) -> Optional[Year]:
        query = select(Year).where(Year.year_id == year_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_year(self, year: int) -> Optional[Year]:
        query = select(Year).where(Year.year_id == year)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_all_years(self) -> List[Year]:
        query = select(Year).order_by(desc(Year.year_id))
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_year_range(self) -> Tuple[int, int]:
        min_query = select(func.min(Year.year_id))
        max_query = select(func.max(Year.year_id))
        min_result = await self.db.execute(min_query)
        max_result = await self.db.execute(max_query)
        min_year = min_result.scalar() or datetime.now().year
        max_year = max_result.scalar() or datetime.now().year
        return (min_year, max_year)
class SubModelRepository(BaseRepository[SubModel, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=SubModel, db=db)
    async def get_by_submodel_id(self, submodel_id: int) -> Optional[SubModel]:
        query = select(SubModel).where(SubModel.submodel_id == submodel_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def search_by_name(self, name: str) -> List[SubModel]:
        query = select(SubModel).where(SubModel.name.ilike(f'%{name}%')).order_by(SubModel.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_all_submodels(self) -> List[SubModel]:
        query = select(SubModel).order_by(SubModel.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
class VehicleTypeRepository(BaseRepository[VehicleType, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=VehicleType, db=db)
    async def get_by_vehicle_type_id(self, vehicle_type_id: int) -> Optional[VehicleType]:
        query = select(VehicleType).where(VehicleType.vehicle_type_id == vehicle_type_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_group(self, vehicle_type_group_id: int) -> List[VehicleType]:
        query = select(VehicleType).where(VehicleType.vehicle_type_group_id == vehicle_type_group_id).order_by(VehicleType.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_all_vehicle_types(self) -> List[VehicleType]:
        query = select(VehicleType).order_by(VehicleType.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
class RegionRepository(BaseRepository[Region, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Region, db=db)
    async def get_by_region_id(self, region_id: int) -> Optional[Region]:
        query = select(Region).where(Region.region_id == region_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_parent(self, parent_id: int) -> List[Region]:
        query = select(Region).where(Region.parent_id == parent_id).order_by(Region.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_all_top_level_regions(self) -> List[Region]:
        query = select(Region).where(Region.parent_id == None).order_by(Region.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
class EngineBaseRepository(BaseRepository[EngineBase, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=EngineBase, db=db)
    async def get_by_engine_base_id(self, engine_base_id: int) -> Optional[EngineBase]:
        query = select(EngineBase).where(EngineBase.engine_base_id == engine_base_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def search_by_criteria(self, liter: Optional[str]=None, cylinders: Optional[str]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(EngineBase)
        conditions = []
        if liter:
            conditions.append(EngineBase.liter == liter)
        if cylinders:
            conditions.append(EngineBase.cylinders == cylinders)
        if conditions:
            query = query.where(and_(*conditions))
        return await self.paginate(query, page, page_size)
class EngineConfigRepository(BaseRepository[EngineConfig, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=EngineConfig, db=db)
    async def get_by_engine_config_id(self, engine_config_id: int) -> Optional[EngineConfig]:
        query = select(EngineConfig).where(EngineConfig.engine_config_id == engine_config_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_criteria(self, engine_base_id: Optional[int]=None, fuel_type_id: Optional[int]=None, aspiration_id: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(EngineConfig)
        conditions = []
        if engine_base_id:
            conditions.append(EngineConfig.engine_base_id == engine_base_id)
        if fuel_type_id:
            conditions.append(EngineConfig.fuel_type_id == fuel_type_id)
        if aspiration_id:
            conditions.append(EngineConfig.aspiration_id == aspiration_id)
        if conditions:
            query = query.where(and_(*conditions))
        return await self.paginate(query, page, page_size)
class EngineBase2Repository(BaseRepository[EngineBase2, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=EngineBase2, db=db)
    async def get_by_engine_base_id(self, engine_base_id: int) -> Optional[EngineBase2]:
        query = select(EngineBase2).where(EngineBase2.engine_base_id == engine_base_id).options(selectinload(EngineBase2.engine_block), selectinload(EngineBase2.engine_bore_stroke))
        result = await self.db.execute(query)
        return result.scalars().first()
    async def search_by_criteria(self, engine_block_id: Optional[int]=None, engine_bore_stroke_id: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(EngineBase2).options(selectinload(EngineBase2.engine_block), selectinload(EngineBase2.engine_bore_stroke))
        conditions = []
        if engine_block_id:
            conditions.append(EngineBase2.engine_block_id == engine_block_id)
        if engine_bore_stroke_id:
            conditions.append(EngineBase2.engine_bore_stroke_id == engine_bore_stroke_id)
        if conditions:
            query = query.where(and_(*conditions))
        return await self.paginate(query, page, page_size)
class EngineConfig2Repository(BaseRepository[EngineConfig2, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=EngineConfig2, db=db)
    async def get_by_engine_config_id(self, engine_config_id: int) -> Optional[EngineConfig2]:
        query = select(EngineConfig2).where(EngineConfig2.engine_config_id == engine_config_id).options(selectinload(EngineConfig2.engine_base).selectinload(EngineBase2.engine_block), selectinload(EngineConfig2.engine_base).selectinload(EngineBase2.engine_bore_stroke), selectinload(EngineConfig2.engine_block), selectinload(EngineConfig2.fuel_type), selectinload(EngineConfig2.aspiration))
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_criteria(self, engine_base_id: Optional[int]=None, fuel_type_id: Optional[int]=None, aspiration_id: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(EngineConfig2).options(selectinload(EngineConfig2.engine_base).selectinload(EngineBase2.engine_block), selectinload(EngineConfig2.engine_block), selectinload(EngineConfig2.fuel_type), selectinload(EngineConfig2.aspiration))
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
        query = select(EngineConfig2).options(selectinload(EngineConfig2.engine_base), selectinload(EngineConfig2.engine_block), selectinload(EngineConfig2.engine_bore_stroke), selectinload(EngineConfig2.aspiration), selectinload(EngineConfig2.fuel_type), selectinload(EngineConfig2.cylinder_head_type), selectinload(EngineConfig2.fuel_delivery_config), selectinload(EngineConfig2.engine_designation), selectinload(EngineConfig2.engine_vin), selectinload(EngineConfig2.valves), selectinload(EngineConfig2.engine_mfr), selectinload(EngineConfig2.ignition_system_type), selectinload(EngineConfig2.engine_version), selectinload(EngineConfig2.power_output), selectinload(EngineConfig2.fuel_delivery_config).selectinload(FuelDeliveryConfig.fuel_delivery_type), selectinload(EngineConfig2.fuel_delivery_config).selectinload(FuelDeliveryConfig.fuel_delivery_subtype), selectinload(EngineConfig2.fuel_delivery_config).selectinload(FuelDeliveryConfig.fuel_system_control_type), selectinload(EngineConfig2.fuel_delivery_config).selectinload(FuelDeliveryConfig.fuel_system_design)).where(EngineConfig2.engine_config_id == engine_config_id)
        result = await self.db.execute(query)
        engine_config = result.scalars().first()
        if not engine_config:
            return {}
        return {'engine_config': {'id': engine_config.engine_config_id, 'engine_base_id': engine_config.engine_base_id, 'engine_designation_id': engine_config.engine_designation_id, 'engine_vin_id': engine_config.engine_vin_id, 'valves_id': engine_config.valves_id, 'fuel_delivery_config_id': engine_config.fuel_delivery_config_id, 'aspiration_id': engine_config.aspiration_id, 'cylinder_head_type_id': engine_config.cylinder_head_type_id, 'fuel_type_id': engine_config.fuel_type_id, 'ignition_system_type_id': engine_config.ignition_system_type_id, 'engine_mfr_id': engine_config.engine_mfr_id, 'engine_version_id': engine_config.engine_version_id, 'power_output_id': engine_config.power_output_id}, 'engine_block': {'id': engine_config.engine_block.engine_block_id if engine_config.engine_block else None, 'liter': engine_config.engine_block.liter if engine_config.engine_block else None, 'cc': engine_config.engine_block.cc if engine_config.engine_block else None, 'cid': engine_config.engine_block.cid if engine_config.engine_block else None, 'cylinders': engine_config.engine_block.cylinders if engine_config.engine_block else None, 'block_type': engine_config.engine_block.block_type if engine_config.engine_block else None}, 'engine_bore_stroke': {'id': engine_config.engine_bore_stroke.engine_bore_stroke_id if engine_config.engine_bore_stroke else None, 'bore_in': engine_config.engine_bore_stroke.bore_in if engine_config.engine_bore_stroke else None, 'bore_metric': engine_config.engine_bore_stroke.bore_metric if engine_config.engine_bore_stroke else None, 'stroke_in': engine_config.engine_bore_stroke.stroke_in if engine_config.engine_bore_stroke else None, 'stroke_metric': engine_config.engine_bore_stroke.stroke_metric if engine_config.engine_bore_stroke else None}, 'aspiration': {'id': engine_config.aspiration.aspiration_id, 'name': engine_config.aspiration.name} if engine_config.aspiration else None, 'fuel_type': {'id': engine_config.fuel_type.fuel_type_id, 'name': engine_config.fuel_type.name} if engine_config.fuel_type else None, 'cylinder_head_type': {'id': engine_config.cylinder_head_type.cylinder_head_type_id, 'name': engine_config.cylinder_head_type.name} if engine_config.cylinder_head_type else None, 'fuel_delivery': {'type': engine_config.fuel_delivery_config.fuel_delivery_type.name if engine_config.fuel_delivery_config and engine_config.fuel_delivery_config.fuel_delivery_type else None, 'subtype': engine_config.fuel_delivery_config.fuel_delivery_subtype.name if engine_config.fuel_delivery_config and engine_config.fuel_delivery_config.fuel_delivery_subtype else None, 'control_type': engine_config.fuel_delivery_config.fuel_system_control_type.name if engine_config.fuel_delivery_config and engine_config.fuel_delivery_config.fuel_system_control_type else None, 'design': engine_config.fuel_delivery_config.fuel_system_design.name if engine_config.fuel_delivery_config and engine_config.fuel_delivery_config.fuel_system_design else None}, 'engine_designation': {'id': engine_config.engine_designation.engine_designation_id, 'name': engine_config.engine_designation.name} if engine_config.engine_designation else None, 'engine_vin': {'id': engine_config.engine_vin.engine_vin_id, 'code': engine_config.engine_vin.code} if engine_config.engine_vin else None, 'valves': {'id': engine_config.valves.valves_id, 'valves_per_engine': engine_config.valves.valves_per_engine} if engine_config.valves else None, 'manufacturer': {'id': engine_config.engine_mfr.mfr_id, 'name': engine_config.engine_mfr.name} if engine_config.engine_mfr else None, 'ignition_system_type': {'id': engine_config.ignition_system_type.ignition_system_type_id, 'name': engine_config.ignition_system_type.name} if engine_config.ignition_system_type else None, 'engine_version': {'id': engine_config.engine_version.engine_version_id, 'version': engine_config.engine_version.version} if engine_config.engine_version else None, 'power_output': {'id': engine_config.power_output.power_output_id, 'horsepower': engine_config.power_output.horsepower, 'kilowatt': engine_config.power_output.kilowatt} if engine_config.power_output else None}
class TransmissionRepository(BaseRepository[Transmission, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Transmission, db=db)
    async def get_by_transmission_id(self, transmission_id: int) -> Optional[Transmission]:
        query = select(Transmission).where(Transmission.transmission_id == transmission_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_criteria(self, transmission_type_id: Optional[int]=None, transmission_num_speeds_id: Optional[int]=None, transmission_control_type_id: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(Transmission).join(TransmissionBase, Transmission.transmission_base_id == TransmissionBase.transmission_base_id)
        conditions = []
        if transmission_type_id:
            conditions.append(TransmissionBase.transmission_type_id == transmission_type_id)
        if transmission_num_speeds_id:
            conditions.append(TransmissionBase.transmission_num_speeds_id == transmission_num_speeds_id)
        if transmission_control_type_id:
            conditions.append(TransmissionBase.transmission_control_type_id == transmission_control_type_id)
        if conditions:
            query = query.where(and_(*conditions))
        return await self.paginate(query, page, page_size)
    async def get_full_transmission_details(self, transmission_id: int) -> Dict[str, Any]:
        query = select(Transmission).options(selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_type), selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_num_speeds), selectinload(Transmission.transmission_base).selectinload(TransmissionBase.transmission_control_type), selectinload(Transmission.transmission_mfr_code), selectinload(Transmission.elec_controlled), selectinload(Transmission.transmission_mfr)).where(Transmission.transmission_id == transmission_id)
        result = await self.db.execute(query)
        transmission = result.scalars().first()
        if not transmission:
            return {}
        return {'transmission': {'id': transmission.transmission_id, 'transmission_base_id': transmission.transmission_base_id, 'transmission_mfr_code_id': transmission.transmission_mfr_code_id, 'elec_controlled_id': transmission.elec_controlled_id, 'transmission_mfr_id': transmission.transmission_mfr_id}, 'type': {'id': transmission.transmission_base.transmission_type.transmission_type_id, 'name': transmission.transmission_base.transmission_type.name} if transmission.transmission_base and transmission.transmission_base.transmission_type else None, 'num_speeds': {'id': transmission.transmission_base.transmission_num_speeds.transmission_num_speeds_id, 'num_speeds': transmission.transmission_base.transmission_num_speeds.num_speeds} if transmission.transmission_base and transmission.transmission_base.transmission_num_speeds else None, 'control_type': {'id': transmission.transmission_base.transmission_control_type.transmission_control_type_id, 'name': transmission.transmission_base.transmission_control_type.name} if transmission.transmission_base and transmission.transmission_base.transmission_control_type else None, 'mfr_code': {'id': transmission.transmission_mfr_code.transmission_mfr_code_id, 'code': transmission.transmission_mfr_code.code} if transmission.transmission_mfr_code else None, 'elec_controlled': {'id': transmission.elec_controlled.elec_controlled_id, 'value': transmission.elec_controlled.value} if transmission.elec_controlled else None, 'manufacturer': {'id': transmission.transmission_mfr.mfr_id, 'name': transmission.transmission_mfr.name} if transmission.transmission_mfr else None}
class DriveTypeRepository(BaseRepository[DriveType, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=DriveType, db=db)
    async def get_by_drive_type_id(self, drive_type_id: int) -> Optional[DriveType]:
        query = select(DriveType).where(DriveType.drive_type_id == drive_type_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_all_drive_types(self) -> List[DriveType]:
        query = select(DriveType).order_by(DriveType.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
class BodyStyleConfigRepository(BaseRepository[BodyStyleConfig, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=BodyStyleConfig, db=db)
    async def get_by_body_style_config_id(self, body_style_config_id: int) -> Optional[BodyStyleConfig]:
        query = select(BodyStyleConfig).where(BodyStyleConfig.body_style_config_id == body_style_config_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_body_type(self, body_type_id: int) -> List[BodyStyleConfig]:
        query = select(BodyStyleConfig).where(BodyStyleConfig.body_type_id == body_type_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_full_body_style_details(self, body_style_config_id: int) -> Dict[str, Any]:
        query = select(BodyStyleConfig).options(selectinload(BodyStyleConfig.body_type), selectinload(BodyStyleConfig.body_num_doors)).where(BodyStyleConfig.body_style_config_id == body_style_config_id)
        result = await self.db.execute(query)
        body_style_config = result.scalars().first()
        if not body_style_config:
            return {}
        return {'body_style_config': {'id': body_style_config.body_style_config_id, 'body_type_id': body_style_config.body_type_id, 'body_num_doors_id': body_style_config.body_num_doors_id}, 'body_type': {'id': body_style_config.body_type.body_type_id, 'name': body_style_config.body_type.name} if body_style_config.body_type else None, 'body_num_doors': {'id': body_style_config.body_num_doors.body_num_doors_id, 'num_doors': body_style_config.body_num_doors.num_doors} if body_style_config.body_num_doors else None}
class BrakeConfigRepository(BaseRepository[BrakeConfig, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=BrakeConfig, db=db)
    async def get_by_brake_config_id(self, brake_config_id: int) -> Optional[BrakeConfig]:
        query = select(BrakeConfig).where(BrakeConfig.brake_config_id == brake_config_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_full_brake_config_details(self, brake_config_id: int) -> Dict[str, Any]:
        query = select(BrakeConfig).options(selectinload(BrakeConfig.front_brake_type), selectinload(BrakeConfig.rear_brake_type), selectinload(BrakeConfig.brake_system), selectinload(BrakeConfig.brake_abs)).where(BrakeConfig.brake_config_id == brake_config_id)
        result = await self.db.execute(query)
        brake_config = result.scalars().first()
        if not brake_config:
            return {}
        return {'brake_config': {'id': brake_config.brake_config_id, 'front_brake_type_id': brake_config.front_brake_type_id, 'rear_brake_type_id': brake_config.rear_brake_type_id, 'brake_system_id': brake_config.brake_system_id, 'brake_abs_id': brake_config.brake_abs_id}, 'front_brake_type': {'id': brake_config.front_brake_type.brake_type_id, 'name': brake_config.front_brake_type.name} if brake_config.front_brake_type else None, 'rear_brake_type': {'id': brake_config.rear_brake_type.brake_type_id, 'name': brake_config.rear_brake_type.name} if brake_config.rear_brake_type else None, 'brake_system': {'id': brake_config.brake_system.brake_system_id, 'name': brake_config.brake_system.name} if brake_config.brake_system else None, 'brake_abs': {'id': brake_config.brake_abs.brake_abs_id, 'name': brake_config.brake_abs.name} if brake_config.brake_abs else None}
class WheelBaseRepository(BaseRepository[WheelBase, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=WheelBase, db=db)
    async def get_by_wheel_base_id(self, wheel_base_id: int) -> Optional[WheelBase]:
        query = select(WheelBase).where(WheelBase.wheel_base_id == wheel_base_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_all_wheel_bases(self) -> List[WheelBase]:
        query = select(WheelBase).order_by(WheelBase.wheel_base)
        result = await self.db.execute(query)
        return list(result.scalars().all())