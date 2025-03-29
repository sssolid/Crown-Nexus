from __future__ import annotations
import re
from typing import Dict, List, Tuple
from .exceptions import ParsingError
from .models import PartApplication, PartFitment, Position, PositionGroup, Vehicle
class FitmentParser:
    def __init__(self, model_mappings: Dict[str, List[str]]) -> None:
        self.model_mappings = model_mappings
        self.position_patterns = {'left_right': {re.compile("\\b(?:left|driver[\\'s]* side)\\b", re.IGNORECASE): Position.LEFT, re.compile("\\b(?:right|passenger[\\'s]* side)\\b", re.IGNORECASE): Position.RIGHT, re.compile("\\b(?:left|driver[\\'s]* side).+(?:right|passenger[\\'s]* side)\\b", re.IGNORECASE): 'BOTH', re.compile("\\b(?:right|passenger[\\'s]* side).+(?:left|driver[\\'s]* side)\\b", re.IGNORECASE): 'BOTH', re.compile('\\b(?:left|right)\\b', re.IGNORECASE): 'BOTH', re.compile('\\b(?:left or right)\\b', re.IGNORECASE): 'BOTH', re.compile('\\b(?:left and right)\\b', re.IGNORECASE): 'BOTH'}, 'front_rear': {re.compile('\\bfront\\b', re.IGNORECASE): Position.FRONT, re.compile('\\brear\\b', re.IGNORECASE): Position.REAR, re.compile('\\bfront.+rear\\b', re.IGNORECASE): 'BOTH', re.compile('\\brear.+front\\b', re.IGNORECASE): 'BOTH', re.compile('\\b(?:front|rear)\\b', re.IGNORECASE): 'BOTH', re.compile('\\b(?:front or rear)\\b', re.IGNORECASE): 'BOTH', re.compile('\\b(?:front and rear)\\b', re.IGNORECASE): 'BOTH'}, 'upper_lower': {re.compile('\\bupper\\b', re.IGNORECASE): Position.UPPER, re.compile('\\blower\\b', re.IGNORECASE): Position.LOWER, re.compile('\\bupper.+lower\\b', re.IGNORECASE): 'BOTH', re.compile('\\blower.+upper\\b', re.IGNORECASE): 'BOTH', re.compile('\\b(?:upper|lower)\\b', re.IGNORECASE): 'BOTH', re.compile('\\b(?:upper or lower)\\b', re.IGNORECASE): 'BOTH', re.compile('\\b(?:upper and lower)\\b', re.IGNORECASE): 'BOTH'}, 'inner_outer': {re.compile('\\binner\\b', re.IGNORECASE): Position.INNER, re.compile('\\bouter\\b', re.IGNORECASE): Position.OUTER, re.compile('\\binner.+outer\\b', re.IGNORECASE): 'BOTH', re.compile('\\bouter.+inner\\b', re.IGNORECASE): 'BOTH', re.compile('\\b(?:inner|outer)\\b', re.IGNORECASE): 'BOTH', re.compile('\\b(?:inner or outer)\\b', re.IGNORECASE): 'BOTH', re.compile('\\b(?:inner and outer)\\b', re.IGNORECASE): 'BOTH'}}
    def parse_application(self, application_text: str) -> PartApplication:
        if application_text.endswith(';'):
            application_text = application_text[:-1]
        try:
            return PartApplication(raw_text=application_text)
        except Exception as e:
            raise ParsingError(f'Failed to parse application text: {str(e)}') from e
    def extract_year_range(self, year_text: str) -> Tuple[int, int]:
        pattern = '(\\d{4})-(\\d{4})'
        match = re.match(pattern, year_text)
        if not match:
            raise ParsingError(f'Invalid year range format: {year_text}')
        start_year = int(match.group(1))
        end_year = int(match.group(2))
        if start_year > end_year:
            raise ParsingError(f'Invalid year range: {start_year} > {end_year}')
        return (start_year, end_year)
    def expand_year_range(self, start_year: int, end_year: int) -> List[int]:
        return list(range(start_year, end_year + 1))
    def find_model_mapping(self, vehicle_text: str) -> List[Dict[str, str]]:
        patterns = sorted(self.model_mappings.keys(), key=len, reverse=True)
        for pattern in patterns:
            if pattern in vehicle_text:
                mappings = self.model_mappings[pattern]
                result = []
                for mapping in mappings:
                    parts = mapping.split('|')
                    if len(parts) != 3:
                        continue
                    make = parts[0]
                    vehicle_code = parts[1]
                    model = parts[2]
                    if make and model:
                        result.append({'make': make, 'model': model})
                    elif make and vehicle_code and (not model):
                        model_value = vehicle_code if vehicle_code else make
                        result.append({'make': make, 'model': model_value})
                    elif make and (not vehicle_code) and (not model):
                        result.append({'make': make, 'model': make})
                    elif not make and (not vehicle_code) and model:
                        result.append({'make': model, 'model': model})
                    elif not make and vehicle_code and (not model):
                        result.append({'make': vehicle_code, 'model': vehicle_code})
                if result:
                    return result
        if 'universal' in vehicle_text.lower():
            return [{'make': 'Universal', 'model': 'Universal'}]
        raise ParsingError(f'No model mapping found for: {vehicle_text}')
    def extract_positions(self, position_text: str) -> List[PositionGroup]:
        position_values = {'left_right': Position.NA, 'front_rear': Position.NA, 'upper_lower': Position.NA, 'inner_outer': Position.NA}
        multiple_positions = []
        for position_type, patterns in self.position_patterns.items():
            for pattern, value in patterns.items():
                if pattern.search(position_text):
                    if value == 'BOTH':
                        if position_type == 'left_right':
                            multiple_positions.append(('left_right', [Position.LEFT, Position.RIGHT]))
                        elif position_type == 'front_rear':
                            multiple_positions.append(('front_rear', [Position.FRONT, Position.REAR]))
                        elif position_type == 'upper_lower':
                            multiple_positions.append(('upper_lower', [Position.UPPER, Position.LOWER]))
                        elif position_type == 'inner_outer':
                            multiple_positions.append(('inner_outer', [Position.INNER, Position.OUTER]))
                    else:
                        position_values[position_type] = value
                    break
        if not multiple_positions:
            return [PositionGroup(front_rear=position_values['front_rear'], left_right=position_values['left_right'], upper_lower=position_values['upper_lower'], inner_outer=position_values['inner_outer'])]
        position_groups = []
        current_group = PositionGroup(front_rear=position_values['front_rear'], left_right=position_values['left_right'], upper_lower=position_values['upper_lower'], inner_outer=position_values['inner_outer'])
        self._expand_position_combinations(position_groups, current_group, multiple_positions, 0)
        return position_groups
    def _expand_position_combinations(self, result: List[PositionGroup], current_group: PositionGroup, multiple_positions: List[Tuple[str, List[Position]]], index: int) -> None:
        if index >= len(multiple_positions):
            result.append(PositionGroup(front_rear=current_group.front_rear, left_right=current_group.left_right, upper_lower=current_group.upper_lower, inner_outer=current_group.inner_outer))
            return
        position_type, values = multiple_positions[index]
        for value in values:
            new_group = PositionGroup(front_rear=current_group.front_rear, left_right=current_group.left_right, upper_lower=current_group.upper_lower, inner_outer=current_group.inner_outer)
            if position_type == 'left_right':
                new_group.left_right = value
            elif position_type == 'front_rear':
                new_group.front_rear = value
            elif position_type == 'upper_lower':
                new_group.upper_lower = value
            elif position_type == 'inner_outer':
                new_group.inner_outer = value
            self._expand_position_combinations(result, new_group, multiple_positions, index + 1)
    def process_application(self, part_app: PartApplication) -> List[PartFitment]:
        if not part_app.year_range or not part_app.vehicle_text:
            raise ParsingError('Missing year range or vehicle text in application')
        years = self.expand_year_range(part_app.year_range[0], part_app.year_range[1])
        model_mappings = self.find_model_mapping(part_app.vehicle_text)
        position_groups = []
        if part_app.position_text:
            position_groups = self.extract_positions(part_app.position_text)
        else:
            position_groups = [PositionGroup()]
        fitments = []
        for year in years:
            for model_map in model_mappings:
                for position_group in position_groups:
                    vehicle = Vehicle(year=year, make=model_map['make'], model=model_map['model'])
                    fitment = PartFitment(vehicle=vehicle, positions=position_group)
                    fitments.append(fitment)
        return fitments