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

from app.domains.autocare.importers.flexible_importer import FlexibleImporter, SourceFormat, detect_source_format
from app.domains.autocare.vcdb.models import (
    Make, Year, Model, VehicleType, VehicleTypeGroup, SubModel,
    Region, BaseVehicle, Vehicle, DriveType, BrakeType, BrakeSystem,
    BrakeABS, BrakeConfig, BodyType, BodyNumDoors, BodyStyleConfig,
    EngineBlock, EngineBoreStroke, EngineBase, Aspiration, FuelType,
    CylinderHeadType, FuelDeliveryType, FuelDeliverySubType, FuelSystemControlType,
    FuelSystemDesign, FuelDeliveryConfig, EngineDesignation, EngineVIN, EngineVersion,
    Valves, Mfr, IgnitionSystemType, PowerOutput, EngineConfig,
    TransmissionType, TransmissionNumSpeeds, TransmissionControlType, TransmissionBase,
    TransmissionMfrCode, ElecControlled, Transmission, WheelBase, VCdbVersion,
    BedType, BedLength, BedConfig, MfrBodyCode, SpringType, SpringTypeConfig,
    SteeringType, SteeringSystem, SteeringConfig, PublicationStage
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
        batch_size: int = 1000
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
        self.set_import_order([
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
        ])

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
                "year_id": "YearId",
                "year": "YearName",
            },
            primary_key="year_id",
            transformers={
                "year_id": lambda x: int(x) if x else None,
                "year": lambda x: int(x) if x else None,
            },
        )

        # VehicleTypeGroup
        self.register_table_mapping(
            source_name=f"VehicleTypeGroup{file_ext}",
            model_class=VehicleTypeGroup,
            field_mapping={
                "vehicle_type_group_id": "VehicleTypeGroupId",
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
                "vehicle_type_id": "VehicleTypeId",
                "name": "VehicleTypeName",
                "vehicle_type_group_id": "VehicleTypeGroupId",
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
                "make_id": "MakeId",
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
                "model_id": "ModelId",
                "name": "ModelName",
                "vehicle_type_id": "VehicleTypeId",
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
                "submodel_id": "SubModelId",
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
                "region_id": "RegionId",
                "parent_id": "ParentId",
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
                "publication_stage_id": "PublicationStageId",
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
                "base_vehicle_id": "BaseVehicleId",
                "year_id": "YearId",
                "make_id": "MakeId",
                "model_id": "ModelId",
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
                "vehicle_id": "VehicleId",
                "base_vehicle_id": "BaseVehicleId",
                "submodel_id": "SubModelId",
                "region_id": "RegionId",
                "source": "Source",
                "publication_stage_id": "PublicationStageId",
                "publication_stage_source": "PublicationStageSource",
                "publication_stage_date": "PublicationStageDate",
            },
            primary_key="vehicle_id",
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "base_vehicle_id": lambda x: int(x) if x else None,
                "submodel_id": lambda x: int(x) if x else None,
                "region_id": lambda x: int(x) if x else None,
                "publication_stage_id": lambda x: int(x) if x else 4,  # Default to "Production"
                "publication_stage_date": lambda x: datetime.strptime(x, "%Y%m%d").date()
                if x and x.strip() else datetime.now().date(),
                "publication_stage_source": lambda x: x if x and x.strip() else "DataLoad",
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
                "drive_type_id": "DriveTypeId",
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
                "brake_type_id": "BrakeTypeId",
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
                "brake_system_id": "BrakeSystemId",
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
                "brake_abs_id": "BrakeABSId",
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
                "brake_config_id": "BrakeConfigId",
                "front_brake_type_id": "FrontBrakeTypeId",
                "rear_brake_type_id": "RearBrakeTypeId",
                "brake_system_id": "BrakeSystemId",
                "brake_abs_id": "BrakeABSId",
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
                "bed_type_id": "BedTypeId",
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
                "bed_length_id": "BedLengthId",
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
                "bed_config_id": "BedConfigId",
                "bed_length_id": "BedLengthId",
                "bed_type_id": "BedTypeId",
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
                "body_type_id": "BodyTypeId",
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
                "body_num_doors_id": "BodyNumDoorsId",
                "num_doors": "NumDoors",
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
                "body_style_config_id": "BodyStyleConfigId",
                "body_num_doors_id": "BodyNumDoorsId",
                "body_type_id": "BodyTypeId",
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
                "mfr_body_code_id": "MfrBodyCodeId",
                "code": "MfrBodyCode",
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
                "engine_block_id": "EngineBlockId",
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
                "engine_bore_stroke_id": "EngineBoreStrokeId",
                "bore_in": "BoreIn",
                "bore_metric": "BoreMetric",
                "stroke_in": "StrokeIn",
                "stroke_metric": "StrokeMetric",
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
                "mfr_id": "MfrId",
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
                "engine_base_id": "EngineBaseId",
                "engine_block_id": "EngineBlockId",
                "engine_bore_stroke_id": "EngineBoreStrokeId",
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
                "aspiration_id": "AspirationId",
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
                "fuel_type_id": "FuelTypeId",
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
                "cylinder_head_type_id": "CylinderHeadTypeId",
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
                "fuel_delivery_type_id": "FuelDeliveryTypeId",
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
                "fuel_delivery_subtype_id": "FuelDeliverySubTypeId",
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
                "fuel_system_control_type_id": "FuelSystemControlTypeId",
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
                "fuel_system_design_id": "FuelSystemDesignId",
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
                "fuel_delivery_config_id": "FuelDeliveryConfigId",
                "fuel_delivery_type_id": "FuelDeliveryTypeId",
                "fuel_delivery_subtype_id": "FuelDeliverySubTypeId",
                "fuel_system_control_type_id": "FuelSystemControlTypeId",
                "fuel_system_design_id": "FuelSystemDesignId",
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
                "engine_designation_id": "EngineDesignationId",
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
                "engine_vin_id": "EngineVINId",
                "code": "EngineVINCode",
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
                "engine_version_id": "EngineVersionId",
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
                "valves_id": "ValvesId",
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
                "ignition_system_type_id": "IgnitionSystemTypeId",
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
                "power_output_id": "PowerOutputId",
                "horsepower": "Horsepower",
                "kilowatt": "Kilowatt",
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
                "engine_config_id": "EngineConfigId",
                "engine_base_id": "EngineBaseId",
                "engine_designation_id": "EngineDesignationId",
                "engine_vin_id": "EngineVINId",
                "valves_id": "ValvesId",
                "fuel_delivery_config_id": "FuelDeliveryConfigId",
                "aspiration_id": "AspirationId",
                "cylinder_head_type_id": "CylinderHeadTypeId",
                "fuel_type_id": "FuelTypeId",
                "ignition_system_type_id": "IgnitionSystemTypeId",
                "engine_mfr_id": "EngineMfrId",
                "engine_version_id": "EngineVersionId",
                "power_output_id": "PowerOutputId",
            },
            primary_key="engine_config_id",
            transformers={
                "engine_config_id": lambda x: int(x) if x else None,
                "engine_base_id": lambda x: int(x) if x else None,
                "engine_designation_id": lambda x: int(x) if x else None,
                "engine_vin_id": lambda x: int(x) if x else None,
                "valves_id": lambda x: int(x) if x else None,
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
                "transmission_type_id": "TransmissionTypeId",
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
                "transmission_num_speeds_id": "TransmissionNumSpeedsId",
                "num_speeds": "NumSpeeds",
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
                "transmission_control_type_id": "TransmissionControlTypeId",
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
                "transmission_base_id": "TransmissionBaseId",
                "transmission_type_id": "TransmissionTypeId",
                "transmission_num_speeds_id": "TransmissionNumSpeedsId",
                "transmission_control_type_id": "TransmissionControlTypeId",
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
                "transmission_mfr_code_id": "TransmissionMfrCodeId",
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
                "elec_controlled_id": "ElecControlledId",
                "value": "ElecControlledValue",
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
                "transmission_id": "TransmissionId",
                "transmission_base_id": "TransmissionBaseId",
                "transmission_mfr_code_id": "TransmissionMfrCodeId",
                "elec_controlled_id": "ElecControlledId",
                "transmission_mfr_id": "TransmissionMfrId",
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
                "wheel_base_id": "WheelBaseId",
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
                "spring_type_id": "SpringTypeId",
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
                "spring_type_config_id": "SpringTypeConfigId",
                "front_spring_type_id": "FrontSpringTypeId",
                "rear_spring_type_id": "RearSpringTypeId",
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
                "steering_type_id": "SteeringTypeId",
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
                "steering_system_id": "SteeringSystemId",
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
                "steering_config_id": "SteeringConfigId",
                "steering_type_id": "SteeringTypeId",
                "steering_system_id": "SteeringSystemId",
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
        self.register_many_to_many_table(
            source_name=f"VehicleToDriveType{file_ext}",
            table_name="vehicle_to_drive_type",
            field_mapping={
                "vehicle_id": "VehicleId",
                "drive_type_id": "DriveTypeId",
                "source": "Source",
            },
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "drive_type_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToBrakeConfig
        self.register_many_to_many_table(
            source_name=f"VehicleToBrakeConfig{file_ext}",
            table_name="vehicle_to_brake_config",
            field_mapping={
                "vehicle_id": "VehicleId",
                "brake_config_id": "BrakeConfigId",
                "source": "Source",
            },
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "brake_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToBedConfig
        self.register_many_to_many_table(
            source_name=f"VehicleToBedConfig{file_ext}",
            table_name="vehicle_to_bed_config",
            field_mapping={
                "vehicle_id": "VehicleId",
                "bed_config_id": "BedConfigId",
                "source": "Source",
            },
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "bed_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToBodyStyleConfig
        self.register_many_to_many_table(
            source_name=f"VehicleToBodyStyleConfig{file_ext}",
            table_name="vehicle_to_body_style_config",
            field_mapping={
                "vehicle_id": "VehicleId",
                "body_style_config_id": "BodyStyleConfigId",
                "source": "Source",
            },
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "body_style_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToMfrBodyCode
        self.register_many_to_many_table(
            source_name=f"VehicleToMfrBodyCode{file_ext}",
            table_name="vehicle_to_mfr_body_code",
            field_mapping={
                "vehicle_id": "VehicleId",
                "mfr_body_code_id": "MfrBodyCodeId",
                "source": "Source",
            },
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "mfr_body_code_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToEngineConfig
        self.register_many_to_many_table(
            source_name=f"VehicleToEngineConfig{file_ext}",
            table_name="vehicle_to_engine_config",
            field_mapping={
                "vehicle_id": "VehicleId",
                "engine_config_id": "EngineConfigId",
                "source": "Source",
            },
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "engine_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToSpringTypeConfig
        self.register_many_to_many_table(
            source_name=f"VehicleToSpringTypeConfig{file_ext}",
            table_name="vehicle_to_spring_type_config",
            field_mapping={
                "vehicle_id": "VehicleId",
                "spring_type_config_id": "SpringTypeConfigId",
                "source": "Source",
            },
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "spring_type_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToSteeringConfig
        self.register_many_to_many_table(
            source_name=f"VehicleToSteeringConfig{file_ext}",
            table_name="vehicle_to_steering_config",
            field_mapping={
                "vehicle_id": "VehicleId",
                "steering_config_id": "SteeringConfigId",
                "source": "Source",
            },
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "steering_config_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToTransmission
        self.register_many_to_many_table(
            source_name=f"VehicleToTransmission{file_ext}",
            table_name="vehicle_to_transmission",
            field_mapping={
                "vehicle_id": "VehicleId",
                "transmission_id": "TransmissionId",
                "source": "Source",
            },
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "transmission_id": lambda x: int(x) if x else None,
            },
        )

        # VehicleToWheelBase
        self.register_many_to_many_table(
            source_name=f"VehicleToWheelBase{file_ext}",
            table_name="vehicle_to_wheel_base",
            field_mapping={
                "vehicle_id": "VehicleId",
                "wheel_base_id": "WheelBaseId",
                "source": "Source",
            },
            transformers={
                "vehicle_id": lambda x: int(x) if x else None,
                "wheel_base_id": lambda x: int(x) if x else None,
            },
        )
