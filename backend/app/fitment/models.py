"""
Fitment data models for the Crown Nexus platform.

This module contains Pydantic models for representing fitment data,
VCDB and PCDB entities, and validation schemas for part application strings.
"""

from __future__ import annotations

import re
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Position(str, Enum):
    """Automotive part position enumeration."""

    FRONT = "Front"
    REAR = "Rear"
    LEFT = "Left"
    RIGHT = "Right"
    UPPER = "Upper"
    LOWER = "Lower"
    INNER = "Inner"
    OUTER = "Outer"
    CENTER = "Center"
    NA = "N/A"
    VARIES = "Varies with Application"


class PositionGroup(BaseModel):
    """Group of positions for a part."""

    front_rear: Position = Position.NA
    left_right: Position = Position.NA
    upper_lower: Position = Position.NA
    inner_outer: Position = Position.NA


class Vehicle(BaseModel):
    """Vehicle information model."""

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
        """Generate a complete vehicle description."""
        name = f"{self.year} {self.make} {self.model}"
        if self.submodel:
            name += f" {self.submodel}"
        return name


class PartFitment(BaseModel):
    """Represents a vehicle fitment for a specific part."""

    vehicle: Vehicle
    positions: PositionGroup
    additional_attributes: Dict[str, str] = Field(default_factory=dict)
    vcdb_vehicle_id: Optional[int] = None
    pcdb_position_ids: List[int] = Field(default_factory=list)
    notes: Optional[str] = None


class PartApplication(BaseModel):
    """Raw part application string with parsing capabilities."""

    raw_text: str
    year_range: Optional[tuple[int, int]] = None
    vehicle_text: Optional[str] = None
    position_text: Optional[str] = None
    additional_notes: Optional[str] = None

    @model_validator(mode="after")
    def parse_application(self) -> "PartApplication":
        """Parse the raw application text into structured components."""
        # Simple parsing of year range pattern like "2005-2010"
        year_pattern = r"^(\d{4})-(\d{4})"
        year_match = re.match(year_pattern, self.raw_text)

        if year_match:
            self.year_range = (int(year_match.group(1)), int(year_match.group(2)))

            # Extract the rest after year range
            rest = self.raw_text[year_match.end() :].strip()

            # Check for position information in parentheses
            position_pattern = r"\((.*?)\)"
            position_match = re.search(position_pattern, rest)

            if position_match:
                self.position_text = position_match.group(1).strip()
                # Get vehicle text (everything before the position)
                self.vehicle_text = rest[: position_match.start()].strip()
                # Get any additional text after the position
                if position_match.end() < len(rest):
                    self.additional_notes = rest[position_match.end() :].strip()
            else:
                # No position found, assume everything is vehicle text
                self.vehicle_text = rest

        return self


class ModelMapping(BaseModel):
    """Database model mapping rule."""

    id: Optional[int] = None
    pattern: str
    mapping: str
    priority: int = 0
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def make(self) -> str:
        """Extract make from mapping string."""
        parts = self.mapping.split("|")
        return parts[0] if len(parts) > 0 else ""

    @property
    def vehicle_code(self) -> str:
        """Extract vehicle code from mapping string."""
        parts = self.mapping.split("|")
        return parts[1] if len(parts) > 1 else ""

    @property
    def model(self) -> str:
        """Extract model from mapping string."""
        parts = self.mapping.split("|")
        return parts[2] if len(parts) > 2 else ""


class MappingRule(BaseModel):
    """Rule for mapping vehicle model text to structured data."""

    pattern: str
    make: str
    models: List[Dict[str, str]]
    priority: int = 0


class ValidationStatus(Enum):
    """Status of a validation result."""

    VALID = auto()
    WARNING = auto()
    ERROR = auto()


class ValidationResult(BaseModel):
    """Result of validating a part fitment."""

    status: ValidationStatus
    message: str
    fitment: Optional[PartFitment] = None
    original_text: str
    suggestions: List[str] = Field(default_factory=list)


class PartTerminology(BaseModel):
    """PCDB part terminology information."""

    id: int
    name: str
    category_id: int
    subcategory_id: int
    valid_positions: List[int]


class PCDBPosition(BaseModel):
    """PCDB position information."""

    id: int
    name: str
    front_rear: Optional[Literal["Front", "Rear", "N/A"]] = None
    left_right: Optional[Literal["Left", "Right", "N/A"]] = None
    upper_lower: Optional[Literal["Upper", "Lower", "N/A"]] = None
    inner_outer: Optional[Literal["Inner", "Outer", "N/A"]] = None


class VCDBVehicle(BaseModel):
    """VCDB vehicle information."""

    id: int
    base_vehicle_id: int
    submodel_id: Optional[int] = None
    region_id: Optional[int] = None
    year: int
    make: str
    model: str
    submodel: Optional[str] = None
