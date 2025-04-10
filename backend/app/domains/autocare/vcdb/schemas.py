from __future__ import annotations

"""VCdb schema definitions.

This module defines Pydantic schemas for vehicle-related objects,
including makes, models, and vehicle configurations.
"""

import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Make(BaseModel):
    """Schema for vehicle make data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    make_id: int = Field(..., description="Make ID from VCdb")
    name: str = Field(..., description="Make name")

    model_config = ConfigDict(from_attributes=True)


class VehicleType(BaseModel):
    """Schema for vehicle type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    vehicle_type_id: int = Field(..., description="Vehicle type ID from VCdb")
    name: str = Field(..., description="Vehicle type name")
    vehicle_type_group_id: Optional[int] = Field(
        None, description="Vehicle type group ID"
    )

    model_config = ConfigDict(from_attributes=True)


class VehicleTypeGroup(BaseModel):
    """Schema for vehicle type group data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    vehicle_type_group_id: int = Field(
        ..., description="Vehicle type group ID from VCdb"
    )
    name: str = Field(..., description="Vehicle type group name")

    model_config = ConfigDict(from_attributes=True)


class Model(BaseModel):
    """Schema for vehicle model data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    model_id: int = Field(..., description="Model ID from VCdb")
    name: str = Field(..., description="Model name")
    vehicle_type_id: int = Field(..., description="Vehicle type ID")
    vehicle_type: Optional[VehicleType] = Field(
        None, description="Vehicle type details"
    )

    model_config = ConfigDict(from_attributes=True)


class Year(BaseModel):
    """Schema for vehicle year data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    year_id: int = Field(..., description="Year ID from VCdb")
    year: int = Field(..., description="Year value")

    model_config = ConfigDict(from_attributes=True)


class SubModel(BaseModel):
    """Schema for vehicle submodel data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    submodel_id: int = Field(..., description="Submodel ID from VCdb")
    name: str = Field(..., description="Submodel name")

    model_config = ConfigDict(from_attributes=True)


class Region(BaseModel):
    """Schema for region data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    region_id: int = Field(..., description="Region ID from VCdb")
    parent_id: Optional[int] = Field(None, description="Parent region ID")
    abbr: Optional[str] = Field(None, description="Region abbreviation")
    name: str = Field(..., description="Region name")

    model_config = ConfigDict(from_attributes=True)


class PublicationStage(BaseModel):
    """Schema for publication stage data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    publication_stage_id: int = Field(..., description="Publication stage ID from VCdb")
    name: str = Field(..., description="Publication stage name")

    model_config = ConfigDict(from_attributes=True)


class BaseVehicle(BaseModel):
    """Schema for base vehicle data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    base_vehicle_id: int = Field(..., description="Base vehicle ID from VCdb")
    year_id: int = Field(..., description="Year ID")
    make_id: int = Field(..., description="Make ID")
    model_id: int = Field(..., description="Model ID")

    # Related entities
    year: Optional[Year] = Field(None, description="Year details")
    make: Optional[Make] = Field(None, description="Make details")
    model: Optional[Model] = Field(None, description="Model details")

    model_config = ConfigDict(from_attributes=True)


class DriveType(BaseModel):
    """Schema for drive type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    drive_type_id: int = Field(..., description="Drive type ID from VCdb")
    name: str = Field(..., description="Drive type name")

    model_config = ConfigDict(from_attributes=True)


class BrakeType(BaseModel):
    """Schema for brake type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    brake_type_id: int = Field(..., description="Brake type ID from VCdb")
    name: str = Field(..., description="Brake type name")

    model_config = ConfigDict(from_attributes=True)


class BrakeSystem(BaseModel):
    """Schema for brake system data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    brake_system_id: int = Field(..., description="Brake system ID from VCdb")
    name: str = Field(..., description="Brake system name")

    model_config = ConfigDict(from_attributes=True)


class BrakeABS(BaseModel):
    """Schema for brake ABS data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    brake_abs_id: int = Field(..., description="Brake ABS ID from VCdb")
    name: str = Field(..., description="Brake ABS name")

    model_config = ConfigDict(from_attributes=True)


class BrakeConfig(BaseModel):
    """Schema for brake configuration data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    brake_config_id: int = Field(..., description="Brake config ID from VCdb")
    front_brake_type_id: int = Field(..., description="Front brake type ID")
    rear_brake_type_id: int = Field(..., description="Rear brake type ID")
    brake_system_id: int = Field(..., description="Brake system ID")
    brake_abs_id: int = Field(..., description="Brake ABS ID")

    # Related entities
    front_brake_type: Optional[BrakeType] = Field(
        None, description="Front brake type details"
    )
    rear_brake_type: Optional[BrakeType] = Field(
        None, description="Rear brake type details"
    )
    brake_system: Optional[BrakeSystem] = Field(
        None, description="Brake system details"
    )
    brake_abs: Optional[BrakeABS] = Field(None, description="Brake ABS details")

    model_config = ConfigDict(from_attributes=True)


