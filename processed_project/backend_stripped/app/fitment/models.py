from __future__ import annotations
import re
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
class Position(str, Enum):
    FRONT = 'Front'
    REAR = 'Rear'
    LEFT = 'Left'
    RIGHT = 'Right'
    UPPER = 'Upper'
    LOWER = 'Lower'
    INNER = 'Inner'
    OUTER = 'Outer'
    CENTER = 'Center'
    NA = 'N/A'
    VARIES = 'Varies with Application'
class PositionGroup(BaseModel):
    front_rear: Position = Position.NA
    left_right: Position = Position.NA
    upper_lower: Position = Position.NA
    inner_outer: Position = Position.NA
class Vehicle(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    year: int
    make: str
    model: str
    submodel: Optional[str] = None
    engine: Optional[str] = None
    transmission: Optional[str] = None
    attributes: Dict[str, str] = Field(default_factory=dict)
    @property
    def full_name(self) -> str:
        name = f'{self.year} {self.make} {self.model}'
        if self.submodel:
            name += f' {self.submodel}'
        return name
class PartFitment(BaseModel):
    vehicle: Vehicle
    positions: PositionGroup
    additional_attributes: Dict[str, str] = Field(default_factory=dict)
    vcdb_vehicle_id: Optional[int] = None
    pcdb_position_ids: List[int] = Field(default_factory=list)
    notes: Optional[str] = None
class PartApplication(BaseModel):
    raw_text: str
    year_range: Optional[tuple[int, int]] = None
    vehicle_text: Optional[str] = None
    position_text: Optional[str] = None
    additional_notes: Optional[str] = None
    @model_validator(mode='after')
    def parse_application(self) -> 'PartApplication':
        year_pattern = '^(\\d{4})-(\\d{4})'
        year_match = re.match(year_pattern, self.raw_text)
        if year_match:
            self.year_range = (int(year_match.group(1)), int(year_match.group(2)))
            rest = self.raw_text[year_match.end():].strip()
            position_pattern = '\\((.*?)\\)'
            position_match = re.search(position_pattern, rest)
            if position_match:
                self.position_text = position_match.group(1).strip()
                self.vehicle_text = rest[:position_match.start()].strip()
                if position_match.end() < len(rest):
                    self.additional_notes = rest[position_match.end():].strip()
            else:
                self.vehicle_text = rest
        return self
class ModelMapping(BaseModel):
    id: Optional[int] = None
    pattern: str
    mapping: str
    priority: int = 0
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    @property
    def make(self) -> str:
        parts = self.mapping.split('|')
        return parts[0] if len(parts) > 0 else ''
    @property
    def vehicle_code(self) -> str:
        parts = self.mapping.split('|')
        return parts[1] if len(parts) > 1 else ''
    @property
    def model(self) -> str:
        parts = self.mapping.split('|')
        return parts[2] if len(parts) > 2 else ''
class MappingRule(BaseModel):
    pattern: str
    make: str
    models: List[Dict[str, str]]
    priority: int = 0
class ValidationStatus(Enum):
    VALID = auto()
    WARNING = auto()
    ERROR = auto()
class ValidationResult(BaseModel):
    status: ValidationStatus
    message: str
    fitment: Optional[PartFitment] = None
    original_text: str
    suggestions: List[str] = Field(default_factory=list)
class PartTerminology(BaseModel):
    id: int
    name: str
    category_id: int
    subcategory_id: int
    valid_positions: List[int]
class PCDBPosition(BaseModel):
    id: int
    name: str
    front_rear: Optional[Literal['Front', 'Rear', 'N/A']] = None
    left_right: Optional[Literal['Left', 'Right', 'N/A']] = None
    upper_lower: Optional[Literal['Upper', 'Lower', 'N/A']] = None
    inner_outer: Optional[Literal['Inner', 'Outer', 'N/A']] = None
class VCDBVehicle(BaseModel):
    id: int
    base_vehicle_id: int
    submodel_id: Optional[int] = None
    region_id: Optional[int] = None
    year: int
    make: str
    model: str
    submodel: Optional[str] = None