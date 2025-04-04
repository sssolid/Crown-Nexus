from __future__ import annotations
'VCdb repository implementation.\n\nThis module provides data access and persistence operations for VCdb entities.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.vcdb.models import Vehicle, BaseVehicle, Make, Model, Year, SubModel, VehicleType, Region, VCdbVersion, DriveType, BrakeType, BrakeSystem, BrakeABS, BrakeConfig, BodyType, BodyNumDoors, BodyStyleConfig, EngineBlock, EngineBoreStroke, EngineBase, Aspiration, FuelType, CylinderHeadType, FuelDeliveryType, FuelDeliverySubType, FuelSystemControlType, FuelSystemDesign, FuelDeliveryConfig, EngineDesignation, EngineVIN, EngineVersion, Valves, Mfr, IgnitionSystemType, PowerOutput, EngineConfig, TransmissionType, TransmissionNumSpeeds, TransmissionControlType, TransmissionBase, TransmissionMfrCode, ElecControlled, Transmission, WheelBase
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
        self.engine_config_repo = EngineConfigRepository(db)
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
        query = select(Vehicle).join(BaseVehicle, Vehicle.base_vehicle_id == BaseVehicle.base_vehicle_id).join(Year, BaseVehicle.year_id == Year.year_id).join(Make, BaseVehicle.make_id == Make.make_id).join(Model, BaseVehicle.model_id == Model.model_id).join(SubModel, Vehicle.submodel_id == SubModel.submodel_id)
        conditions = []
        if year:
            conditions.append(Year.year == year)
        if make:
            conditions.append(Make.name.ilike(f'%{make}%'))
        if model:
            conditions.append(Model.name.ilike(f'%{model}%'))
        if submodel:
            conditions.append(SubModel.name.ilike(f'%{submodel}%'))
        if body_type:
            query = query.join(BodyStyleConfig, Vehicle.id == BodyStyleConfig.body_style_config_id).join(BodyType, BodyStyleConfig.body_type_id == BodyType.body_type_id)
            conditions.append(BodyType.name.ilike(f'%{body_type}%'))
        if engine_config:
            query = query.join(EngineConfig, Vehicle.id == EngineConfig.engine_config_id)
            conditions.append(EngineConfig.engine_config_id == engine_config)
        if transmission_type:
            query = query.join(Transmission, Vehicle.id == Transmission.transmission_id).join(TransmissionBase, Transmission.transmission_base_id == TransmissionBase.transmission_base_id)
            conditions.append(TransmissionBase.transmission_type_id == transmission_type)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.order_by(desc(Year.year), Make.name, Model.name)
        return await self.paginate(query, page, page_size)
    async def get_submodels_by_base_vehicle(self, base_vehicle_id: int) -> List[SubModel]:
        query = select(SubModel).join(Vehicle, SubModel.submodel_id == Vehicle.submodel_id).where(Vehicle.base_vehicle_id == base_vehicle_id).distinct().order_by(SubModel.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_vehicle_configurations(self, vehicle_id: int) -> Dict[str, List[Any]]:
        vehicle = await self.get_by_vehicle_id(vehicle_id)
        if not vehicle:
            return {'engines': [], 'transmissions': [], 'drive_types': [], 'body_styles': [], 'brake_configs': [], 'wheel_bases': []}
        engine_query = select(EngineConfig).join(EngineBase, EngineConfig.engine_base_id == EngineBase.engine_base_id).join(EngineBlock, EngineBase.engine_block_id == EngineBlock.engine_block_id).join(FuelType, EngineConfig.fuel_type_id == FuelType.fuel_type_id).join(Aspiration, EngineConfig.aspiration_id == Aspiration.aspiration_id).where(EngineConfig.engine_config_id.in_([ec.engine_config_id for ec in vehicle.engine_configs]))
        engines_result = await self.db.execute(engine_query)
        engines = engines_result.unique().all()
        transmission_query = select(Transmission).join(TransmissionBase, Transmission.transmission_base_id == TransmissionBase.transmission_base_id).join(TransmissionType, TransmissionBase.transmission_type_id == TransmissionType.transmission_type_id).join(TransmissionNumSpeeds, TransmissionBase.transmission_num_speeds_id == TransmissionNumSpeeds.transmission_num_speeds_id).where(Transmission.transmission_id.in_([t.transmission_id for t in vehicle.transmissions]))
        transmissions_result = await self.db.execute(transmission_query)
        transmissions = transmissions_result.unique().all()
        return {'engines': engines, 'transmissions': transmissions, 'drive_types': vehicle.drive_types, 'body_styles': vehicle.body_style_configs, 'brake_configs': vehicle.brake_configs, 'wheel_bases': vehicle.wheel_bases}
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
            conditions.append(Year.year == year)
        if make:
            conditions.append(Make.name.ilike(f'%{make}%'))
        if model:
            conditions.append(Model.name.ilike(f'%{model}%'))
        if conditions:
            query = query.where(and_(*conditions))
        query = query.order_by(desc(Year.year), Make.name, Model.name)
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
        query = select(Make).join(BaseVehicle, Make.make_id == BaseVehicle.make_id).join(Year, BaseVehicle.year_id == Year.year_id).where(Year.year == year).distinct().order_by(Make.name)
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
        query = select(Model).join(BaseVehicle, Model.model_id == BaseVehicle.model_id).join(Year, BaseVehicle.year_id == Year.year_id).where(Year.year == year, BaseVehicle.make_id == make_id).distinct().order_by(Model.name)
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
        query = select(Year).where(Year.year == year)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_all_years(self) -> List[Year]:
        query = select(Year).order_by(desc(Year.year))
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_year_range(self) -> Tuple[int, int]:
        min_query = select(func.min(Year.year))
        max_query = select(func.max(Year.year))
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
    async def get_full_engine_details(self, engine_config_id: int) -> Dict[str, Any]:
        query = select(EngineConfig, EngineBase, EngineBlock, EngineBoreStroke, Aspiration, FuelType, CylinderHeadType, FuelDeliveryConfig, EngineDesignation, EngineVIN, Valves, Mfr, IgnitionSystemType, EngineVersion, PowerOutput).join(EngineBase, EngineConfig.engine_base_id == EngineBase.engine_base_id).join(EngineBlock, EngineBase.engine_block_id == EngineBlock.engine_block_id).join(EngineBoreStroke, EngineBase.engine_bore_stroke_id == EngineBoreStroke.engine_bore_stroke_id).join(Aspiration, EngineConfig.aspiration_id == Aspiration.aspiration_id).join(FuelType, EngineConfig.fuel_type_id == FuelType.fuel_type_id).join(CylinderHeadType, EngineConfig.cylinder_head_type_id == CylinderHeadType.cylinder_head_type_id).join(FuelDeliveryConfig, EngineConfig.fuel_delivery_config_id == FuelDeliveryConfig.fuel_delivery_config_id).join(EngineDesignation, EngineConfig.engine_designation_id == EngineDesignation.engine_designation_id).join(EngineVIN, EngineConfig.engine_vin_id == EngineVIN.engine_vin_id).join(Valves, EngineConfig.valves_id == Valves.valves_id).join(Mfr, EngineConfig.engine_mfr_id == Mfr.mfr_id).join(IgnitionSystemType, EngineConfig.ignition_system_type_id == IgnitionSystemType.ignition_system_type_id).join(EngineVersion, EngineConfig.engine_version_id == EngineVersion.engine_version_id).join(PowerOutput, EngineConfig.power_output_id == PowerOutput.power_output_id).where(EngineConfig.engine_config_id == engine_config_id)
        result = await self.db.execute(query)
        row = result.first()
        if not row:
            return {}
        engine_config, engine_base, engine_block, engine_bore_stroke, aspiration, fuel_type, cylinder_head_type, fuel_delivery_config, engine_designation, engine_vin, valves, mfr, ignition_system_type, engine_version, power_output = row
        fuel_delivery_query = select(FuelDeliveryType, FuelDeliverySubType, FuelSystemControlType, FuelSystemDesign).join(FuelDeliverySubType, FuelDeliveryConfig.fuel_delivery_subtype_id == FuelDeliverySubType.fuel_delivery_subtype_id).join(FuelSystemControlType, FuelDeliveryConfig.fuel_system_control_type_id == FuelSystemControlType.fuel_system_control_type_id).join(FuelSystemDesign, FuelDeliveryConfig.fuel_system_design_id == FuelSystemDesign.fuel_system_design_id).where(FuelDeliveryConfig.fuel_delivery_config_id == fuel_delivery_config.fuel_delivery_config_id)
        fuel_delivery_result = await self.db.execute(fuel_delivery_query)
        fuel_delivery_row = fuel_delivery_result.first()
        if fuel_delivery_row:
            fuel_delivery_type, fuel_delivery_subtype, fuel_system_control_type, fuel_system_design = fuel_delivery_row
        else:
            fuel_delivery_type = fuel_delivery_subtype = fuel_system_control_type = fuel_system_design = None
        return {'engine_config': {'id': engine_config.engine_config_id, 'engine_base_id': engine_config.engine_base_id, 'engine_designation_id': engine_config.engine_designation_id, 'engine_vin_id': engine_config.engine_vin_id, 'valves_id': engine_config.valves_id, 'fuel_delivery_config_id': engine_config.fuel_delivery_config_id, 'aspiration_id': engine_config.aspiration_id, 'cylinder_head_type_id': engine_config.cylinder_head_type_id, 'fuel_type_id': engine_config.fuel_type_id, 'ignition_system_type_id': engine_config.ignition_system_type_id, 'engine_mfr_id': engine_config.engine_mfr_id, 'engine_version_id': engine_config.engine_version_id, 'power_output_id': engine_config.power_output_id}, 'engine_block': {'id': engine_block.engine_block_id, 'liter': engine_block.liter, 'cc': engine_block.cc, 'cid': engine_block.cid, 'cylinders': engine_block.cylinders, 'block_type': engine_block.block_type}, 'engine_bore_stroke': {'id': engine_bore_stroke.engine_bore_stroke_id, 'bore_in': engine_bore_stroke.bore_in, 'bore_metric': engine_bore_stroke.bore_metric, 'stroke_in': engine_bore_stroke.stroke_in, 'stroke_metric': engine_bore_stroke.stroke_metric}, 'aspiration': {'id': aspiration.aspiration_id, 'name': aspiration.name}, 'fuel_type': {'id': fuel_type.fuel_type_id, 'name': fuel_type.name}, 'cylinder_head_type': {'id': cylinder_head_type.cylinder_head_type_id, 'name': cylinder_head_type.name}, 'fuel_delivery': {'type': fuel_delivery_type.name if fuel_delivery_type else None, 'subtype': fuel_delivery_subtype.name if fuel_delivery_subtype else None, 'control_type': fuel_system_control_type.name if fuel_system_control_type else None, 'design': fuel_system_design.name if fuel_system_design else None}, 'engine_designation': {'id': engine_designation.engine_designation_id, 'name': engine_designation.name}, 'engine_vin': {'id': engine_vin.engine_vin_id, 'code': engine_vin.code}, 'valves': {'id': valves.valves_id, 'valves_per_engine': valves.valves_per_engine}, 'manufacturer': {'id': mfr.mfr_id, 'name': mfr.name}, 'ignition_system_type': {'id': ignition_system_type.ignition_system_type_id, 'name': ignition_system_type.name}, 'engine_version': {'id': engine_version.engine_version_id, 'version': engine_version.version}, 'power_output': {'id': power_output.power_output_id, 'horsepower': power_output.horsepower, 'kilowatt': power_output.kilowatt}}
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
        query = select(Transmission, TransmissionBase, TransmissionType, TransmissionNumSpeeds, TransmissionControlType, TransmissionMfrCode, ElecControlled, Mfr).join(TransmissionBase, Transmission.transmission_base_id == TransmissionBase.transmission_base_id).join(TransmissionType, TransmissionBase.transmission_type_id == TransmissionType.transmission_type_id).join(TransmissionNumSpeeds, TransmissionBase.transmission_num_speeds_id == TransmissionNumSpeeds.transmission_num_speeds_id).join(TransmissionControlType, TransmissionBase.transmission_control_type_id == TransmissionControlType.transmission_control_type_id).join(TransmissionMfrCode, Transmission.transmission_mfr_code_id == TransmissionMfrCode.transmission_mfr_code_id).join(ElecControlled, Transmission.elec_controlled_id == ElecControlled.elec_controlled_id).join(Mfr, Transmission.transmission_mfr_id == Mfr.mfr_id).where(Transmission.transmission_id == transmission_id)
        result = await self.db.execute(query)
        row = result.first()
        if not row:
            return {}
        transmission, transmission_base, transmission_type, transmission_num_speeds, transmission_control_type, transmission_mfr_code, elec_controlled, mfr = row
        return {'transmission': {'id': transmission.transmission_id, 'transmission_base_id': transmission.transmission_base_id, 'transmission_mfr_code_id': transmission.transmission_mfr_code_id, 'elec_controlled_id': transmission.elec_controlled_id, 'transmission_mfr_id': transmission.transmission_mfr_id}, 'type': {'id': transmission_type.transmission_type_id, 'name': transmission_type.name}, 'num_speeds': {'id': transmission_num_speeds.transmission_num_speeds_id, 'num_speeds': transmission_num_speeds.num_speeds}, 'control_type': {'id': transmission_control_type.transmission_control_type_id, 'name': transmission_control_type.name}, 'mfr_code': {'id': transmission_mfr_code.transmission_mfr_code_id, 'code': transmission_mfr_code.code}, 'elec_controlled': {'id': elec_controlled.elec_controlled_id, 'value': elec_controlled.value}, 'manufacturer': {'id': mfr.mfr_id, 'name': mfr.name}}
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
        query = select(BodyStyleConfig, BodyType, BodyNumDoors).join(BodyType, BodyStyleConfig.body_type_id == BodyType.body_type_id).join(BodyNumDoors, BodyStyleConfig.body_num_doors_id == BodyNumDoors.body_num_doors_id).where(BodyStyleConfig.body_style_config_id == body_style_config_id)
        result = await self.db.execute(query)
        row = result.first()
        if not row:
            return {}
        body_style_config, body_type, body_num_doors = row
        return {'body_style_config': {'id': body_style_config.body_style_config_id, 'body_type_id': body_style_config.body_type_id, 'body_num_doors_id': body_style_config.body_num_doors_id}, 'body_type': {'id': body_type.body_type_id, 'name': body_type.name}, 'body_num_doors': {'id': body_num_doors.body_num_doors_id, 'num_doors': body_num_doors.num_doors}}
class BrakeConfigRepository(BaseRepository[BrakeConfig, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=BrakeConfig, db=db)
    async def get_by_brake_config_id(self, brake_config_id: int) -> Optional[BrakeConfig]:
        query = select(BrakeConfig).where(BrakeConfig.brake_config_id == brake_config_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_full_brake_config_details(self, brake_config_id: int) -> Dict[str, Any]:
        query = select(BrakeConfig, BrakeType.name.label('front_brake_type_name'), BrakeType.name.label('rear_brake_type_name'), BrakeSystem, BrakeABS).join(BrakeType, BrakeConfig.front_brake_type_id == BrakeType.brake_type_id, isouter=True).join(BrakeType, BrakeConfig.rear_brake_type_id == BrakeType.brake_type_id, isouter=True).join(BrakeSystem, BrakeConfig.brake_system_id == BrakeSystem.brake_system_id, isouter=True).join(BrakeABS, BrakeConfig.brake_abs_id == BrakeABS.brake_abs_id, isouter=True).where(BrakeConfig.brake_config_id == brake_config_id)
        result = await self.db.execute(query)
        row = result.first()
        if not row:
            return {}
        brake_config, front_brake_type_name, rear_brake_type_name, brake_system, brake_abs = row
        return {'brake_config': {'id': brake_config.brake_config_id, 'front_brake_type_id': brake_config.front_brake_type_id, 'rear_brake_type_id': brake_config.rear_brake_type_id, 'brake_system_id': brake_config.brake_system_id, 'brake_abs_id': brake_config.brake_abs_id}, 'front_brake_type': {'id': brake_config.front_brake_type_id, 'name': front_brake_type_name}, 'rear_brake_type': {'id': brake_config.rear_brake_type_id, 'name': rear_brake_type_name}, 'brake_system': {'id': brake_system.brake_system_id if brake_system else None, 'name': brake_system.name if brake_system else None}, 'brake_abs': {'id': brake_abs.brake_abs_id if brake_abs else None, 'name': brake_abs.name if brake_abs else None}}
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