class BedType(BaseModel):
    """Schema for bed type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    bed_type_id: int = Field(..., description="Bed type ID from VCdb")
    name: str = Field(..., description="Bed type name")

    model_config = ConfigDict(from_attributes=True)


class BedLength(BaseModel):
    """Schema for bed length data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    bed_length_id: int = Field(..., description="Bed length ID from VCdb")
    length: str = Field(..., description="Bed length")
    length_metric: str = Field(..., description="Bed length in metric")

    model_config = ConfigDict(from_attributes=True)


class BedConfig(BaseModel):
    """Schema for bed configuration data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    bed_config_id: int = Field(..., description="Bed config ID from VCdb")
    bed_length_id: int = Field(..., description="Bed length ID")
    bed_type_id: int = Field(..., description="Bed type ID")

    # Related entities
    bed_length: Optional[BedLength] = Field(None, description="Bed length details")
    bed_type: Optional[BedType] = Field(None, description="Bed type details")

    model_config = ConfigDict(from_attributes=True)


class BodyType(BaseModel):
    """Schema for body type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    body_type_id: int = Field(..., description="Body type ID from VCdb")
    name: str = Field(..., description="Body type name")

    model_config = ConfigDict(from_attributes=True)


class BodyNumDoors(BaseModel):
    """Schema for body number of doors data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    body_num_doors_id: int = Field(..., description="Body num doors ID from VCdb")
    num_doors: str = Field(..., description="Number of doors")

    model_config = ConfigDict(from_attributes=True)


class BodyStyleConfig(BaseModel):
    """Schema for body style configuration data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    body_style_config_id: int = Field(..., description="Body style config ID from VCdb")
    body_num_doors_id: int = Field(..., description="Body num doors ID")
    body_type_id: int = Field(..., description="Body type ID")

    # Related entities
    body_num_doors: Optional[BodyNumDoors] = Field(
        None, description="Body num doors details"
    )
    body_type: Optional[BodyType] = Field(None, description="Body type details")

    model_config = ConfigDict(from_attributes=True)


class MfrBodyCode(BaseModel):
    """Schema for manufacturer body code data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    mfr_body_code_id: int = Field(..., description="Mfr body code ID from VCdb")
    code: str = Field(..., description="Body code")

    model_config = ConfigDict(from_attributes=True)


class EngineBlock(BaseModel):
    """Schema for engine block data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    engine_block_id: int = Field(..., description="Engine block ID from VCdb")
    liter: str = Field(..., description="Engine displacement in liters")
    cc: str = Field(..., description="Engine displacement in cc")
    cid: str = Field(..., description="Engine displacement in cubic inches")
    cylinders: str = Field(..., description="Number of cylinders")
    block_type: str = Field(..., description="Block type code")

    model_config = ConfigDict(from_attributes=True)


class EngineBoreStroke(BaseModel):
    """Schema for engine bore and stroke data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    engine_bore_stroke_id: int = Field(
        ..., description="Engine bore stroke ID from VCdb"
    )
    bore_in: str = Field(..., description="Bore in inches")
    bore_metric: str = Field(..., description="Bore in metric")
    stroke_in: str = Field(..., description="Stroke in inches")
    stroke_metric: str = Field(..., description="Stroke in metric")

    model_config = ConfigDict(from_attributes=True)


class EngineBase(BaseModel):
    """Schema for engine base data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    engine_base_id: int = Field(..., description="Engine base ID from VCdb")
    engine_block_id: int = Field(..., description="Engine block ID")
    engine_bore_stroke_id: int = Field(..., description="Engine bore stroke ID")

    # Related entities
    engine_block: Optional[EngineBlock] = Field(
        None, description="Engine block details"
    )
    engine_bore_stroke: Optional[EngineBoreStroke] = Field(
        None, description="Engine bore stroke details"
    )

    model_config = ConfigDict(from_attributes=True)


