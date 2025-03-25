"""
Parser for fitment application strings.

This module provides functionality to parse various formats of
fitment application strings into structured data.
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from .exceptions import ParsingError
from .models import (
    PartApplication,
    PartFitment,
    Position,
    PositionGroup,
    Vehicle,
)


class FitmentParser:
    """Parser for fitment strings with configurable rules."""

    def __init__(self, model_mappings: Dict[str, List[str]]) -> None:
        """
        Initialize the parser with model mappings.

        Args:
            model_mappings: Dictionary mapping vehicle model text to structured make/model data
        """
        self.model_mappings = model_mappings

        # Common position patterns
        self.position_patterns = {
            "left_right": {
                re.compile(
                    r"\b(?:left|driver[\'s]* side)\b", re.IGNORECASE
                ): Position.LEFT,
                re.compile(
                    r"\b(?:right|passenger[\'s]* side)\b", re.IGNORECASE
                ): Position.RIGHT,
                re.compile(
                    r"\b(?:left|driver[\'s]* side).+(?:right|passenger[\'s]* side)\b",
                    re.IGNORECASE,
                ): "BOTH",
                re.compile(
                    r"\b(?:right|passenger[\'s]* side).+(?:left|driver[\'s]* side)\b",
                    re.IGNORECASE,
                ): "BOTH",
                re.compile(r"\b(?:left|right)\b", re.IGNORECASE): "BOTH",
                re.compile(r"\b(?:left or right)\b", re.IGNORECASE): "BOTH",
                re.compile(r"\b(?:left and right)\b", re.IGNORECASE): "BOTH",
            },
            "front_rear": {
                re.compile(r"\bfront\b", re.IGNORECASE): Position.FRONT,
                re.compile(r"\brear\b", re.IGNORECASE): Position.REAR,
                re.compile(r"\bfront.+rear\b", re.IGNORECASE): "BOTH",
                re.compile(r"\brear.+front\b", re.IGNORECASE): "BOTH",
                re.compile(r"\b(?:front|rear)\b", re.IGNORECASE): "BOTH",
                re.compile(r"\b(?:front or rear)\b", re.IGNORECASE): "BOTH",
                re.compile(r"\b(?:front and rear)\b", re.IGNORECASE): "BOTH",
            },
            "upper_lower": {
                re.compile(r"\bupper\b", re.IGNORECASE): Position.UPPER,
                re.compile(r"\blower\b", re.IGNORECASE): Position.LOWER,
                re.compile(r"\bupper.+lower\b", re.IGNORECASE): "BOTH",
                re.compile(r"\blower.+upper\b", re.IGNORECASE): "BOTH",
                re.compile(r"\b(?:upper|lower)\b", re.IGNORECASE): "BOTH",
                re.compile(r"\b(?:upper or lower)\b", re.IGNORECASE): "BOTH",
                re.compile(r"\b(?:upper and lower)\b", re.IGNORECASE): "BOTH",
            },
            "inner_outer": {
                re.compile(r"\binner\b", re.IGNORECASE): Position.INNER,
                re.compile(r"\bouter\b", re.IGNORECASE): Position.OUTER,
                re.compile(r"\binner.+outer\b", re.IGNORECASE): "BOTH",
                re.compile(r"\bouter.+inner\b", re.IGNORECASE): "BOTH",
                re.compile(r"\b(?:inner|outer)\b", re.IGNORECASE): "BOTH",
                re.compile(r"\b(?:inner or outer)\b", re.IGNORECASE): "BOTH",
                re.compile(r"\b(?:inner and outer)\b", re.IGNORECASE): "BOTH",
            },
        }

    def parse_application(self, application_text: str) -> PartApplication:
        """
        Parse a raw part application text into a structured PartApplication object.

        Args:
            application_text: Raw application text string

        Returns:
            PartApplication with extracted components

        Raises:
            ParsingError: If the application text cannot be parsed
        """
        # Remove trailing semicolon if present
        if application_text.endswith(";"):
            application_text = application_text[:-1]

        try:
            return PartApplication(raw_text=application_text)
        except Exception as e:
            raise ParsingError(f"Failed to parse application text: {str(e)}") from e

    def extract_year_range(self, year_text: str) -> Tuple[int, int]:
        """
        Extract start and end years from a year range string.

        Args:
            year_text: Year range text (e.g., "2005-2010")

        Returns:
            Tuple of (start_year, end_year)

        Raises:
            ParsingError: If the year range cannot be parsed
        """
        pattern = r"(\d{4})-(\d{4})"
        match = re.match(pattern, year_text)

        if not match:
            raise ParsingError(f"Invalid year range format: {year_text}")

        start_year = int(match.group(1))
        end_year = int(match.group(2))

        if start_year > end_year:
            raise ParsingError(f"Invalid year range: {start_year} > {end_year}")

        return (start_year, end_year)

    def expand_year_range(self, start_year: int, end_year: int) -> List[int]:
        """
        Expand a year range into a list of individual years.

        Args:
            start_year: First year in range
            end_year: Last year in range

        Returns:
            List of all years in the range (inclusive)
        """
        return list(range(start_year, end_year + 1))

    def find_model_mapping(self, vehicle_text: str) -> List[Dict[str, str]]:
        """
        Find the appropriate model mapping for the vehicle text.

        Args:
            vehicle_text: Text describing the vehicle model

        Returns:
            List of dictionaries with make, model mappings

        Raises:
            ParsingError: If no mapping is found
        """
        # Sort patterns by length (descending) to prioritize longer matches
        patterns = sorted(self.model_mappings.keys(), key=len, reverse=True)

        for pattern in patterns:
            if pattern in vehicle_text:
                mappings = self.model_mappings[pattern]
                result = []

                for mapping in mappings:
                    parts = mapping.split("|")
                    if len(parts) != 3:
                        # Skip invalid format
                        continue

                    # Handle various cases flexibly
                    make = parts[0]
                    vehicle_code = parts[1]
                    model = parts[2]

                    # Case 1: Standard "Make|VehicleCode|Model"
                    if make and model:
                        result.append({"make": make, "model": model})

                    # Case 2: "Make|VehicleCode|" (missing model)
                    elif make and vehicle_code and not model:
                        # Use vehicle code as model if available, otherwise use make
                        model_value = vehicle_code if vehicle_code else make
                        result.append({"make": make, "model": model_value})

                    # Case 3: "Make||" (only make, like "Universal||")
                    elif make and not vehicle_code and not model:
                        result.append({"make": make, "model": make})

                    # Case 4: "||Model" (only model)
                    elif not make and not vehicle_code and model:
                        result.append({"make": model, "model": model})

                    # Case 5: "|VehicleCode|" (only vehicle code)
                    elif not make and vehicle_code and not model:
                        result.append({"make": vehicle_code, "model": vehicle_code})

                if result:
                    return result

        # Special fallback for Universal parts
        if "universal" in vehicle_text.lower():
            return [{"make": "Universal", "model": "Universal"}]

        raise ParsingError(f"No model mapping found for: {vehicle_text}")

    def extract_positions(self, position_text: str) -> List[PositionGroup]:
        """
        Extract position information from the position text.

        Args:
            position_text: Text describing position (e.g., "Left or Right Front Upper")

        Returns:
            List of PositionGroup objects representing all position combinations
        """
        # Initialize with default N/A
        position_values = {
            "left_right": Position.NA,
            "front_rear": Position.NA,
            "upper_lower": Position.NA,
            "inner_outer": Position.NA,
        }

        multiple_positions = []

        # Check each position pattern
        for position_type, patterns in self.position_patterns.items():
            for pattern, value in patterns.items():
                if pattern.search(position_text):
                    if value == "BOTH":
                        if position_type == "left_right":
                            multiple_positions.append(
                                ("left_right", [Position.LEFT, Position.RIGHT])
                            )
                        elif position_type == "front_rear":
                            multiple_positions.append(
                                ("front_rear", [Position.FRONT, Position.REAR])
                            )
                        elif position_type == "upper_lower":
                            multiple_positions.append(
                                ("upper_lower", [Position.UPPER, Position.LOWER])
                            )
                        elif position_type == "inner_outer":
                            multiple_positions.append(
                                ("inner_outer", [Position.INNER, Position.OUTER])
                            )
                    else:
                        position_values[position_type] = value
                    break

        # If no multiple positions, return a single PositionGroup
        if not multiple_positions:
            return [
                PositionGroup(
                    front_rear=position_values["front_rear"],
                    left_right=position_values["left_right"],
                    upper_lower=position_values["upper_lower"],
                    inner_outer=position_values["inner_outer"],
                )
            ]

        # Handle multiple positions by generating all combinations
        position_groups = []
        current_group = PositionGroup(
            front_rear=position_values["front_rear"],
            left_right=position_values["left_right"],
            upper_lower=position_values["upper_lower"],
            inner_outer=position_values["inner_outer"],
        )

        self._expand_position_combinations(
            position_groups, current_group, multiple_positions, 0
        )
        return position_groups

    def _expand_position_combinations(
        self,
        result: List[PositionGroup],
        current_group: PositionGroup,
        multiple_positions: List[Tuple[str, List[Position]]],
        index: int,
    ) -> None:
        """
        Recursively expand all position combinations.

        Args:
            result: List to collect the results
            current_group: Current position group being built
            multiple_positions: List of position types with multiple values
            index: Current index in multiple_positions
        """
        if index >= len(multiple_positions):
            # Add a copy of the current group to results
            result.append(
                PositionGroup(
                    front_rear=current_group.front_rear,
                    left_right=current_group.left_right,
                    upper_lower=current_group.upper_lower,
                    inner_outer=current_group.inner_outer,
                )
            )
            return

        position_type, values = multiple_positions[index]

        for value in values:
            # Create a copy of the current group and set the position
            new_group = PositionGroup(
                front_rear=current_group.front_rear,
                left_right=current_group.left_right,
                upper_lower=current_group.upper_lower,
                inner_outer=current_group.inner_outer,
            )

            # Update the specific position
            if position_type == "left_right":
                new_group.left_right = value
            elif position_type == "front_rear":
                new_group.front_rear = value
            elif position_type == "upper_lower":
                new_group.upper_lower = value
            elif position_type == "inner_outer":
                new_group.inner_outer = value

            # Recursive call to handle the next position type
            self._expand_position_combinations(
                result, new_group, multiple_positions, index + 1
            )

    def process_application(self, part_app: PartApplication) -> List[PartFitment]:
        """
        Process a part application into a list of specific part fitments.

        Args:
            part_app: Parsed part application

        Returns:
            List of expanded PartFitment objects

        Raises:
            ParsingError: If processing fails
        """
        if not part_app.year_range or not part_app.vehicle_text:
            raise ParsingError("Missing year range or vehicle text in application")

        # Extract years
        years = self.expand_year_range(part_app.year_range[0], part_app.year_range[1])

        # Find model mappings
        model_mappings = self.find_model_mapping(part_app.vehicle_text)

        # Extract positions
        position_groups = []
        if part_app.position_text:
            position_groups = self.extract_positions(part_app.position_text)
        else:
            # Default to a single group with N/A positions
            position_groups = [PositionGroup()]

        # Generate all combinations
        fitments = []

        for year in years:
            for model_map in model_mappings:
                for position_group in position_groups:
                    vehicle = Vehicle(
                        year=year, make=model_map["make"], model=model_map["model"]
                    )

                    fitment = PartFitment(vehicle=vehicle, positions=position_group)

                    fitments.append(fitment)

        return fitments
