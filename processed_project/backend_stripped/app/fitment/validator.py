from __future__ import annotations
from app.logging import get_logger
from typing import Dict, List, Set
from .models import PartFitment, PCDBPosition, Position, ValidationResult, ValidationStatus, VCDBVehicle
logger = get_logger('app.fitment.validator')
class FitmentValidator:
    def __init__(self, part_terminology_id: int, pcdb_positions: List[PCDBPosition]) -> None:
        self.part_terminology_id = part_terminology_id
        self.pcdb_positions = pcdb_positions
        self.position_index: Dict[str, Dict[Position, Set[int]]] = {'front_rear': {}, 'left_right': {}, 'upper_lower': {}, 'inner_outer': {}}
        for pos in pcdb_positions:
            self._index_position(pos)
    def _index_position(self, position: PCDBPosition) -> None:
        if position.front_rear:
            pos_value = Position(position.front_rear)
            if pos_value not in self.position_index['front_rear']:
                self.position_index['front_rear'][pos_value] = set()
            self.position_index['front_rear'][pos_value].add(position.id)
        if position.left_right:
            pos_value = Position(position.left_right)
            if pos_value not in self.position_index['left_right']:
                self.position_index['left_right'][pos_value] = set()
            self.position_index['left_right'][pos_value].add(position.id)
        if position.upper_lower:
            pos_value = Position(position.upper_lower)
            if pos_value not in self.position_index['upper_lower']:
                self.position_index['upper_lower'][pos_value] = set()
            self.position_index['upper_lower'][pos_value].add(position.id)
        if position.inner_outer:
            pos_value = Position(position.inner_outer)
            if pos_value not in self.position_index['inner_outer']:
                self.position_index['inner_outer'][pos_value] = set()
            self.position_index['inner_outer'][pos_value].add(position.id)
    def validate_fitment(self, fitment: PartFitment, available_vehicles: List[VCDBVehicle]) -> ValidationResult:
        issues = []
        vehicle_result = self._validate_vehicle(fitment, available_vehicles)
        if vehicle_result.status == ValidationStatus.ERROR:
            return vehicle_result
        elif vehicle_result.status == ValidationStatus.WARNING:
            issues.append(vehicle_result.message)
        position_result = self._validate_positions(fitment)
        if position_result.status == ValidationStatus.ERROR:
            return position_result
        elif position_result.status == ValidationStatus.WARNING:
            issues.append(position_result.message)
        if issues:
            return ValidationResult(status=ValidationStatus.WARNING, message='; '.join(issues), fitment=fitment, original_text=fitment.vehicle.full_name)
        return ValidationResult(status=ValidationStatus.VALID, message='Fitment is valid', fitment=fitment, original_text=fitment.vehicle.full_name)
    def _validate_vehicle(self, fitment: PartFitment, available_vehicles: List[VCDBVehicle]) -> ValidationResult:
        exact_matches = []
        partial_matches = []
        for vehicle in available_vehicles:
            if vehicle.year == fitment.vehicle.year and vehicle.make.lower() == fitment.vehicle.make.lower() and (vehicle.model.lower() == fitment.vehicle.model.lower()):
                if fitment.vehicle.submodel and vehicle.submodel:
                    if fitment.vehicle.submodel.lower() == vehicle.submodel.lower():
                        exact_matches.append(vehicle)
                elif not fitment.vehicle.submodel and vehicle.submodel:
                    partial_matches.append(vehicle)
                elif not vehicle.submodel:
                    exact_matches.append(vehicle)
        if exact_matches:
            fitment.vcdb_vehicle_id = exact_matches[0].id
            return ValidationResult(status=ValidationStatus.VALID, message='Exact vehicle match found', fitment=fitment, original_text=fitment.vehicle.full_name)
        if partial_matches:
            fitment.vcdb_vehicle_id = partial_matches[0].id
            submodels = ', '.join((v.submodel for v in partial_matches if v.submodel))
            return ValidationResult(status=ValidationStatus.WARNING, message=f'No exact vehicle match found. Possible submodels: {submodels}', fitment=fitment, original_text=fitment.vehicle.full_name, suggestions=[v.submodel for v in partial_matches if v.submodel])
        return ValidationResult(status=ValidationStatus.ERROR, message='No matching vehicle found in VCDB', fitment=fitment, original_text=fitment.vehicle.full_name)
    def _validate_positions(self, fitment: PartFitment) -> ValidationResult:
        positions = fitment.positions
        valid_position_ids = set()
        if positions.front_rear != Position.NA:
            if positions.front_rear not in self.position_index['front_rear']:
                if positions.front_rear == Position.VARIES:
                    return ValidationResult(status=ValidationStatus.WARNING, message='Front/Rear position varies with application - manual review needed', fitment=fitment, original_text=fitment.vehicle.full_name)
                else:
                    return ValidationResult(status=ValidationStatus.ERROR, message=f'Invalid Front/Rear position: {positions.front_rear}', fitment=fitment, original_text=fitment.vehicle.full_name)
            else:
                valid_position_ids.update(self.position_index['front_rear'][positions.front_rear])
        if positions.left_right != Position.NA:
            if positions.left_right not in self.position_index['left_right']:
                if positions.left_right == Position.VARIES:
                    return ValidationResult(status=ValidationStatus.WARNING, message='Left/Right position varies with application - manual review needed', fitment=fitment, original_text=fitment.vehicle.full_name)
                else:
                    return ValidationResult(status=ValidationStatus.ERROR, message=f'Invalid Left/Right position: {positions.left_right}', fitment=fitment, original_text=fitment.vehicle.full_name)
            else:
                valid_position_ids.update(self.position_index['left_right'][positions.left_right])
        if positions.upper_lower != Position.NA:
            if positions.upper_lower not in self.position_index['upper_lower']:
                if positions.upper_lower == Position.VARIES:
                    return ValidationResult(status=ValidationStatus.WARNING, message='Upper/Lower position varies with application - manual review needed', fitment=fitment, original_text=fitment.vehicle.full_name)
                else:
                    return ValidationResult(status=ValidationStatus.ERROR, message=f'Invalid Upper/Lower position: {positions.upper_lower}', fitment=fitment, original_text=fitment.vehicle.full_name)
            else:
                valid_position_ids.update(self.position_index['upper_lower'][positions.upper_lower])
        if positions.inner_outer != Position.NA:
            if positions.inner_outer not in self.position_index['inner_outer']:
                if positions.inner_outer == Position.VARIES:
                    return ValidationResult(status=ValidationStatus.WARNING, message='Inner/Outer position varies with application - manual review needed', fitment=fitment, original_text=fitment.vehicle.full_name)
                else:
                    return ValidationResult(status=ValidationStatus.ERROR, message=f'Invalid Inner/Outer position: {positions.inner_outer}', fitment=fitment, original_text=fitment.vehicle.full_name)
            else:
                valid_position_ids.update(self.position_index['inner_outer'][positions.inner_outer])
        if not valid_position_ids and any([positions.front_rear != Position.NA, positions.left_right != Position.NA, positions.upper_lower != Position.NA, positions.inner_outer != Position.NA]):
            return ValidationResult(status=ValidationStatus.ERROR, message='No valid positions found for this part terminology', fitment=fitment, original_text=fitment.vehicle.full_name)
        fitment.pcdb_position_ids = list(valid_position_ids)
        return ValidationResult(status=ValidationStatus.VALID, message='Positions are valid', fitment=fitment, original_text=fitment.vehicle.full_name)