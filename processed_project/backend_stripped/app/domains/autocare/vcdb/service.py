from __future__ import annotations
'VCdb service implementation.\n\nThis module provides service methods for working with VCdb data, including\nimport, export, and query operations for vehicles and their components.\n'
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import VCdbException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.vcdb.repository import VCdbRepository
from app.logging import get_logger
logger = get_logger('app.domains.autocare.vcdb.service')
class VCdbService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repository = VCdbRepository(db)
    async def get_version(self) -> str:
        version = await self.repository.get_version()
        return version or 'No version information available'
    async def get_stats(self) -> Dict[str, Any]:
        total_vehicles = await self.repository.vehicle_repo.count()
        make_count = await self.repository.make_repo.count()
        model_count = await self.repository.model_repo.count()
        year_range = await self.repository.year_repo.get_year_range()
        return {'totalVehicles': total_vehicles, 'makeCount': make_count, 'modelCount': model_count, 'yearRange': f'{year_range[0]}-{year_range[1]}'}
    async def update_database(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        try:
            file_path_str = str(file_path) if isinstance(file_path, Path) else file_path
            logger.info(f'Starting VCdb database update from {file_path_str}')
            version = await self.repository.update_version(datetime.now())
            logger.info(f'VCdb database updated to {version.version_date}')
            return {'status': 'success', 'version': version.version_date.strftime('%Y-%m-%d'), 'message': 'VCdb database updated successfully'}
        except Exception as e:
            logger.error(f'Error updating VCdb database: {str(e)}', exc_info=True)
            raise VCdbException(f'Failed to update VCdb database: {str(e)}') from e
    async def import_from_aces(self, file_path: Path, params: AutocareImportParams) -> Dict[str, Any]:
        try:
            logger.info(f'Starting vehicle import from ACES XML: {file_path}')
            return {'status': 'success', 'imported': 0, 'updated': 0, 'skipped': 0, 'errors': 0, 'details': []}
        except Exception as e:
            logger.error(f'Error importing from ACES XML: {str(e)}', exc_info=True)
            raise VCdbException(f'Failed to import from ACES XML: {str(e)}') from e
    async def get_years(self) -> List[Dict[str, Any]]:
        years = await self.repository.year_repo.get_all_years()
        return [{'id': year.id, 'year': year.year_id} for year in years]
    async def get_year_range(self) -> Tuple[int, int]:
        return await self.repository.year_repo.get_year_range()
    async def get_makes(self) -> List[Dict[str, Any]]:
        makes = await self.repository.make_repo.get_all_makes()
        return [{'id': make.make_id, 'name': make.name} for make in makes]
    async def get_makes_by_year(self, year: int) -> List[Dict[str, Any]]:
        makes = await self.repository.make_repo.get_by_year(year)
        return [{'id': make.make_id, 'name': make.name} for make in makes]
    async def search_makes(self, search_term: str) -> List[Dict[str, Any]]:
        makes = await self.repository.make_repo.search_by_name(search_term)
        return [{'id': make.make_id, 'name': make.name} for make in makes]
    async def get_make_by_id(self, make_id: int) -> Dict[str, Any]:
        make = await self.repository.make_repo.get_by_make_id(make_id)
        if not make:
            raise ResourceNotFoundException(resource_type='Make', resource_id=str(make_id))
        return {'id': make.make_id, 'name': make.name}
    async def get_models_by_year_make(self, year: int, make_id: int) -> List[Dict[str, Any]]:
        models = await self.repository.model_repo.get_by_year_make(year, make_id)
        return [{'id': model.model_id, 'name': model.name, 'vehicle_type': {'id': model.vehicle_type.vehicle_type_id, 'name': model.vehicle_type.name} if model.vehicle_type else None} for model in models]
    async def search_models(self, search_term: str) -> List[Dict[str, Any]]:
        models = await self.repository.model_repo.search_by_name(search_term)
        return [{'id': model.model_id, 'name': model.name, 'vehicle_type_id': model.vehicle_type_id} for model in models]
    async def get_model_by_id(self, model_id: int) -> Dict[str, Any]:
        model = await self.repository.model_repo.get_by_model_id(model_id)
        if not model:
            raise ResourceNotFoundException(resource_type='Model', resource_id=str(model_id))
        return {'id': model.model_id, 'name': model.name, 'vehicle_type_id': model.vehicle_type_id, 'vehicle_type': {'id': model.vehicle_type.vehicle_type_id, 'name': model.vehicle_type.name} if model.vehicle_type else None}
    async def get_submodels_by_base_vehicle(self, base_vehicle_id: int) -> List[Dict[str, Any]]:
        submodels = await self.repository.vehicle_repo.get_submodels_by_base_vehicle(base_vehicle_id)
        return [{'id': submodel.submodel_id, 'name': submodel.name} for submodel in submodels]
    async def get_all_submodels(self) -> List[Dict[str, Any]]:
        submodels = await self.repository.submodel_repo.get_all_submodels()
        return [{'id': submodel.submodel_id, 'name': submodel.name} for submodel in submodels]
    async def search_submodels(self, search_term: str) -> List[Dict[str, Any]]:
        submodels = await self.repository.submodel_repo.search_by_name(search_term)
        return [{'id': submodel.submodel_id, 'name': submodel.name} for submodel in submodels]
    async def get_vehicle_types(self) -> List[Dict[str, Any]]:
        vehicle_types = await self.repository.vehicle_type_repo.get_all_vehicle_types()
        return [{'id': vt.vehicle_type_id, 'name': vt.name, 'group_id': vt.vehicle_type_group_id} for vt in vehicle_types]
    async def get_vehicle_types_by_group(self, group_id: int) -> List[Dict[str, Any]]:
        vehicle_types = await self.repository.vehicle_type_repo.get_by_group(group_id)
        return [{'id': vt.vehicle_type_id, 'name': vt.name, 'group_id': vt.vehicle_type_group_id} for vt in vehicle_types]
    async def get_regions(self) -> List[Dict[str, Any]]:
        regions = await self.repository.region_repo.get_all_top_level_regions()
        return [{'id': region.region_id, 'name': region.name, 'abbr': region.abbr} for region in regions]
    async def get_regions_by_parent(self, parent_id: int) -> List[Dict[str, Any]]:
        regions = await self.repository.region_repo.get_by_parent(parent_id)
        return [{'id': region.region_id, 'name': region.name, 'abbr': region.abbr} for region in regions]
    async def get_base_vehicle(self, base_vehicle_id: int) -> Dict[str, Any]:
        base_vehicle = await self.repository.base_vehicle_repo.get_by_base_vehicle_id(base_vehicle_id)
        if not base_vehicle:
            raise ResourceNotFoundException(resource_type='BaseVehicle', resource_id=str(base_vehicle_id))
        return {'id': base_vehicle.base_vehicle_id, 'year': base_vehicle.year.year_id if base_vehicle.year else None, 'make': base_vehicle.make.name if base_vehicle.make else None, 'model': base_vehicle.model.name if base_vehicle.model else None, 'year_id': base_vehicle.year_id, 'make_id': base_vehicle.make_id, 'model_id': base_vehicle.model_id}
    async def find_base_vehicle(self, year_id: int, make_id: int, model_id: int) -> Optional[Dict[str, Any]]:
        base_vehicle = await self.repository.base_vehicle_repo.find_by_year_make_model(year_id, make_id, model_id)
        if not base_vehicle:
            return None
        return {'id': base_vehicle.base_vehicle_id, 'year': base_vehicle.year.year_id if base_vehicle.year else None, 'make': base_vehicle.make.name if base_vehicle.make else None, 'model': base_vehicle.model.name if base_vehicle.model else None, 'year_id': base_vehicle.year_id, 'make_id': base_vehicle.make_id, 'model_id': base_vehicle.model_id}
    async def search_base_vehicles(self, year: Optional[int]=None, make: Optional[str]=None, model: Optional[str]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        result = await self.repository.base_vehicle_repo.search_by_criteria(year=year, make=make, model=model, page=page, page_size=page_size)
        base_vehicles = []
        for bv in result['items']:
            base_vehicles.append({'id': bv.base_vehicle_id, 'year': bv.year.year_id if bv.year else None, 'make': bv.make.name if bv.make else None, 'model': bv.model.name if bv.model else None, 'year_id': bv.year_id, 'make_id': bv.make_id, 'model_id': bv.model_id})
        return {'items': base_vehicles, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def search_vehicles(self, year: Optional[int]=None, make: Optional[str]=None, model: Optional[str]=None, submodel: Optional[str]=None, body_type: Optional[str]=None, engine_config: Optional[int]=None, transmission_type: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        result = await self.repository.vehicle_repo.search(year=year, make=make, model=model, submodel=submodel, body_type=body_type, engine_config=engine_config, transmission_type=transmission_type, page=page, page_size=page_size)
        vehicles = []
        for vehicle in result['items']:
            make_name = None
            if vehicle.base_vehicle and vehicle.base_vehicle.make:
                make_name = vehicle.base_vehicle.make.name
            vehicles.append({'id': str(vehicle.id), 'vehicle_id': vehicle.vehicle_id, 'year': vehicle.year, 'make': make_name, 'model': vehicle.model if hasattr(vehicle, 'model') else None, 'submodel': vehicle.submodel.name if vehicle.submodel else None, 'region': vehicle.region.name if vehicle.region else None})
        return {'items': vehicles, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def get_vehicle_by_id(self, vehicle_id: int) -> Dict[str, Any]:
        vehicle = await self.repository.vehicle_repo.get_by_vehicle_id(vehicle_id)
        if not vehicle:
            raise ResourceNotFoundException(resource_type='Vehicle', resource_id=str(vehicle_id))
        make_name = None
        if vehicle.base_vehicle and vehicle.base_vehicle.make:
            make_name = vehicle.base_vehicle.make.name
        return {'id': str(vehicle.id), 'vehicle_id': vehicle.vehicle_id, 'year': vehicle.year, 'make': make_name, 'model': vehicle.model if hasattr(vehicle, 'model') else None, 'submodel': vehicle.submodel.name if vehicle.submodel else None, 'region': vehicle.region.name if vehicle.region else None}
    async def get_vehicle_details(self, vehicle_id: int) -> Dict[str, Any]:
        result = await self.repository.vehicle_repo.get_vehicle_with_components2(vehicle_id)
        if not result:
            raise ResourceNotFoundException(resource_type='Vehicle', resource_id=str(vehicle_id))
        vehicle = result['vehicle']
        engine_configs = result['engine_configs']
        transmissions = result['transmissions']
        drive_types = result['drive_types']
        body_styles = result['body_styles']
        engines = []
        for engine in engine_configs:
            liter = None
            cylinders = None
            if hasattr(engine, 'engine_block') and engine.engine_block:
                liter = engine.engine_block.liter
                cylinders = engine.engine_block.cylinders
            elif hasattr(engine, 'engine_base') and engine.engine_base and hasattr(engine.engine_base, 'engine_block') and engine.engine_base.engine_block:
                liter = engine.engine_base.engine_block.liter
                cylinders = engine.engine_base.engine_block.cylinders
            fuel_type = engine.fuel_type.name if hasattr(engine, 'fuel_type') and engine.fuel_type else None
            aspiration = engine.aspiration.name if hasattr(engine, 'aspiration') and engine.aspiration else None
            engines.append({'id': engine.engine_config_id, 'liter': liter, 'cylinders': cylinders, 'aspiration': aspiration, 'fuel_type': fuel_type})
        trans_list = []
        for trans in transmissions:
            trans_type = None
            speeds = None
            if hasattr(trans, 'transmission_base') and trans.transmission_base:
                if hasattr(trans.transmission_base, 'transmission_type') and trans.transmission_base.transmission_type:
                    trans_type = trans.transmission_base.transmission_type.name
                if hasattr(trans.transmission_base, 'transmission_num_speeds') and trans.transmission_base.transmission_num_speeds:
                    speeds = trans.transmission_base.transmission_num_speeds.num_speeds
            trans_list.append({'id': trans.transmission_id, 'type': trans_type, 'speeds': speeds})
        make_name = None
        if vehicle.base_vehicle and vehicle.base_vehicle.make:
            make_name = vehicle.base_vehicle.make.name
        return {'id': str(vehicle.id), 'vehicle_id': vehicle.vehicle_id, 'year': vehicle.year, 'make': make_name, 'model': vehicle.model if hasattr(vehicle, 'model') else None, 'submodel': vehicle.submodel.name if vehicle.submodel else None, 'region': vehicle.region.name if vehicle.region else None, 'engines': engines, 'transmissions': trans_list, 'drive_types': [dt.name for dt in drive_types], 'body_styles': [bs.body_type.name for bs in body_styles if hasattr(bs, 'body_type') and bs.body_type]}
    async def get_vehicle_configurations(self, vehicle_id: int) -> Dict[str, List[Dict[str, Any]]]:
        configs = await self.repository.vehicle_repo.get_vehicle_configurations(vehicle_id)
        if not configs:
            raise ResourceNotFoundException(resource_type='Vehicle', resource_id=str(vehicle_id))
        result: Dict[str, List[Dict[str, Any]]] = {'engines': [], 'transmissions': [], 'drive_types': [], 'body_styles': [], 'brake_configs': [], 'wheel_bases': []}
        for engine_data in configs['engines']:
            engine_config = engine_data['config']
            engine_base = engine_data['base']
            fuel_type = engine_data['fuel_type']
            aspiration = engine_data['aspiration']
            power_output = engine_data['power_output']
            result['engines'].append({'id': engine_config.engine_config_id, 'liter': engine_base.liter if engine_base else None, 'cc': engine_base.cc if engine_base else None, 'cid': engine_base.cid if engine_base else None, 'cylinders': engine_base.cylinders if engine_base else None, 'fuel_type': fuel_type.name if fuel_type else None, 'aspiration': aspiration.name if aspiration else None, 'power': {'horsepower': power_output.horsepower if power_output else None, 'kilowatt': power_output.kilowatt if power_output else None}})
        for trans in configs['transmissions']:
            trans_type = None
            speeds = None
            control_type = None
            if hasattr(trans, 'transmission_base') and trans.transmission_base:
                if hasattr(trans.transmission_base, 'transmission_type') and trans.transmission_base.transmission_type:
                    trans_type = trans.transmission_base.transmission_type.name
                if hasattr(trans.transmission_base, 'transmission_num_speeds') and trans.transmission_base.transmission_num_speeds:
                    speeds = trans.transmission_base.transmission_num_speeds.num_speeds
                if hasattr(trans.transmission_base, 'transmission_control_type') and trans.transmission_base.transmission_control_type:
                    control_type = trans.transmission_base.transmission_control_type.name
            manufacturer = trans.transmission_mfr.name if hasattr(trans, 'transmission_mfr') and trans.transmission_mfr else None
            code = trans.transmission_mfr_code.code if hasattr(trans, 'transmission_mfr_code') and trans.transmission_mfr_code else None
            result['transmissions'].append({'id': trans.transmission_id, 'type': trans_type, 'speeds': speeds, 'control_type': control_type, 'manufacturer': manufacturer, 'code': code})
        for dt in configs['drive_types']:
            result['drive_types'].append({'id': dt.drive_type_id, 'name': dt.name})
        for bs in configs['body_styles']:
            body_type = bs.body_type.name if hasattr(bs, 'body_type') and bs.body_type else None
            doors = bs.body_num_doors.num_doors if hasattr(bs, 'body_num_doors') and bs.body_num_doors else None
            result['body_styles'].append({'id': bs.body_style_config_id, 'type': body_type, 'doors': doors})
        for bc in configs['brake_configs']:
            front_type = bc.front_brake_type.name if hasattr(bc, 'front_brake_type') and bc.front_brake_type else None
            rear_type = bc.rear_brake_type.name if hasattr(bc, 'rear_brake_type') and bc.rear_brake_type else None
            system = bc.brake_system.name if hasattr(bc, 'brake_system') and bc.brake_system else None
            abs_type = bc.brake_abs.name if hasattr(bc, 'brake_abs') and bc.brake_abs else None
            result['brake_configs'].append({'id': bc.brake_config_id, 'front_type': front_type, 'rear_type': rear_type, 'system': system, 'abs': abs_type})
        for wb in configs['wheel_bases']:
            result['wheel_bases'].append({'id': wb.wheel_base_id, 'wheel_base': wb.wheel_base, 'wheel_base_metric': wb.wheel_base_metric})
        return result
    async def get_vehicle_configurations2(self, vehicle_id: int) -> Dict[str, List[Dict[str, Any]]]:
        configs = await self.repository.vehicle_repo.get_vehicle_configurations2(vehicle_id)
        if not configs:
            raise ResourceNotFoundException(resource_type='Vehicle', resource_id=str(vehicle_id))
        result: Dict[str, List[Dict[str, Any]]] = {'engines': [], 'transmissions': [], 'drive_types': [], 'body_styles': [], 'brake_configs': [], 'wheel_bases': []}
        for engine in configs['engines']:
            liter = None
            cylinders = None
            if hasattr(engine, 'engine_block') and engine.engine_block:
                liter = engine.engine_block.liter
                cylinders = engine.engine_block.cylinders
            elif hasattr(engine, 'engine_base') and engine.engine_base and hasattr(engine.engine_base, 'engine_block') and engine.engine_base.engine_block:
                liter = engine.engine_base.engine_block.liter
                cylinders = engine.engine_base.engine_block.cylinders
            fuel_type = engine.fuel_type.name if hasattr(engine, 'fuel_type') and engine.fuel_type else None
            aspiration = engine.aspiration.name if hasattr(engine, 'aspiration') and engine.aspiration else None
            horsepower = None
            kilowatt = None
            if hasattr(engine, 'power_output') and engine.power_output:
                horsepower = engine.power_output.horsepower
                kilowatt = engine.power_output.kilowatt
            result['engines'].append({'id': engine.engine_config_id, 'liter': liter, 'cylinders': cylinders, 'fuel_type': fuel_type, 'aspiration': aspiration, 'power': {'horsepower': horsepower, 'kilowatt': kilowatt}})
        for trans in configs['transmissions']:
            trans_type = None
            speeds = None
            control_type = None
            if hasattr(trans, 'transmission_base') and trans.transmission_base:
                if hasattr(trans.transmission_base, 'transmission_type') and trans.transmission_base.transmission_type:
                    trans_type = trans.transmission_base.transmission_type.name
                if hasattr(trans.transmission_base, 'transmission_num_speeds') and trans.transmission_base.transmission_num_speeds:
                    speeds = trans.transmission_base.transmission_num_speeds.num_speeds
                if hasattr(trans.transmission_base, 'transmission_control_type') and trans.transmission_base.transmission_control_type:
                    control_type = trans.transmission_base.transmission_control_type.name
            manufacturer = trans.transmission_mfr.name if hasattr(trans, 'transmission_mfr') and trans.transmission_mfr else None
            code = trans.transmission_mfr_code.code if hasattr(trans, 'transmission_mfr_code') and trans.transmission_mfr_code else None
            result['transmissions'].append({'id': trans.transmission_id, 'type': trans_type, 'speeds': speeds, 'control_type': control_type, 'manufacturer': manufacturer, 'code': code})
        for dt in configs['drive_types']:
            result['drive_types'].append({'id': dt.drive_type_id, 'name': dt.name})
        for bs in configs['body_styles']:
            body_type = bs.body_type.name if hasattr(bs, 'body_type') and bs.body_type else None
            doors = bs.body_num_doors.num_doors if hasattr(bs, 'body_num_doors') and bs.body_num_doors else None
            result['body_styles'].append({'id': bs.body_style_config_id, 'type': body_type, 'doors': doors})
        for bc in configs['brake_configs']:
            front_type = bc.front_brake_type.name if hasattr(bc, 'front_brake_type') and bc.front_brake_type else None
            rear_type = bc.rear_brake_type.name if hasattr(bc, 'rear_brake_type') and bc.rear_brake_type else None
            system = bc.brake_system.name if hasattr(bc, 'brake_system') and bc.brake_system else None
            abs_type = bc.brake_abs.name if hasattr(bc, 'brake_abs') and bc.brake_abs else None
            result['brake_configs'].append({'id': bc.brake_config_id, 'front_type': front_type, 'rear_type': rear_type, 'system': system, 'abs': abs_type})
        for wb in configs['wheel_bases']:
            result['wheel_bases'].append({'id': wb.wheel_base_id, 'wheel_base': wb.wheel_base, 'wheel_base_metric': wb.wheel_base_metric})
        return result
    async def get_engine_base(self, engine_base_id: int) -> Dict[str, Any]:
        engine_base = await self.repository.engine_base_repo.get_by_engine_base_id(engine_base_id)
        if not engine_base:
            raise ResourceNotFoundException(resource_type='EngineBase', resource_id=str(engine_base_id))
        return {'id': engine_base.engine_base_id, 'liter': engine_base.liter, 'cc': engine_base.cc, 'cid': engine_base.cid, 'cylinders': engine_base.cylinders, 'block_type': engine_base.block_type, 'bore_in': engine_base.eng_bore_in, 'bore_metric': engine_base.eng_bore_metric, 'stroke_in': engine_base.eng_stroke_in, 'stroke_metric': engine_base.eng_stroke_metric}
    async def search_engine_bases(self, liter: Optional[str]=None, cylinders: Optional[str]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        result = await self.repository.engine_base_repo.search_by_criteria(liter=liter, cylinders=cylinders, page=page, page_size=page_size)
        engine_bases = []
        for eb in result['items']:
            engine_bases.append({'id': eb.engine_base_id, 'liter': eb.liter, 'cc': eb.cc, 'cylinders': eb.cylinders})
        return {'items': engine_bases, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def get_engine_config_details(self, engine_config_id: int) -> Dict[str, Any]:
        engine_config = await self.repository.engine_config_repo.get_by_engine_config_id(engine_config_id)
        if not engine_config:
            raise ResourceNotFoundException(resource_type='EngineConfig', resource_id=str(engine_config_id))
        engine_base = await self.repository.engine_base_repo.get_by_engine_base_id(engine_config.engine_base_id)
        return {'id': engine_config.engine_config_id, 'engine_base': {'id': engine_base.engine_base_id if engine_base else None, 'liter': engine_base.liter if engine_base else None, 'cylinders': engine_base.cylinders if engine_base else None} if engine_base else None}
    async def get_engine_configs(self, engine_config_id: int) -> Dict[str, Any]:
        engine_details = await self.repository.engine_config_repo.get_full_engine_details(engine_config_id)
        if not engine_details:
            raise ResourceNotFoundException(resource_type='EngineConfig', resource_id=str(engine_config_id))
        return engine_details
    async def search_engine_configs(self, engine_base_id: Optional[int]=None, fuel_type_id: Optional[int]=None, aspiration_id: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        result = await self.repository.engine_config_repo.get_by_criteria(engine_base_id=engine_base_id, fuel_type_id=fuel_type_id, aspiration_id=aspiration_id, page=page, page_size=page_size)
        engine_configs = []
        for ec in result['items']:
            engine_configs.append({'id': ec.engine_config_id, 'engine_base_id': ec.engine_base_id, 'fuel_type_id': ec.fuel_type_id, 'aspiration_id': ec.aspiration_id})
        return {'items': engine_configs, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def get_engine_base2(self, engine_base_id: int) -> Dict[str, Any]:
        engine_base = await self.repository.engine_base2_repo.get_by_engine_base_id(engine_base_id)
        if not engine_base:
            raise ResourceNotFoundException(resource_type='EngineBase2', resource_id=str(engine_base_id))
        engine_block = engine_base.engine_block
        engine_bore_stroke = engine_base.engine_bore_stroke
        return {'id': engine_base.engine_base_id, 'engine_block': {'id': engine_block.engine_block_id if engine_block else None, 'liter': engine_block.liter if engine_block else None, 'cc': engine_block.cc if engine_block else None, 'cid': engine_block.cid if engine_block else None, 'cylinders': engine_block.cylinders if engine_block else None, 'block_type': engine_block.block_type if engine_block else None} if engine_block else None, 'engine_bore_stroke': {'id': engine_bore_stroke.engine_bore_stroke_id if engine_bore_stroke else None, 'bore_in': engine_bore_stroke.bore_in if engine_bore_stroke else None, 'bore_metric': engine_bore_stroke.bore_metric if engine_bore_stroke else None, 'stroke_in': engine_bore_stroke.stroke_in if engine_bore_stroke else None, 'stroke_metric': engine_bore_stroke.stroke_metric if engine_bore_stroke else None} if engine_bore_stroke else None}
    async def search_engine_bases2(self, engine_block_id: Optional[int]=None, engine_bore_stroke_id: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        result = await self.repository.engine_base2_repo.search_by_criteria(engine_block_id=engine_block_id, engine_bore_stroke_id=engine_bore_stroke_id, page=page, page_size=page_size)
        engine_bases = []
        for eb in result['items']:
            engine_block = eb.engine_block
            engine_bases.append({'id': eb.engine_base_id, 'liter': engine_block.liter if engine_block else None, 'cc': engine_block.cc if engine_block else None, 'cylinders': engine_block.cylinders if engine_block else None})
        return {'items': engine_bases, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def get_engine_config2(self, engine_config_id: int) -> Dict[str, Any]:
        engine_details = await self.repository.engine_config2_repo.get_full_engine_details(engine_config_id)
        if not engine_details:
            raise ResourceNotFoundException(resource_type='EngineConfig2', resource_id=str(engine_config_id))
        return engine_details
    async def search_engine_configs2(self, engine_base_id: Optional[int]=None, fuel_type_id: Optional[int]=None, aspiration_id: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        result = await self.repository.engine_config2_repo.get_by_criteria(engine_base_id=engine_base_id, fuel_type_id=fuel_type_id, aspiration_id=aspiration_id, page=page, page_size=page_size)
        engine_configs = []
        for ec in result['items']:
            engine_configs.append({'id': ec.engine_config_id, 'engine_base_id': ec.engine_base_id, 'fuel_type': ec.fuel_type.name if ec.fuel_type else None, 'aspiration': ec.aspiration.name if ec.aspiration else None, 'liter': ec.engine_block.liter if ec.engine_block else None, 'cylinders': ec.engine_block.cylinders if ec.engine_block else None})
        return {'items': engine_configs, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def get_transmission(self, transmission_id: int) -> Dict[str, Any]:
        transmission_details = await self.repository.transmission_repo.get_full_transmission_details(transmission_id)
        if not transmission_details:
            raise ResourceNotFoundException(resource_type='Transmission', resource_id=str(transmission_id))
        return transmission_details
    async def search_transmissions(self, transmission_type_id: Optional[int]=None, transmission_num_speeds_id: Optional[int]=None, transmission_control_type_id: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        result = await self.repository.transmission_repo.get_by_criteria(transmission_type_id=transmission_type_id, transmission_num_speeds_id=transmission_num_speeds_id, transmission_control_type_id=transmission_control_type_id, page=page, page_size=page_size)
        transmissions = []
        for trans in result['items']:
            transmissions.append({'id': trans.transmission_id, 'transmission_base_id': trans.transmission_base_id, 'transmission_mfr_code_id': trans.transmission_mfr_code_id, 'elec_controlled_id': trans.elec_controlled_id, 'transmission_mfr_id': trans.transmission_mfr_id})
        return {'items': transmissions, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def get_drive_types(self) -> List[Dict[str, Any]]:
        drive_types = await self.repository.drive_type_repo.get_all_drive_types()
        return [{'id': dt.drive_type_id, 'name': dt.name} for dt in drive_types]
    async def get_body_style_config(self, body_style_config_id: int) -> Dict[str, Any]:
        body_style_details = await self.repository.body_style_repo.get_full_body_style_details(body_style_config_id)
        if not body_style_details:
            raise ResourceNotFoundException(resource_type='BodyStyleConfig', resource_id=str(body_style_config_id))
        return body_style_details
    async def get_brake_config(self, brake_config_id: int) -> Dict[str, Any]:
        brake_config_details = await self.repository.brake_config_repo.get_full_brake_config_details(brake_config_id)
        if not brake_config_details:
            raise ResourceNotFoundException(resource_type='BrakeConfig', resource_id=str(brake_config_id))
        return brake_config_details
    async def get_wheel_bases(self) -> List[Dict[str, Any]]:
        wheel_bases = await self.repository.wheel_base_repo.get_all_wheel_bases()
        return [{'id': wb.wheel_base_id, 'wheel_base': wb.wheel_base, 'wheel_base_metric': wb.wheel_base_metric} for wb in wheel_bases]