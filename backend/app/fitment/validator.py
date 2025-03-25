"""
Validator for fitment data.

This module provides validation functionality for fitment data against
VCDB and PCDB databases.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Set

from .models import (
    PartFitment,
    PCDBPosition,
    Position,
    ValidationResult,
    ValidationStatus,
    VCDBVehicle,
)

logger = logging.getLogger(__name__)


class FitmentValidator:
    """Validator for fitment data against VCDB and PCDB databases."""

    def __init__(
        self, part_terminology_id: int, pcdb_positions: List[PCDBPosition]
    ) -> None:
        """
        Initialize the validator.

        Args:
            part_terminology_id: ID of the part terminology
            pcdb_positions: List of valid PCDB positions for this part
        """
        self.part_terminology_id = part_terminology_id
        self.pcdb_positions = pcdb_positions

        # Index positions by their components for faster lookup
        self.position_index: Dict[str, Dict[Position, Set[int]]] = {
            "front_rear": {},
            "left_right": {},
            "upper_lower": {},
            "inner_outer": {},
        }

        for pos in pcdb_positions:
            self._index_position(pos)

    def _index_position(self, position: PCDBPosition) -> None:
        """
        Index a PCDB position by its components.

        Args:
            position: PCDB position to index
        """
        # Index front_rear
        if position.front_rear:
            pos_value = Position(position.front_rear)
            if pos_value not in self.position_index["front_rear"]:
                self.position_index["front_rear"][pos_value] = set()
            self.position_index["front_rear"][pos_value].add(position.id)

        # Index left_right
        if position.left_right:
            pos_value = Position(position.left_right)
            if pos_value not in self.position_index["left_right"]:
                self.position_index["left_right"][pos_value] = set()
            self.position_index["left_right"][pos_value].add(position.id)

        # Index upper_lower
        if position.upper_lower:
            pos_value = Position(position.upper_lower)
            if pos_value not in self.position_index["upper_lower"]:
                self.position_index["upper_lower"][pos_value] = set()
            self.position_index["upper_lower"][pos_value].add(position.id)

        # Index inner_outer
        if position.inner_outer:
            pos_value = Position(position.inner_outer)
            if pos_value not in self.position_index["inner_outer"]:
                self.position_index["inner_outer"][pos_value] = set()
            self.position_index["inner_outer"][pos_value].add(position.id)

    def validate_fitment(
        self, fitment: PartFitment, available_vehicles: List[VCDBVehicle]
    ) -> ValidationResult:
        """
        Validate a fitment against VCDB and PCDB data.

        Args:
            fitment: The fitment to validate
            available_vehicles: List of available VCDB vehicles

        Returns:
            ValidationResult with status and messages
        """
        # Track issues for reporting
        issues = []

        # Validate vehicle against VCDB
        vehicle_result = self._validate_vehicle(fitment, available_vehicles)
        if vehicle_result.status == ValidationStatus.ERROR:
            return vehicle_result
        elif vehicle_result.status == ValidationStatus.WARNING:
            issues.append(vehicle_result.message)

        # Validate positions against PCDB
        position_result = self._validate_positions(fitment)
        if position_result.status == ValidationStatus.ERROR:
            return position_result
        elif position_result.status == ValidationStatus.WARNING:
            issues.append(position_result.message)

        # If we had any warnings, return them
        if issues:
            return ValidationResult(
                status=ValidationStatus.WARNING,
                message="; ".join(issues),
                fitment=fitment,
                original_text=fitment.vehicle.full_name,
            )

        # Everything is valid
        return ValidationResult(
            status=ValidationStatus.VALID,
            message="Fitment is valid",
            fitment=fitment,
            original_text=fitment.vehicle.full_name,
        )

    def _validate_vehicle(
        self, fitment: PartFitment, available_vehicles: List[VCDBVehicle]
    ) -> ValidationResult:
        """
        Validate a vehicle against VCDB data.

        Args:
            fitment: The fitment to validate
            available_vehicles: List of available VCDB vehicles

        Returns:
            ValidationResult with status and messages
        """
        # First check: exact match
        exact_matches = []
        partial_matches = []

        for vehicle in available_vehicles:
            if (
                vehicle.year == fitment.vehicle.year
                and vehicle.make.lower() == fitment.vehicle.make.lower()
                and vehicle.model.lower() == fitment.vehicle.model.lower()
            ):

                # Check submodel if both have it
                if fitment.vehicle.submodel and vehicle.submodel:
                    if fitment.vehicle.submodel.lower() == vehicle.submodel.lower():
                        exact_matches.append(vehicle)
                # If fitment has no submodel but vehicle does, it's a partial match
                elif not fitment.vehicle.submodel and vehicle.submodel:
                    partial_matches.append(vehicle)
                # If neither has submodel or vehicle has no submodel, it's an exact match
                elif not vehicle.submodel:
                    exact_matches.append(vehicle)

        # If we have exact matches, use the first one
        if exact_matches:
            fitment.vcdb_vehicle_id = exact_matches[0].id
            return ValidationResult(
                status=ValidationStatus.VALID,
                message="Exact vehicle match found",
                fitment=fitment,
                original_text=fitment.vehicle.full_name,
            )

        # If we have partial matches, use the first one but warn
        if partial_matches:
            fitment.vcdb_vehicle_id = partial_matches[0].id
            submodels = ", ".join(v.submodel for v in partial_matches if v.submodel)
            return ValidationResult(
                status=ValidationStatus.WARNING,
                message=f"No exact vehicle match found. Possible submodels: {submodels}",
                fitment=fitment,
                original_text=fitment.vehicle.full_name,
                suggestions=[v.submodel for v in partial_matches if v.submodel],
            )

        # No matches found
        return ValidationResult(
            status=ValidationStatus.ERROR,
            message="No matching vehicle found in VCDB",
            fitment=fitment,
            original_text=fitment.vehicle.full_name,
        )

    def _validate_positions(self, fitment: PartFitment) -> ValidationResult:
        """
        Validate positions against PCDB data.

        Args:
            fitment: The fitment to validate

        Returns:
            ValidationResult with status and messages
        """
        # Check if all positions are valid for this part terminology
        positions = fitment.positions

        # Track valid position IDs
        valid_position_ids = set()

        # Check front_rear
        if positions.front_rear != Position.NA:
            if positions.front_rear not in self.position_index["front_rear"]:
                if positions.front_rear == Position.VARIES:
                    # Varies is a special case - need manual review
                    return ValidationResult(
                        status=ValidationStatus.WARNING,
                        message="Front/Rear position varies with application - manual review needed",
                        fitment=fitment,
                        original_text=fitment.vehicle.full_name,
                    )
                else:
                    return ValidationResult(
                        status=ValidationStatus.ERROR,
                        message=f"Invalid Front/Rear position: {positions.front_rear}",
                        fitment=fitment,
                        original_text=fitment.vehicle.full_name,
                    )
            else:
                valid_position_ids.update(
                    self.position_index["front_rear"][positions.front_rear]
                )

        # Check left_right
        if positions.left_right != Position.NA:
            if positions.left_right not in self.position_index["left_right"]:
                if positions.left_right == Position.VARIES:
                    # Varies is a special case - need manual review
                    return ValidationResult(
                        status=ValidationStatus.WARNING,
                        message="Left/Right position varies with application - manual review needed",
                        fitment=fitment,
                        original_text=fitment.vehicle.full_name,
                    )
                else:
                    return ValidationResult(
                        status=ValidationStatus.ERROR,
                        message=f"Invalid Left/Right position: {positions.left_right}",
                        fitment=fitment,
                        original_text=fitment.vehicle.full_name,
                    )
            else:
                valid_position_ids.update(
                    self.position_index["left_right"][positions.left_right]
                )

        # Check upper_lower
        if positions.upper_lower != Position.NA:
            if positions.upper_lower not in self.position_index["upper_lower"]:
                if positions.upper_lower == Position.VARIES:
                    # Varies is a special case - need manual review
                    return ValidationResult(
                        status=ValidationStatus.WARNING,
                        message="Upper/Lower position varies with application - manual review needed",
                        fitment=fitment,
                        original_text=fitment.vehicle.full_name,
                    )
                else:
                    return ValidationResult(
                        status=ValidationStatus.ERROR,
                        message=f"Invalid Upper/Lower position: {positions.upper_lower}",
                        fitment=fitment,
                        original_text=fitment.vehicle.full_name,
                    )
            else:
                valid_position_ids.update(
                    self.position_index["upper_lower"][positions.upper_lower]
                )

        # Check inner_outer
        if positions.inner_outer != Position.NA:
            if positions.inner_outer not in self.position_index["inner_outer"]:
                if positions.inner_outer == Position.VARIES:
                    # Varies is a special case - need manual review
                    return ValidationResult(
                        status=ValidationStatus.WARNING,
                        message="Inner/Outer position varies with application - manual review needed",
                        fitment=fitment,
                        original_text=fitment.vehicle.full_name,
                    )
                else:
                    return ValidationResult(
                        status=ValidationStatus.ERROR,
                        message=f"Invalid Inner/Outer position: {positions.inner_outer}",
                        fitment=fitment,
                        original_text=fitment.vehicle.full_name,
                    )
            else:
                valid_position_ids.update(
                    self.position_index["inner_outer"][positions.inner_outer]
                )

        # If no valid position IDs found and we have non-N/A positions
        if not valid_position_ids and any(
            [
                positions.front_rear != Position.NA,
                positions.left_right != Position.NA,
                positions.upper_lower != Position.NA,
                positions.inner_outer != Position.NA,
            ]
        ):
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="No valid positions found for this part terminology",
                fitment=fitment,
                original_text=fitment.vehicle.full_name,
            )

        # Set the valid position IDs on the fitment
        fitment.pcdb_position_ids = list(valid_position_ids)

        return ValidationResult(
            status=ValidationStatus.VALID,
            message="Positions are valid",
            fitment=fitment,
            original_text=fitment.vehicle.full_name,
        )