class Aspiration(BaseModel):
    """Schema for aspiration data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    aspiration_id: int = Field(..., description="Aspiration ID from VCdb")
    name: str = Field(..., description="Aspiration name")

    model_config = ConfigDict(from_attributes=True)


class FuelType(BaseModel):
    """Schema for fuel type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    fuel_type_id: int = Field(..., description="Fuel type ID from VCdb")
    name: str = Field(..., description="Fuel type name")

    model_config = ConfigDict(from_attributes=True)


class CylinderHeadType(BaseModel):
    """Schema for cylinder head type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    cylinder_head_type_id: int = Field(
        ..., description="Cylinder head type ID from VCdb"
    )
    name: str = Field(..., description="Cylinder head type name")

    model_config = ConfigDict(from_attributes=True)


class FuelDeliveryType(BaseModel):
    """Schema for fuel delivery type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    fuel_delivery_type_id: int = Field(
        ..., description="Fuel delivery type ID from VCdb"
    )
    name: str = Field(..., description="Fuel delivery type name")

    model_config = ConfigDict(from_attributes=True)


class FuelDeliverySubType(BaseModel):
    """Schema for fuel delivery subtype data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    fuel_delivery_subtype_id: int = Field(
        ..., description="Fuel delivery subtype ID from VCdb"
    )
    name: str = Field(..., description="Fuel delivery subtype name")

    model_config = ConfigDict(from_attributes=True)


class FuelSystemControlType(BaseModel):
    """Schema for fuel system control type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    fuel_system_control_type_id: int = Field(
        ..., description="Fuel system control type ID from VCdb"
    )
    name: str = Field(..., description="Fuel system control type name")

    model_config = ConfigDict(from_attributes=True)


class FuelSystemDesign(BaseModel):
    """Schema for fuel system design data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    fuel_system_design_id: int = Field(
        ..., description="Fuel system design ID from VCdb"
    )
    name: str = Field(..., description="Fuel system design name")

    model_config = ConfigDict(from_attributes=True)


class FuelDeliveryConfig(BaseModel):
    """Schema for fuel delivery configuration data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    fuel_delivery_config_id: int = Field(
        ..., description="Fuel delivery config ID from VCdb"
    )
    fuel_delivery_type_id: int = Field(..., description="Fuel delivery type ID")
    fuel_delivery_subtype_id: int = Field(..., description="Fuel delivery subtype ID")
    fuel_system_control_type_id: int = Field(
        ..., description="Fuel system control type ID"
    )
    fuel_system_design_id: int = Field(..., description="Fuel system design ID")

    # Related entities
    fuel_delivery_type: Optional[FuelDeliveryType] = Field(
        None, description="Fuel delivery type details"
    )
    fuel_delivery_subtype: Optional[FuelDeliverySubType] = Field(
        None, description="Fuel delivery subtype details"
    )
    fuel_system_control_type: Optional[FuelSystemControlType] = Field(
        None, description="Fuel system control type details"
    )
    fuel_system_design: Optional[FuelSystemDesign] = Field(
        None, description="Fuel system design details"
    )

    model_config = ConfigDict(from_attributes=True)


class EngineDesignation(BaseModel):
    """Schema for engine designation data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    engine_designation_id: int = Field(
        ..., description="Engine designation ID from VCdb"
    )
    name: str = Field(..., description="Engine designation name")

    model_config = ConfigDict(from_attributes=True)


class EngineVIN(BaseModel):
    """Schema for engine VIN data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    engine_vin_id: int = Field(..., description="Engine VIN ID from VCdb")
    code: str = Field(..., description="Engine VIN code")

    model_config = ConfigDict(from_attributes=True)


class EngineVersion(BaseModel):
    """Schema for engine version data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    engine_version_id: int = Field(..., description="Engine version ID from VCdb")
    version: str = Field(..., description="Engine version")

    model_config = ConfigDict(from_attributes=True)


class Valves(BaseModel):
    """Schema for valves data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    valves_id: int = Field(..., description="Valves ID from VCdb")
    valves_per_engine: str = Field(..., description="Number of valves per engine")

    model_config = ConfigDict(from_attributes=True)


class Mfr(BaseModel):
    """Schema for manufacturer data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    mfr_id: int = Field(..., description="Manufacturer ID from VCdb")
    name: str = Field(..., description="Manufacturer name")

    model_config = ConfigDict(from_attributes=True)


class IgnitionSystemType(BaseModel):
    """Schema for ignition system type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    ignition_system_type_id: int = Field(
        ..., description="Ignition system type ID from VCdb"
    )
    name: str = Field(..., description="Ignition system type name")

    model_config = ConfigDict(from_attributes=True)


