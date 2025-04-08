# app/domains/autocare/importers/vcdb_importer.py
from __future__ import annotations

"""
VCdb (Vehicle Component Database) data importer.

This module provides a specialized importer for VCdb data from various formats,
mapping external data to the correct database models with proper transformations.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.autocare.importers.flexible_importer import (
    FlexibleImporter,
    SourceFormat,
    detect_source_format,
)
from app.domains.autocare.vcdb.models import (
    Make,
    Year,
    Model,
    VehicleType,
    VehicleTypeGroup,
    SubModel,
    Region,
    BaseVehicle,
    Vehicle,
    DriveType,
    BrakeType,
    BrakeSystem,
    BrakeABS,
    BrakeConfig,
    BodyType,
    BodyNumDoors,
    BodyStyleConfig,
    EngineBlock,
    EngineBoreStroke,
    EngineBase,
    EngineBase2,
    Aspiration,
    FuelType,
    CylinderHeadType,
    FuelDeliveryType,
    FuelDeliverySubType,
    FuelSystemControlType,
    FuelSystemDesign,
    FuelDeliveryConfig,
    EngineDesignation,
    EngineVIN,
    EngineVersion,
    Valves,
    Mfr,
    IgnitionSystemType,
    PowerOutput,
    EngineConfig,
    EngineConfig2,
    TransmissionType,
    TransmissionNumSpeeds,
    TransmissionControlType,
    TransmissionBase,
    TransmissionMfrCode,
    ElecControlled,
    Transmission,
    WheelBase,
    VCdbVersion,
    BedType,
    BedLength,
    BedConfig,
    MfrBodyCode,
    SpringType,
    SpringTypeConfig,
    SteeringType,
    SteeringSystem,
    SteeringConfig,
    PublicationStage,
    VehicleToDriveType,
    VehicleToBrakeConfig,
    VehicleToBedConfig,
    VehicleToBodyStyleConfig,
    VehicleToMfrBodyCode,
    VehicleToEngineConfig,
    VehicleToSpringTypeConfig,
    VehicleToSteeringConfig,
    VehicleToTransmission,
    VehicleToWheelBase,
)
from app.logging import get_logger

logger = get_logger("app.domains.autocare.importers.vcdb_importer")


class VCdbImporter(FlexibleImporter):
    """Importer for VCdb (Vehicle Component Database) data from various formats."""

    def __init__(
        self,
        db: AsyncSession,
        source_path: Path,
        source_format: Optional[SourceFormat] = None,
        batch_size: int = 1000,
    ):
        """
        Initialize VCdbImporter.

        Args:
            db: Database session
            source_path: Path to source files directory
            source_format: Format of the source data (auto-detected if None)
            batch_size: Batch size for imports
        """
        # Auto-detect format if not specified
        if source_format is None:
            source_format = detect_source_format(source_path)
            logger.info(f"Auto-detected source format: {source_format.value}")

        # Define file extensions based on source format
        file_ext = ".json" if source_format == SourceFormat.JSON else ".txt"

        # Define required files for minimal import
        required_sources = [
            f"Version{file_ext}",
            f"BaseVehicle{file_ext}",
            f"Make{file_ext}",
            f"Model{file_ext}",
            f"Year{file_ext}",
            f"VehicleType{file_ext}",
            f"SubModel{file_ext}",
            f"Region{file_ext}",
        ]

        super().__init__(
            db=db,
            source_path=source_path,
            schema_name="vcdb",
            required_sources=required_sources,
            version_class=VCdbVersion,
            source_format=source_format,
            version_date_field="version_date",
            batch_size=batch_size,
        )

        # Register all table mappings
        self._register_mappings()

        # Define import order for referential integrity
        self.set_import_order(
            [
                f"Year{file_ext}",
                f"VehicleTypeGroup{file_ext}",
                f"VehicleType{file_ext}",
                f"Make{file_ext}",
                f"Model{file_ext}",
                f"SubModel{file_ext}",
                f"Region{file_ext}",
                f"PublicationStage{file_ext}",
                f"BaseVehicle{file_ext}",
                f"Vehicle{file_ext}",
                f"DriveType{file_ext}",
                f"BrakeType{file_ext}",
                f"BrakeSystem{file_ext}",
                f"BrakeABS{file_ext}",
                f"BrakeConfig{file_ext}",
                f"BedType{file_ext}",
                f"BedLength{file_ext}",
                f"BedConfig{file_ext}",
                f"BodyType{file_ext}",
                f"BodyNumDoors{file_ext}",
                f"BodyStyleConfig{file_ext}",
                f"MfrBodyCode{file_ext}",
                f"EngineBlock{file_ext}",
                f"EngineBoreStroke{file_ext}",
                f"Mfr{file_ext}",
                f"EngineBase{file_ext}",
                f"EngineBase2{file_ext}",
                f"Aspiration{file_ext}",
                f"FuelType{file_ext}",
                f"CylinderHeadType{file_ext}",
                f"FuelDeliveryType{file_ext}",
                f"FuelDeliverySubType{file_ext}",
                f"FuelSystemControlType{file_ext}",
                f"FuelSystemDesign{file_ext}",
                f"FuelDeliveryConfig{file_ext}",
                f"EngineDesignation{file_ext}",
                f"EngineVIN{file_ext}",
                f"EngineVersion{file_ext}",
                f"Valves{file_ext}",
                f"IgnitionSystemType{file_ext}",
                f"PowerOutput{file_ext}",
                f"EngineConfig{file_ext}",
                f"EngineConfig2{file_ext}",
                f"TransmissionType{file_ext}",
                f"TransmissionNumSpeeds{file_ext}",
                f"TransmissionControlType{file_ext}",
                f"TransmissionBase{file_ext}",
                f"TransmissionMfrCode{file_ext}",
                f"ElecControlled{file_ext}",
                f"Transmission{file_ext}",
                f"WheelBase{file_ext}",
                f"SpringType{file_ext}",
                f"SpringTypeConfig{file_ext}",
                f"SteeringType{file_ext}",
                f"SteeringSystem{file_ext}",
                f"SteeringConfig{file_ext}",
                f"VehicleToDriveType{file_ext}",
                f"VehicleToBrakeConfig{file_ext}",
                f"VehicleToBedConfig{file_ext}",
                f"VehicleToBodyStyleConfig{file_ext}",
                f"VehicleToMfrBodyCode{file_ext}",
                f"VehicleToEngineConfig{file_ext}",
                f"VehicleToSpringTypeConfig{file_ext}",
                f"VehicleToSteeringConfig{file_ext}",
                f"VehicleToTransmission{file_ext}",
                f"VehicleToWheelBase{file_ext}",
            ]
        )

    def _register_mappings(self) -> None:
        """Register all table mappings for VCdb imports."""
        # Use appropriate file extension for all mappings
        file_ext = ".json" if self.source_format == SourceFormat.JSON else ".txt"

        # Base tables
        self._register_base_tables(file_ext)

        # Vehicle structure tables
        self._register_vehicle_structure_tables(file_ext)

        # Engine tables
        self._register_engine_tables(file_ext)

        # Transmission tables
        self._register_transmission_tables(file_ext)

        # Configuration tables
        self._register_config_tables(file_ext)

        # Many-to-many tables
        self._register_many_to_many_tables(file_ext)

    def _register_base_tables(self, file_ext: str) -> None:
        """
        Register base table mappings.

        Args:
            file_ext: File extension to use
        """
        # Year
        self.register_table_mapping(
            source_name=f"Year{file_ext}",
            model_class=Year,
            field_mapping={
                "year_id": "YearID",
            },
            primary_key="year_id",
            transformers={
                "year_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleTypeGroup
        self.register_table_mapping(
            source_name=f"VehicleTypeGroup{file_ext}",
            model_class=VehicleTypeGroup,
            field_mapping={
                "vehicle_type_group_id": "VehicleTypeGroupID",
                "name": "VehicleTypeGroupName",
            },
            primary_key="vehicle_type_group_id",
            transformers={
                "vehicle_type_group_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleType
        self.register_table_mapping(
            source_name=f"VehicleType{file_ext}",
            model_class=VehicleType,
            field_mapping={
                "vehicle_type_id": "VehicleTypeID",
                "name": "VehicleTypeName",
                "vehicle_type_group_id": "VehicleTypeGroupID",
            },
            primary_key="vehicle_type_id",
            transformers={
                "vehicle_type_id": lambda x: int(x) if x else None,
                "vehicle_type_group_id": lambda x: int(x) if x else None,
            },
        )

        # Make
        self.register_table_mapping(
            source_name=f"Make{file_ext}",
            model_class=Make,
            field_mapping={
                "make_id": "MakeID",
                "name": "MakeName",
            },
            primary_key="make_id",
            transformers={
                "make_id": lambda x: int(x) if x else None,
            },
        )

        # Model
        self.register_table_mapping(
            source_name=f"Model{file_ext}",
            model_class=Model,
            field_mapping={
                "model_id": "ModelID",
                "name": "ModelName",
                "vehicle_type_id": "VehicleTypeID",
            },
            primary_key="model_id",
            transformers={
                "model_id": lambda x: int(x) if x else None,
                "vehicle_type_id": lambda x: int(x) if x else None,
            },
        )

        # SubModel
        self.register_table_mapping(
            source_name=f"SubModel{file_ext}",
            model_class=SubModel,
            field_mapping={
                "submodel_id": "SubModelID",
                "name": "SubModelName",
            },
            primary_key="submodel_id",
            transformers={
                "submodel_id": lambda x: int(x) if x else None,
            },
        )

        # Region
        self.register_table_mapping(
            source_name=f"Region{file_ext}",
            model_class=Region,
            field_mapping={
                "region_id": "RegionID",
                "parent_id": "ParentID",
                "abbr": "RegionAbbr",
                "name": "RegionName",
            },
            primary_key="region_id",
            transformers={
                "region_id": lambda x: int(x) if x else None,
                "parent_id": lambda x: int(x) if x and x.strip() else None,
            },
        )

        # PublicationStage
        self.register_table_mapping(
            source_name=f"PublicationStage{file_ext}",
            model_class=PublicationStage,
            field_mapping={
                "publication_stage_id": "PublicationStageID",
                "name": "PublicationStageName",
            },
            primary_key="publication_stage_id",
            transformers={
                "publication_stage_id": lambda x: int(x) if x else None,
            },
        )

        # BaseVehicle
        self.register_table_mapping(
            source_name=f"BaseVehicle{file_ext}",
            model_class=BaseVehicle,
            field_mapping={
                "base_vehicle_id": "BaseVehicleID",
                "year_id": "YearID",
                "make_id": "MakeID",
                "model_id": "ModelID",
            },
            primary_key="base_vehicle_id",
            transformers={
                "base_vehicle_id": lambda x: int(x) if x else None,
                "year_id": lambda x: int(x) if x else None,
                "make_id": lambda x: int(x) if x else None,
                "model_id": lambda x: int(x) if x else None,
            },
        )

        # Vehicle
        self.register_table_mapping(
            source_name=f"Vehicle{file_ext}",
            model_class=Vehicle,
            field_mapping={
                "vehicle_id": "VehicleID",
                "base_vehicle_id": "BaseVehicleID",
                "submodel_id": "SubmodelID",
                "region_id": "RegionID",
                "source": "Source",
                "publication_stage_id": "PublicationStageID",
                "publication_stage_source": "PublicationStageSource",
                "publication_stage_date": "PublicationStageDate",
            },
            primary_key="vehicle_id",
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "base_vehicle_id": lambda x: int(x) if x else None,
                "submodel_id": lambda x: int(x) if x else None,
                "region_id": lambda x: int(x) if x else None,
                "publication_stage_id": lambda x: (
                    int(x) if x else 4
                ),  # Default to "Production"
                "publication_stage_date": lambda x: (
                    datetime.strptime(x, "%Y-%m-%dT%H:%M:%S").date()
                    if x and x.strip()
                    else datetime.now().date()
                ),
                "publication_stage_source": lambda x: (
                    x if x and x.strip() else "DataLoad"
                ),
            },
        )

    def _register_vehicle_structure_tables(self, file_ext: str) -> None:
        """
        Register vehicle structure table mappings.

        Args:
            file_ext: File extension to use
        """
        # DriveType
        self.register_table_mapping(
            source_name=f"DriveType{file_ext}",
            model_class=DriveType,
            field_mapping={
                "drive_type_id": "DriveTypeID",
                "name": "DriveTypeName",
            },
            primary_key="drive_type_id",
            transformers={
                "drive_type_id": lambda x: int(x) if x else None,
            },
        )

        # BrakeType
        self.register_table_mapping(
            source_name=f"BrakeType{file_ext}",
            model_class=BrakeType,
            field_mapping={
                "brake_type_id": "BrakeTypeID",
                "name": "BrakeTypeName",
            },
            primary_key="brake_type_id",
            transformers={
                "brake_type_id": lambda x: int(x) if x else None,
            },
        )

        # BrakeSystem
        self.register_table_mapping(
            source_name=f"BrakeSystem{file_ext}",
            model_class=BrakeSystem,
            field_mapping={
                "brake_system_id": "BrakeSystemID",
                "name": "BrakeSystemName",
            },
            primary_key="brake_system_id",
            transformers={
                "brake_system_id": lambda x: int(x) if x else None,
            },
        )

        # BrakeABS
        self.register_table_mapping(
            source_name=f"BrakeABS{file_ext}",
            model_class=BrakeABS,
            field_mapping={
                "brake_abs_id": "BrakeABSID",
                "name": "BrakeABSName",
            },
            primary_key="brake_abs_id",
            transformers={
                "brake_abs_id": lambda x: int(x) if x else None,
            },
        )

        # BrakeConfig
        self.register_table_mapping(
            source_name=f"BrakeConfig{file_ext}",
            model_class=BrakeConfig,
            field_mapping={
                "brake_config_id": "BrakeConfigID",
                "front_brake_type_id": "FrontBrakeTypeID",
                "rear_brake_type_id": "RearBrakeTypeID",
                "brake_system_id": "BrakeSystemID",
                "brake_abs_id": "BrakeABSID",
            },
            primary_key="brake_config_id",
            transformers={
                "brake_config_id": lambda x: int(x) if x else None,
                "front_brake_type_id": lambda x: int(x) if x else None,
                "rear_brake_type_id": lambda x: int(x) if x else None,
                "brake_system_id": lambda x: int(x) if x else None,
                "brake_abs_id": lambda x: int(x) if x else None,
            },
        )

        # BedType
        self.register_table_mapping(
            source_name=f"BedType{file_ext}",
            model_class=BedType,
            field_mapping={
                "bed_type_id": "BedTypeID",
                "name": "BedTypeName",
            },
            primary_key="bed_type_id",
            transformers={
                "bed_type_id": lambda x: int(x) if x else None,
            },
        )

        # BedLength
        self.register_table_mapping(
            source_name=f"BedLength{file_ext}",
            model_class=BedLength,
            field_mapping={
                "bed_length_id": "BedLengthID",
                "length": "BedLength",
                "length_metric": "BedLengthMetric",
            },
            primary_key="bed_length_id",
            transformers={
                "bed_length_id": lambda x: int(x) if x else None,
            },
        )

        # BedConfig
        self.register_table_mapping(
            source_name=f"BedConfig{file_ext}",
            model_class=BedConfig,
            field_mapping={
                "bed_config_id": "BedConfigID",
                "bed_length_id": "BedLengthID",
                "bed_type_id": "BedTypeID",
            },
            primary_key="bed_config_id",
            transformers={
                "bed_config_id": lambda x: int(x) if x else None,
                "bed_length_id": lambda x: int(x) if x else None,
                "bed_type_id": lambda x: int(x) if x else None,
            },
        )

        # BodyType
        self.register_table_mapping(
            source_name=f"BodyType{file_ext}",
            model_class=BodyType,
            field_mapping={
                "body_type_id": "BodyTypeID",
                "name": "BodyTypeName",
            },
            primary_key="body_type_id",
            transformers={
                "body_type_id": lambda x: int(x) if x else None,
            },
        )

        # BodyNumDoors
        self.register_table_mapping(
            source_name=f"BodyNumDoors{file_ext}",
            model_class=BodyNumDoors,
            field_mapping={
                "body_num_doors_id": "BodyNumDoorsID",
                "num_doors": "BodyNumDoors",
            },
            primary_key="body_num_doors_id",
            transformers={
                "body_num_doors_id": lambda x: int(x) if x else None,
            },
        )

        # BodyStyleConfig
        self.register_table_mapping(
            source_name=f"BodyStyleConfig{file_ext}",
            model_class=BodyStyleConfig,
            field_mapping={
                "body_style_config_id": "BodyStyleConfigID",
                "body_num_doors_id": "BodyNumDoorsID",
                "body_type_id": "BodyTypeID",
            },
            primary_key="body_style_config_id",
            transformers={
                "body_style_config_id": lambda x: int(x) if x else None,
                "body_num_doors_id": lambda x: int(x) if x else None,
                "body_type_id": lambda x: int(x) if x else None,
            },
        )

        # MfrBodyCode
        self.register_table_mapping(
            source_name=f"MfrBodyCode{file_ext}",
            model_class=MfrBodyCode,
            field_mapping={
                "mfr_body_code_id": "MfrBodyCodeID",
                "code": "MfrBodyCodeName",
            },
            primary_key="mfr_body_code_id",
            transformers={
                "mfr_body_code_id": lambda x: int(x) if x else None,
            },
        )

    def _register_engine_tables(self, file_ext: str) -> None:
        """
        Register engine-related table mappings.

        Args:
            file_ext: File extension to use
        """
        # EngineBlock
        self.register_table_mapping(
            source_name=f"EngineBlock{file_ext}",
            model_class=EngineBlock,
            field_mapping={
                "engine_block_id": "EngineBlockID",
                "liter": "Liter",
                "cc": "CC",
                "cid": "CID",
                "cylinders": "Cylinders",
                "block_type": "BlockType",
            },
            primary_key="engine_block_id",
            transformers={
                "engine_block_id": lambda x: int(x) if x else None,
            },
        )

        # EngineBoreStroke
        self.register_table_mapping(
            source_name=f"EngineBoreStroke{file_ext}",
            model_class=EngineBoreStroke,
            field_mapping={
                "engine_bore_stroke_id": "EngineBoreStrokeID",
                "bore_in": "EngBoreIn",
                "bore_metric": "EngBoreMetric",
                "stroke_in": "EngStrokeIn",
                "stroke_metric": "EngStrokeMetric",
            },
            primary_key="engine_bore_stroke_id",
            transformers={
                "engine_bore_stroke_id": lambda x: int(x) if x else None,
            },
        )

        # Mfr
        self.register_table_mapping(
            source_name=f"Mfr{file_ext}",
            model_class=Mfr,
            field_mapping={
                "mfr_id": "MfrID",
                "name": "MfrName",
            },
            primary_key="mfr_id",
            transformers={
                "mfr_id": lambda x: int(x) if x else None,
            },
        )

        # EngineBase
        self.register_table_mapping(
            source_name=f"EngineBase{file_ext}",
            model_class=EngineBase,
            field_mapping={
                "engine_base_id": "EngineBaseID",
                "liter": "Liter",
                "cc": "CC",
                "cid": "CID",
                "cylinders": "Cylinders",
                "block_type": "BlockType",
                "eng_bore_in": "EngBoreIn",
                "eng_bore_metric": "EngBoreMetric",
                "eng_stroke_in": "EngStrokeIn",
                "eng_stroke_metric": "EngStrokeMetric",
            },
            primary_key="engine_base_id",
            transformers={
                "engine_base_id": lambda x: int(x) if x else None,
            },
        )

        # EngineBase2
        self.register_table_mapping(
            source_name=f"EngineBase2{file_ext}",
            model_class=EngineBase2,
            field_mapping={
                "engine_base_id": "EngineBaseID",
                "engine_block_id": "EngineBlockID",
                "engine_bore_stroke_id": "EngineBoreStrokeID",
            },
            primary_key="engine_base_id",
            transformers={
                "engine_base_id": lambda x: int(x) if x else None,
                "engine_block_id": lambda x: int(x) if x else None,
                "engine_bore_stroke_id": lambda x: int(x) if x else None,
            },
        )

        # Aspiration
        self.register_table_mapping(
            source_name=f"Aspiration{file_ext}",
            model_class=Aspiration,
            field_mapping={
                "aspiration_id": "AspirationID",
                "name": "AspirationName",
            },
            primary_key="aspiration_id",
            transformers={
                "aspiration_id": lambda x: int(x) if x else None,
            },
        )

        # FuelType
        self.register_table_mapping(
            source_name=f"FuelType{file_ext}",
            model_class=FuelType,
            field_mapping={
                "fuel_type_id": "FuelTypeID",
                "name": "FuelTypeName",
            },
            primary_key="fuel_type_id",
            transformers={
                "fuel_type_id": lambda x: int(x) if x else None,
            },
        )

        # CylinderHeadType
        self.register_table_mapping(
            source_name=f"CylinderHeadType{file_ext}",
            model_class=CylinderHeadType,
            field_mapping={
                "cylinder_head_type_id": "CylinderHeadTypeID",
                "name": "CylinderHeadTypeName",
            },
            primary_key="cylinder_head_type_id",
            transformers={
                "cylinder_head_type_id": lambda x: int(x) if x else None,
            },
        )

        # FuelDeliveryType
        self.register_table_mapping(
            source_name=f"FuelDeliveryType{file_ext}",
            model_class=FuelDeliveryType,
            field_mapping={
                "fuel_delivery_type_id": "FuelDeliveryTypeID",
                "name": "FuelDeliveryTypeName",
            },
            primary_key="fuel_delivery_type_id",
            transformers={
                "fuel_delivery_type_id": lambda x: int(x) if x else None,
            },
        )

        # FuelDeliverySubType
        self.register_table_mapping(
            source_name=f"FuelDeliverySubType{file_ext}",
            model_class=FuelDeliverySubType,
            field_mapping={
                "fuel_delivery_subtype_id": "FuelDeliverySubTypeID",
                "name": "FuelDeliverySubTypeName",
            },
            primary_key="fuel_delivery_subtype_id",
            transformers={
                "fuel_delivery_subtype_id": lambda x: int(x) if x else None,
            },
        )

        # FuelSystemControlType
        self.register_table_mapping(
            source_name=f"FuelSystemControlType{file_ext}",
            model_class=FuelSystemControlType,
            field_mapping={
                "fuel_system_control_type_id": "FuelSystemControlTypeID",
                "name": "FuelSystemControlTypeName",
            },
            primary_key="fuel_system_control_type_id",
            transformers={
                "fuel_system_control_type_id": lambda x: int(x) if x else None,
            },
        )

        # FuelSystemDesign
        self.register_table_mapping(
            source_name=f"FuelSystemDesign{file_ext}",
            model_class=FuelSystemDesign,
            field_mapping={
                "fuel_system_design_id": "FuelSystemDesignID",
                "name": "FuelSystemDesignName",
            },
            primary_key="fuel_system_design_id",
            transformers={
                "fuel_system_design_id": lambda x: int(x) if x else None,
            },
        )

        # FuelDeliveryConfig
        self.register_table_mapping(
            source_name=f"FuelDeliveryConfig{file_ext}",
            model_class=FuelDeliveryConfig,
            field_mapping={
                "fuel_delivery_config_id": "FuelDeliveryConfigID",
                "fuel_delivery_type_id": "FuelDeliveryTypeID",
                "fuel_delivery_subtype_id": "FuelDeliverySubTypeID",
                "fuel_system_control_type_id": "FuelSystemControlTypeID",
                "fuel_system_design_id": "FuelSystemDesignID",
            },
            primary_key="fuel_delivery_config_id",
            transformers={
                "fuel_delivery_config_id": lambda x: int(x) if x else None,
                "fuel_delivery_type_id": lambda x: int(x) if x else None,
                "fuel_delivery_subtype_id": lambda x: int(x) if x else None,
                "fuel_system_control_type_id": lambda x: int(x) if x else None,
                "fuel_system_design_id": lambda x: int(x) if x else None,
            },
        )

        # EngineDesignation
        self.register_table_mapping(
            source_name=f"EngineDesignation{file_ext}",
            model_class=EngineDesignation,
            field_mapping={
                "engine_designation_id": "EngineDesignationID",
                "name": "EngineDesignationName",
            },
            primary_key="engine_designation_id",
            transformers={
                "engine_designation_id": lambda x: int(x) if x else None,
            },
        )

        # EngineVIN
        self.register_table_mapping(
            source_name=f"EngineVIN{file_ext}",
            model_class=EngineVIN,
            field_mapping={
                "engine_vin_id": "EngineVINID",
                "code": "EngineVINName",
            },
            primary_key="engine_vin_id",
            transformers={
                "engine_vin_id": lambda x: int(x) if x else None,
            },
        )

        # EngineVersion
        self.register_table_mapping(
            source_name=f"EngineVersion{file_ext}",
            model_class=EngineVersion,
            field_mapping={
                "engine_version_id": "EngineVersionID",
                "version": "EngineVersion",
            },
            primary_key="engine_version_id",
            transformers={
                "engine_version_id": lambda x: int(x) if x else None,
            },
        )

        # Valves
        self.register_table_mapping(
            source_name=f"Valves{file_ext}",
            model_class=Valves,
            field_mapping={
                "valves_id": "ValvesID",
                "valves_per_engine": "ValvesPerEngine",
            },
            primary_key="valves_id",
            transformers={
                "valves_id": lambda x: int(x) if x else None,
            },
        )

        # IgnitionSystemType
        self.register_table_mapping(
            source_name=f"IgnitionSystemType{file_ext}",
            model_class=IgnitionSystemType,
            field_mapping={
                "ignition_system_type_id": "IgnitionSystemTypeID",
                "name": "IgnitionSystemTypeName",
            },
            primary_key="ignition_system_type_id",
            transformers={
                "ignition_system_type_id": lambda x: int(x) if x else None,
            },
        )

        # PowerOutput
        self.register_table_mapping(
            source_name=f"PowerOutput{file_ext}",
            model_class=PowerOutput,
            field_mapping={
                "power_output_id": "PowerOutputID",
                "horsepower": "HorsePower",
                "kilowatt": "KilowattPower",
            },
            primary_key="power_output_id",
            transformers={
                "power_output_id": lambda x: int(x) if x else None,
            },
        )

        # EngineConfig
        self.register_table_mapping(
            source_name=f"EngineConfig{file_ext}",
            model_class=EngineConfig,
            field_mapping={
                "engine_config_id": "EngineConfigID",
                "engine_designation_id": "EngineDesignationID",
                "engine_vin_id": "EngineVINID",
                "valves_id": "ValvesID",
                "engine_base_id": "EngineBaseID",
                "fuel_delivery_config_id": "FuelDeliveryConfigID",
                "aspiration_id": "AspirationID",
                "cylinder_head_type_id": "CylinderHeadTypeID",
                "fuel_type_id": "FuelTypeID",
                "ignition_system_type_id": "IgnitionSystemTypeID",
                "engine_mfr_id": "EngineMfrID",
                "engine_version_id": "EngineVersionID",
                "power_output_id": "PowerOutputID",
            },
            primary_key="engine_config_id",
            transformers={
                "engine_config_id": lambda x: int(x) if x else None,
                "engine_designation_id": lambda x: int(x) if x else None,
                "engine_vin_id": lambda x: int(x) if x else None,
                "valves_id": lambda x: int(x) if x else None,
                "engine_base_id": lambda x: int(x) if x else None,
                "fuel_delivery_config_id": lambda x: int(x) if x else None,
                "aspiration_id": lambda x: int(x) if x else None,
                "cylinder_head_type_id": lambda x: int(x) if x else None,
                "fuel_type_id": lambda x: int(x) if x else None,
                "ignition_system_type_id": lambda x: int(x) if x else None,
                "engine_mfr_id": lambda x: int(x) if x else None,
                "engine_version_id": lambda x: int(x) if x else None,
                "power_output_id": lambda x: int(x) if x else None,
            },
        )

        # EngineConfig2
        self.register_table_mapping(
            source_name=f"EngineConfig2{file_ext}",
            model_class=EngineConfig2,
            field_mapping={
                "engine_config_id": "EngineConfigID",
                "engine_designation_id": "EngineDesignationID",
                "engine_vin_id": "EngineVINID",
                "valves_id": "ValvesID",
                "engine_base_id": "EngineBaseID",
                "engine_block_id": "EngineBlockID",
                "engine_bore_stroke_id": "EngineBoreStrokeID",
                "fuel_delivery_config_id": "FuelDeliveryConfigID",
                "aspiration_id": "AspirationID",
                "cylinder_head_type_id": "CylinderHeadTypeID",
                "fuel_type_id": "FuelTypeID",
                "ignition_system_type_id": "IgnitionSystemTypeID",
                "engine_mfr_id": "EngineMfrID",
                "engine_version_id": "EngineVersionID",
                "power_output_id": "PowerOutputID",
            },
            primary_key="engine_config_id",
            transformers={
                "engine_config_id": lambda x: int(x) if x else None,
                "engine_designation_id": lambda x: int(x) if x else None,
                "engine_vin_id": lambda x: int(x) if x else None,
                "valves_id": lambda x: int(x) if x else None,
                "engine_base_id": lambda x: int(x) if x else None,
                "engine_block_id": lambda x: int(x) if x else None,
                "engine_bore_stroke_id": lambda x: int(x) if x else None,
                "fuel_delivery_config_id": lambda x: int(x) if x else None,
                "aspiration_id": lambda x: int(x) if x else None,
                "cylinder_head_type_id": lambda x: int(x) if x else None,
                "fuel_type_id": lambda x: int(x) if x else None,
                "ignition_system_type_id": lambda x: int(x) if x else None,
                "engine_mfr_id": lambda x: int(x) if x else None,
                "engine_version_id": lambda x: int(x) if x else None,
                "power_output_id": lambda x: int(x) if x else None,
            },
        )

    def _register_transmission_tables(self, file_ext: str) -> None:
        """
        Register transmission-related table mappings.

        Args:
            file_ext: File extension to use
        """
        # TransmissionType
        self.register_table_mapping(
            source_name=f"TransmissionType{file_ext}",
            model_class=TransmissionType,
            field_mapping={
                "transmission_type_id": "TransmissionTypeID",
                "name": "TransmissionTypeName",
            },
            primary_key="transmission_type_id",
            transformers={
                "transmission_type_id": lambda x: int(x) if x else None,
            },
        )

        # TransmissionNumSpeeds
        self.register_table_mapping(
            source_name=f"TransmissionNumSpeeds{file_ext}",
            model_class=TransmissionNumSpeeds,
            field_mapping={
                "transmission_num_speeds_id": "TransmissionNumSpeedsID",
                "num_speeds": "TransmissionNumSpeeds",
            },
            primary_key="transmission_num_speeds_id",
            transformers={
                "transmission_num_speeds_id": lambda x: int(x) if x else None,
            },
        )

        # TransmissionControlType
        self.register_table_mapping(
            source_name=f"TransmissionControlType{file_ext}",
            model_class=TransmissionControlType,
            field_mapping={
                "transmission_control_type_id": "TransmissionControlTypeID",
                "name": "TransmissionControlTypeName",
            },
            primary_key="transmission_control_type_id",
            transformers={
                "transmission_control_type_id": lambda x: int(x) if x else None,
            },
        )

        # TransmissionBase
        self.register_table_mapping(
            source_name=f"TransmissionBase{file_ext}",
            model_class=TransmissionBase,
            field_mapping={
                "transmission_base_id": "TransmissionBaseID",
                "transmission_type_id": "TransmissionTypeID",
                "transmission_num_speeds_id": "TransmissionNumSpeedsID",
                "transmission_control_type_id": "TransmissionControlTypeID",
            },
            primary_key="transmission_base_id",
            transformers={
                "transmission_base_id": lambda x: int(x) if x else None,
                "transmission_type_id": lambda x: int(x) if x else None,
                "transmission_num_speeds_id": lambda x: int(x) if x else None,
                "transmission_control_type_id": lambda x: int(x) if x else None,
            },
        )

        # TransmissionMfrCode
        self.register_table_mapping(
            source_name=f"TransmissionMfrCode{file_ext}",
            model_class=TransmissionMfrCode,
            field_mapping={
                "transmission_mfr_code_id": "TransmissionMfrCodeID",
                "code": "TransmissionMfrCode",
            },
            primary_key="transmission_mfr_code_id",
            transformers={
                "transmission_mfr_code_id": lambda x: int(x) if x else None,
            },
        )

        # ElecControlled
        self.register_table_mapping(
            source_name=f"ElecControlled{file_ext}",
            model_class=ElecControlled,
            field_mapping={
                "elec_controlled_id": "ElecControlledID",
                "value": "ElecControlled",
            },
            primary_key="elec_controlled_id",
            transformers={
                "elec_controlled_id": lambda x: int(x) if x else None,
            },
        )

        # Transmission
        self.register_table_mapping(
            source_name=f"Transmission{file_ext}",
            model_class=Transmission,
            field_mapping={
                "transmission_id": "TransmissionID",
                "transmission_base_id": "TransmissionBaseID",
                "transmission_mfr_code_id": "TransmissionMfrCodeID",
                "elec_controlled_id": "TransmissionElecControlledID",
                "transmission_mfr_id": "TransmissionMfrID",
            },
            primary_key="transmission_id",
            transformers={
                "transmission_id": lambda x: int(x) if x else None,
                "transmission_base_id": lambda x: int(x) if x else None,
                "transmission_mfr_code_id": lambda x: int(x) if x else None,
                "elec_controlled_id": lambda x: int(x) if x else None,
                "transmission_mfr_id": lambda x: int(x) if x else None,
            },
        )

    def _register_config_tables(self, file_ext: str) -> None:
        """
        Register configuration table mappings.

        Args:
            file_ext: File extension to use
        """
        # WheelBase
        self.register_table_mapping(
            source_name=f"WheelBase{file_ext}",
            model_class=WheelBase,
            field_mapping={
                "wheel_base_id": "WheelBaseID",
                "wheel_base": "WheelBase",
                "wheel_base_metric": "WheelBaseMetric",
            },
            primary_key="wheel_base_id",
            transformers={
                "wheel_base_id": lambda x: int(x) if x else None,
            },
        )

        # SpringType
        self.register_table_mapping(
            source_name=f"SpringType{file_ext}",
            model_class=SpringType,
            field_mapping={
                "spring_type_id": "SpringTypeID",
                "name": "SpringTypeName",
            },
            primary_key="spring_type_id",
            transformers={
                "spring_type_id": lambda x: int(x) if x else None,
            },
        )

        # SpringTypeConfig
        self.register_table_mapping(
            source_name=f"SpringTypeConfig{file_ext}",
            model_class=SpringTypeConfig,
            field_mapping={
                "spring_type_config_id": "SpringTypeConfigID",
                "front_spring_type_id": "FrontSpringTypeID",
                "rear_spring_type_id": "RearSpringTypeID",
            },
            primary_key="spring_type_config_id",
            transformers={
                "spring_type_config_id": lambda x: int(x) if x else None,
                "front_spring_type_id": lambda x: int(x) if x else None,
                "rear_spring_type_id": lambda x: int(x) if x else None,
            },
        )

        # SteeringType
        self.register_table_mapping(
            source_name=f"SteeringType{file_ext}",
            model_class=SteeringType,
            field_mapping={
                "steering_type_id": "SteeringTypeID",
                "name": "SteeringTypeName",
            },
            primary_key="steering_type_id",
            transformers={
                "steering_type_id": lambda x: int(x) if x else None,
            },
        )

        # SteeringSystem
        self.register_table_mapping(
            source_name=f"SteeringSystem{file_ext}",
            model_class=SteeringSystem,
            field_mapping={
                "steering_system_id": "SteeringSystemID",
                "name": "SteeringSystemName",
            },
            primary_key="steering_system_id",
            transformers={
                "steering_system_id": lambda x: int(x) if x else None,
            },
        )

        # SteeringConfig
        self.register_table_mapping(
            source_name=f"SteeringConfig{file_ext}",
            model_class=SteeringConfig,
            field_mapping={
                "steering_config_id": "SteeringConfigID",
                "steering_type_id": "SteeringTypeID",
                "steering_system_id": "SteeringSystemID",
            },
            primary_key="steering_config_id",
            transformers={
                "steering_config_id": lambda x: int(x) if x else None,
                "steering_type_id": lambda x: int(x) if x else None,
                "steering_system_id": lambda x: int(x) if x else None,
            },
        )

    def _register_many_to_many_tables(self, file_ext: str) -> None:
        """
        Register many-to-many table mappings.

        Args:
            file_ext: File extension to use
        """
        # VehicleToDriveType
        self.register_table_mapping(
            source_name=f"VehicleToDriveType{file_ext}",
            model_class=VehicleToDriveType,
            field_mapping={
                "vehicle_to_drive_type_id": "VehicleToDriveTypeID",
                "vehicle_id": "VehicleID",
                "drive_type_id": "DriveTypeID",
                "source": "Source",
            },
            primary_key="vehicle_to_drive_type_id",
            transformers={
                "vehicle_to_drive_type_id": lambda x: int(x) if x else None,
                "vehicle_id": lambda x: int(x) if x else None,
                "drive_type_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToBrakeConfig
        self.register_table_mapping(
            source_name=f"VehicleToBrakeConfig{file_ext}",
            model_class=VehicleToBrakeConfig,
            field_mapping={
                "vehicle_to_brake_config_id": "VehicleToBrakeConfigID",
                "vehicle_id": "VehicleID",
                "brake_config_id": "BrakeConfigID",
                "source": "Source",
            },
            primary_key="vehicle_to_brake_config_id",
            transformers={
                "vehicle_to_brake_config_id": lambda x: int(x) if x else None,
                "vehicle_id": lambda x: int(x) if x else None,
                "brake_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToBedConfig
        self.register_table_mapping(
            source_name=f"VehicleToBedConfig{file_ext}",
            model_class=VehicleToBedConfig,
            field_mapping={
                "vehicle_to_bed_config_id": "VehicleToBedConfigID",
                "vehicle_id": "VehicleID",
                "bed_config_id": "BedConfigID",
                "source": "Source",
            },
            primary_key="vehicle_to_bed_config_id",
            transformers={
                "vehicle_to_bed_config_id": lambda x: int(x) if x else None,
                "vehicle_id": lambda x: int(x) if x else None,
                "bed_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToBodyStyleConfig
        self.register_table_mapping(
            source_name=f"VehicleToBodyStyleConfig{file_ext}",
            model_class=VehicleToBodyStyleConfig,
            field_mapping={
                "vehicle_to_body_style_config_id": "VehicleToBodyStyleConfigID",
                "vehicle_id": "VehicleID",
                "body_style_config_id": "BodyStyleConfigID",
                "source": "Source",
            },
            primary_key="vehicle_to_body_style_config_id",
            transformers={
                "vehicle_to_body_style_config_id": lambda x: int(x) if x else None,
                "vehicle_id": lambda x: int(x) if x else None,
                "body_style_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToMfrBodyCode
        self.register_table_mapping(
            source_name=f"VehicleToMfrBodyCode{file_ext}",
            model_class=VehicleToMfrBodyCode,
            field_mapping={
                "vehicle_to_mfr_body_code_id": "VehicleToMfrBodyCodeID",
                "vehicle_id": "VehicleID",
                "mfr_body_code_id": "MfrBodyCodeID",
                "source": "Source",
            },
            primary_key="vehicle_to_mfr_body_code_id",
            transformers={
                "vehicle_to_mfr_body_code_id": lambda x: int(x) if x else None,
                "vehicle_id": lambda x: int(x) if x else None,
                "mfr_body_code_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToEngineConfig
        self.register_table_mapping(
            source_name=f"VehicleToEngineConfig{file_ext}",
            model_class=VehicleToEngineConfig,
            field_mapping={
                "vehicle_to_engine_config_id": "VehicleToEngineConfigID",
                "vehicle_id": "VehicleID",
                "engine_config_id": "EngineConfigID",
                "source": "Source",
            },
            primary_key="vehicle_to_engine_config_id",
            transformers={
                "vehicle_to_engine_config_id": lambda x: int(x) if x else None,
                "vehicle_id": lambda x: int(x) if x else None,
                "engine_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToSpringTypeConfig
        self.register_table_mapping(
            source_name=f"VehicleToSpringTypeConfig{file_ext}",
            model_class=VehicleToSpringTypeConfig,
            field_mapping={
                "vehicle_to_spring_type_config_id": "VehicleToSpringTypeConfigID",
                "vehicle_id": "VehicleID",
                "spring_type_config_id": "SpringTypeConfigID",
                "source": "Source",
            },
            primary_key="vehicle_to_spring_type_config_id",
            transformers={
                "vehicle_to_spring_type_config_id": lambda x: int(x) if x else None,
                "vehicle_id": lambda x: int(x) if x else None,
                "spring_type_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToSteeringConfig
        self.register_table_mapping(
            source_name=f"VehicleToSteeringConfig{file_ext}",
            model_class=VehicleToSteeringConfig,
            field_mapping={
                "vehicle_to_steering_config_id": "VehicleToSteeringConfigID",
                "vehicle_id": "VehicleID",
                "steering_config_id": "SteeringConfigID",
                "source": "Source",
            },
            primary_key="vehicle_to_steering_config_id",
            transformers={
                "vehicle_to_steering_config_id": lambda x: int(x) if x else None,
                "vehicle_id": lambda x: int(x) if x else None,
                "steering_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToTransmission
        self.register_table_mapping(
            source_name=f"VehicleToTransmission{file_ext}",
            model_class=VehicleToTransmission,
            field_mapping={
                "vehicle_to_transmission_id": "VehicleToTransmissionID",
                "vehicle_id": "VehicleID",
                "transmission_id": "TransmissionID",
                "source": "Source",
            },
            primary_key="vehicle_to_transmission_id",
            transformers={
                "vehicle_to_transmission_id": lambda x: int(x) if x else None,
                "vehicle_id": lambda x: int(x) if x else None,
                "transmission_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToWheelBase
        self.register_table_mapping(
            source_name=f"VehicleToWheelBase{file_ext}",
            model_class=VehicleToWheelBase,
            field_mapping={
                "vehicle_to_wheel_base_id": "VehicleToWheelbaseID",
                "vehicle_id": "VehicleID",
                "wheel_base_id": "WheelbaseID",
                "source": "Source",
            },
            primary_key="vehicle_to_wheel_base_id",
            transformers={
                "vehicle_to_wheel_base_id": lambda x: int(x) if x else None,
                "vehicle_id": lambda x: int(x) if x else None,
                "wheel_base_id": lambda x: int(x) if x else None,
            },
        )
