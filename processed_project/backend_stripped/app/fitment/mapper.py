from __future__ import annotations
from functools import lru_cache
from typing import Any, Dict, List, Optional
from app.logging import get_logger
from .db import FitmentDBService
from .exceptions import MappingError
from .models import PartTerminology, PCDBPosition, ValidationResult, ValidationStatus, VCDBVehicle
from .parser import FitmentParser
from .validator import FitmentValidator
logger = get_logger('app.fitment.mapper')
class FitmentMappingEngine:
    def __init__(self, db_service: FitmentDBService) -> None:
        self.db_service = db_service
        self.model_mappings: Dict[str, List[str]] = {}
        self.parser: Optional[FitmentParser] = None
    def configure(self, model_mappings_path: str) -> None:
        self.model_mappings = self.db_service.load_model_mappings_from_excel(model_mappings_path)
        self.parser = FitmentParser(self.model_mappings)
    @lru_cache(maxsize=100)
    def get_part_terminology(self, terminology_id: int) -> PartTerminology:
        try:
            return self.db_service.get_pcdb_part_terminology(terminology_id)
        except Exception as e:
            raise MappingError(f'Failed to get part terminology: {str(e)}') from e
    @lru_cache(maxsize=100)
    def get_pcdb_positions(self, terminology_id: int) -> List[PCDBPosition]:
        try:
            terminology = self.get_part_terminology(terminology_id)
            return self.db_service.get_pcdb_positions(terminology.valid_positions)
        except Exception as e:
            raise MappingError(f'Failed to get PCDB positions: {str(e)}') from e
    def get_vcdb_vehicles(self, year: Optional[int]=None, make: Optional[str]=None, model: Optional[str]=None) -> List[VCDBVehicle]:
        try:
            return self.db_service.get_vcdb_vehicles(year, make, model)
        except Exception as e:
            raise MappingError(f'Failed to get VCDB vehicles: {str(e)}') from e
    def process_application(self, application_text: str, terminology_id: int) -> List[ValidationResult]:
        if not self.parser:
            raise MappingError('Mapping engine not configured')
        try:
            part_app = self.parser.parse_application(application_text)
            fitments = self.parser.process_application(part_app)
            pcdb_positions = self.get_pcdb_positions(terminology_id)
            validator = FitmentValidator(terminology_id, pcdb_positions)
            validation_results = []
            for fitment in fitments:
                vehicles = self.get_vcdb_vehicles(year=fitment.vehicle.year, make=fitment.vehicle.make, model=fitment.vehicle.model)
                result = validator.validate_fitment(fitment, vehicles)
                validation_results.append(result)
            return validation_results
        except Exception as e:
            logger.error(f'Error processing application: {str(e)}')
            raise MappingError(f'Failed to process application: {str(e)}') from e
    def batch_process_applications(self, application_texts: List[str], terminology_id: int) -> Dict[str, List[ValidationResult]]:
        results = {}
        for text in application_texts:
            try:
                results[text] = self.process_application(text, terminology_id)
            except Exception as e:
                logger.error(f"Error processing application '{text}': {str(e)}")
                results[text] = [ValidationResult(status=ValidationStatus.ERROR, message=f'Processing error: {str(e)}', original_text=text, fitment=None)]
        return results
    def serialize_validation_results(self, results: List[ValidationResult]) -> List[Dict[str, Any]]:
        serialized = []
        for result in results:
            status_str = result.status.name
            fitment_dict = None
            if result.fitment:
                fitment_dict = {'vehicle': {'year': result.fitment.vehicle.year, 'make': result.fitment.vehicle.make, 'model': result.fitment.vehicle.model, 'submodel': result.fitment.vehicle.submodel, 'engine': result.fitment.vehicle.engine, 'transmission': result.fitment.vehicle.transmission, 'attributes': result.fitment.vehicle.attributes}, 'positions': {'front_rear': result.fitment.positions.front_rear.value, 'left_right': result.fitment.positions.left_right.value, 'upper_lower': result.fitment.positions.upper_lower.value, 'inner_outer': result.fitment.positions.inner_outer.value}, 'vcdb_vehicle_id': result.fitment.vcdb_vehicle_id, 'pcdb_position_ids': result.fitment.pcdb_position_ids}
            serialized_result = {'status': status_str, 'message': result.message, 'original_text': result.original_text, 'suggestions': result.suggestions, 'fitment': fitment_dict}
            serialized.append(serialized_result)
        return serialized
    async def save_mapping_results(self, product_id: str, results: List[ValidationResult]) -> bool:
        try:
            valid_results = [r for r in results if r.status != ValidationStatus.ERROR and r.fitment is not None]
            fitments = []
            for result in valid_results:
                if result.fitment is None:
                    continue
                fitment_dict = {'vcdb_vehicle_id': result.fitment.vcdb_vehicle_id, 'pcdb_position_ids': result.fitment.pcdb_position_ids, 'year': result.fitment.vehicle.year, 'make': result.fitment.vehicle.make, 'model': result.fitment.vehicle.model, 'submodel': result.fitment.vehicle.submodel, 'notes': result.message if result.status == ValidationStatus.WARNING else None}
                fitments.append(fitment_dict)
            return await self.db_service.save_fitment_results(product_id, fitments)
        except Exception as e:
            logger.error(f'Error saving mapping results: {str(e)}')
            raise MappingError(f'Failed to save mapping results: {str(e)}') from e
    def configure_from_file(self, model_mappings_path: str) -> None:
        self.model_mappings = self.db_service.load_model_mappings_from_json(model_mappings_path)
        self.parser = FitmentParser(self.model_mappings)
    async def configure_from_database(self) -> None:
        self.model_mappings = await self.db_service.get_model_mappings()
        self.parser = FitmentParser(self.model_mappings)
    async def refresh_mappings(self) -> None:
        await self.configure_from_database()