class PowerOutput(BaseModel):
    """Schema for power output data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    power_output_id: int = Field(..., description="Power output ID from VCdb")
    horsepower: str = Field(..., description="Horsepower")
    kilowatt: str = Field(..., description="Kilowatt power")

    model_config = ConfigDict(from_attributes=True)


class EngineConfig(BaseModel):
    """Schema for engine configuration data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    engine_config_id: int = Field(..., description="Engine config ID from VCdb")
    engine_base_id: int = Field(..., description="Engine base ID")
    engine_designation_id: int = Field(..., description="Engine designation ID")
    engine_vin_id: int = Field(..., description="Engine VIN ID")
    valves_id: int = Field(..., description="Valves ID")
    fuel_delivery_config_id: int = Field(..., description="Fuel delivery config ID")
    aspiration_id: int = Field(..., description="Aspiration ID")
    cylinder_head_type_id: int = Field(..., description="Cylinder head type ID")
    fuel_type_id: int = Field(..., description="Fuel type ID")
    ignition_system_type_id: int = Field(..., description="Ignition system type ID")
    engine_mfr_id: int = Field(..., description="Engine manufacturer ID")
    engine_version_id: int = Field(..., description="Engine version ID")
    power_output_id: int = Field(..., description="Power output ID")

    # Selected related entities (for brevity)
    engine_base: Optional[EngineBase] = Field(None, description="Engine base details")
    fuel_type: Optional[FuelType] = Field(None, description="Fuel type details")
    aspiration: Optional[Aspiration] = Field(None, description="Aspiration details")

    model_config = ConfigDict(from_attributes=True)


class SpringType(BaseModel):
    """Schema for spring type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    spring_type_id: int = Field(..., description="Spring type ID from VCdb")
    name: str = Field(..., description="Spring type name")

    model_config = ConfigDict(from_attributes=True)


class SpringTypeConfig(BaseModel):
    """Schema for spring type configuration data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    spring_type_config_id: int = Field(
        ..., description="Spring type config ID from VCdb"
    )
    front_spring_type_id: int = Field(..., description="Front spring type ID")
    rear_spring_type_id: int = Field(..., description="Rear spring type ID")

    # Related entities
    front_spring_type: Optional[SpringType] = Field(
        None, description="Front spring type details"
    )
    rear_spring_type: Optional[SpringType] = Field(
        None, description="Rear spring type details"
    )

    model_config = ConfigDict(from_attributes=True)


class SteeringType(BaseModel):
    """Schema for steering type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    steering_type_id: int = Field(..., description="Steering type ID from VCdb")
    name: str = Field(..., description="Steering type name")

    model_config = ConfigDict(from_attributes=True)


class SteeringSystem(BaseModel):
    """Schema for steering system data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    steering_system_id: int = Field(..., description="Steering system ID from VCdb")
    name: str = Field(..., description="Steering system name")

    model_config = ConfigDict(from_attributes=True)


class SteeringConfig(BaseModel):
    """Schema for steering configuration data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    steering_config_id: int = Field(..., description="Steering config ID from VCdb")
    steering_type_id: int = Field(..., description="Steering type ID")
    steering_system_id: int = Field(..., description="Steering system ID")

    # Related entities
    steering_type: Optional[SteeringType] = Field(
        None, description="Steering type details"
    )
    steering_system: Optional[SteeringSystem] = Field(
        None, description="Steering system details"
    )

    model_config = ConfigDict(from_attributes=True)


class TransmissionType(BaseModel):
    """Schema for transmission type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    transmission_type_id: int = Field(..., description="Transmission type ID from VCdb")
    name: str = Field(..., description="Transmission type name")

    model_config = ConfigDict(from_attributes=True)


class TransmissionNumSpeeds(BaseModel):
    """Schema for transmission number of speeds data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    transmission_num_speeds_id: int = Field(
        ..., description="Transmission num speeds ID from VCdb"
    )
    num_speeds: str = Field(..., description="Number of speeds")

    model_config = ConfigDict(from_attributes=True)


class TransmissionControlType(BaseModel):
    """Schema for transmission control type data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    transmission_control_type_id: int = Field(
        ..., description="Transmission control type ID from VCdb"
    )
    name: str = Field(..., description="Transmission control type name")

    model_config = ConfigDict(from_attributes=True)


class TransmissionBase(BaseModel):
    """Schema for transmission base data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    transmission_base_id: int = Field(..., description="Transmission base ID from VCdb")
    transmission_type_id: int = Field(..., description="Transmission type ID")
    transmission_num_speeds_id: int = Field(
        ..., description="Transmission num speeds ID"
    )
    transmission_control_type_id: int = Field(
        ..., description="Transmission control type ID"
    )

    # Related entities
    transmission_type: Optional[TransmissionType] = Field(
        None, description="Transmission type details"
    )
    transmission_num_speeds: Optional[TransmissionNumSpeeds] = Field(
        None, description="Transmission num speeds details"
    )
    transmission_control_type: Optional[TransmissionControlType] = Field(
        None, description="Transmission control type details"
    )

    model_config = ConfigDict(from_attributes=True)


class TransmissionMfrCode(BaseModel):
    """Schema for transmission manufacturer code data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    transmission_mfr_code_id: int = Field(
        ..., description="Transmission mfr code ID from VCdb"
    )
    code: str = Field(..., description="Transmission manufacturer code")

    model_config = ConfigDict(from_attributes=True)


class ElecControlled(BaseModel):
    """Schema for electrically controlled data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    elec_controlled_id: int = Field(..., description="Elec controlled ID from VCdb")
    value: str = Field(..., description="Electrically controlled value")

    model_config = ConfigDict(from_attributes=True)


class Transmission(BaseModel):
    """Schema for transmission data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    transmission_id: int = Field(..., description="Transmission ID from VCdb")
    transmission_base_id: int = Field(..., description="Transmission base ID")
    transmission_mfr_code_id: int = Field(..., description="Transmission mfr code ID")
    elec_controlled_id: int = Field(..., description="Elec controlled ID")
    transmission_mfr_id: int = Field(..., description="Transmission manufacturer ID")

    # Related entities
    transmission_base: Optional[TransmissionBase] = Field(
        None, description="Transmission base details"
    )

    model_config = ConfigDict(from_attributes=True)


class WheelBase(BaseModel):
    """Schema for wheel base data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    wheel_base_id: int = Field(..., description="Wheel base ID from VCdb")
    wheel_base: str = Field(..., description="Wheel base measurement")
    wheel_base_metric: str = Field(..., description="Wheel base measurement in metric")

    model_config = ConfigDict(from_attributes=True)


class Vehicle(BaseModel):
    """Schema for complete vehicle data."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    vehicle_id: int = Field(..., description="Vehicle ID from VCdb")
    base_vehicle_id: int = Field(..., description="Base vehicle ID")
    submodel_id: int = Field(..., description="Submodel ID")
    region_id: int = Field(..., description="Region ID")
    publication_stage_id: int = Field(..., description="Publication stage ID")

    # Related entities
    base_vehicle: Optional[BaseVehicle] = Field(
        None, description="Base vehicle details"
    )
    submodel: Optional[SubModel] = Field(None, description="Submodel details")
    region: Optional[Region] = Field(None, description="Region details")
    publication_stage: Optional[PublicationStage] = Field(
        None, description="Publication stage details"
    )

    # Computed properties
    year: Optional[int] = Field(None, description="Vehicle year")
    make: Optional[str] = Field(None, description="Vehicle make name")
    model: Optional[str] = Field(None, description="Vehicle model name")

    model_config = ConfigDict(from_attributes=True)


class VehicleDetail(Vehicle):
    """Schema for detailed vehicle data with configurations."""

    engines: List[Dict[str, Any]] = Field([], description="Engine configurations")
    transmissions: List[Dict[str, Any]] = Field(
        [], description="Transmission configurations"
    )
    drive_types: List[str] = Field([], description="Drive types")
    body_styles: List[Dict[str, Any]] = Field([], description="Body styles")
    brake_configs: List[Dict[str, Any]] = Field([], description="Brake configurations")
    wheel_bases: List[Dict[str, Any]] = Field([], description="Wheel bases")

    model_config = ConfigDict(from_attributes=True)


class VehicleSearchParameters(BaseModel):
    """Schema for vehicle search parameters."""

    year: Optional[int] = Field(None, description="Filter by year")
    make: Optional[str] = Field(None, description="Filter by make name")
    model: Optional[str] = Field(None, description="Filter by model name")
    submodel: Optional[str] = Field(None, description="Filter by submodel name")
    body_type: Optional[str] = Field(None, description="Filter by body type")
    engine_config: Optional[int] = Field(
        None, description="Filter by engine configuration ID"
    )
    transmission_type: Optional[int] = Field(
        None, description="Filter by transmission type ID"
    )
    page: int = Field(1, description="Page number", ge=1)
    page_size: int = Field(20, description="Page size", ge=1, le=100)


class VehicleSearchResponse(BaseModel):
    """Schema for paginated vehicle search response."""

    items: List[Vehicle] = Field(..., description="List of vehicles")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")
