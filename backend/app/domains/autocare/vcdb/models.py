from __future__ import annotations

"""VCdb (Vehicle Component Database) models.

This module defines the SQLAlchemy models that correspond to the VCdb database schema.
These models represent vehicle information and their components according to
Auto Care Association standards.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Make(Base):
    """Make entity representing vehicle manufacturers.

    Attributes:
        id: Primary key.
        make_id: VCdb specific ID.
        name: Make name.
        vehicles: Relationship to vehicles.
        base_vehicles: Relationship to base vehicles.
    """

    __tablename__ = "make"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    make_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Relationships
    vehicles: Mapped[List["Vehicle"]] = relationship(
        "Vehicle",
        secondary="vcdb.base_vehicle",
        primaryjoin="Make.make_id == BaseVehicle.make_id",
        secondaryjoin="BaseVehicle.base_vehicle_id == Vehicle.base_vehicle_id",
        viewonly=True,
    )
    base_vehicles: Mapped[List["BaseVehicle"]] = relationship(
        "BaseVehicle", back_populates="make"
    )

    def __repr__(self) -> str:
        """Return string representation of Make instance.

        Returns:
            String representation.
        """
        return f"<Make {self.name} ({self.make_id})>"


class Year(Base):
    """Year entity representing vehicle model years.

    Attributes:
        id: Primary key.
        year_id: VCdb specific ID.
        base_vehicles: Relationship to base vehicles.
    """

    __tablename__ = "year"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    year_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )

    # Relationships
    base_vehicles: Mapped[List["BaseVehicle"]] = relationship(
        "BaseVehicle", back_populates="year"
    )

    def __repr__(self) -> str:
        """Return string representation of Year instance.

        Returns:
            String representation.
        """
        return f"<Year {self.year_id}>"


class Model(Base):
    """Model entity representing vehicle models.

    Attributes:
        id: Primary key.
        model_id: VCdb specific ID.
        name: Model name.
        vehicle_type_id: Reference to vehicle type.
        base_vehicles: Relationship to base vehicles.
        vehicle_type: Relationship to vehicle type.
    """

    __tablename__ = "model"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    model_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    vehicle_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.vehicle_type.vehicle_type_id"), nullable=False
    )

    # Relationships
    base_vehicles: Mapped[List["BaseVehicle"]] = relationship(
        "BaseVehicle", back_populates="model"
    )
    vehicle_type: Mapped["VehicleType"] = relationship(
        "VehicleType", back_populates="models"
    )

    def __repr__(self) -> str:
        """Return string representation of Model instance.

        Returns:
            String representation.
        """
        return f"<Model {self.name} ({self.model_id})>"


class VehicleType(Base):
    """VehicleType entity representing types of vehicles.

    Attributes:
        id: Primary key.
        vehicle_type_id: VCdb specific ID.
        name: Vehicle type name.
        vehicle_type_group_id: Optional reference to vehicle type group.
        models: Relationship to models.
        vehicle_type_group: Relationship to vehicle type group.
    """

    __tablename__ = "vehicle_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vehicle_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    vehicle_type_group_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("vcdb.vehicle_type_group.vehicle_type_group_id"),
        nullable=True,
    )

    # Relationships
    models: Mapped[List["Model"]] = relationship("Model", back_populates="vehicle_type")
    vehicle_type_group: Mapped["VehicleTypeGroup"] = relationship(
        "VehicleTypeGroup", back_populates="vehicle_types"
    )

    def __repr__(self) -> str:
        """Return string representation of VehicleType instance.

        Returns:
            String representation.
        """
        return f"<VehicleType {self.name} ({self.vehicle_type_id})>"


class VehicleTypeGroup(Base):
    """VehicleTypeGroup entity representing groups of vehicle types.

    Attributes:
        id: Primary key.
        vehicle_type_group_id: VCdb specific ID.
        name: Vehicle type group name.
        vehicle_types: Relationship to vehicle types.
    """

    __tablename__ = "vehicle_type_group"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vehicle_type_group_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Relationships
    vehicle_types: Mapped[List["VehicleType"]] = relationship(
        "VehicleType", back_populates="vehicle_type_group"
    )

    def __repr__(self) -> str:
        """Return string representation of VehicleTypeGroup instance.

        Returns:
            String representation.
        """
        return f"<VehicleTypeGroup {self.name} ({self.vehicle_type_group_id})>"


class SubModel(Base):
    """SubModel entity representing vehicle submodels.

    Attributes:
        id: Primary key.
        submodel_id: VCdb specific ID.
        name: Submodel name.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "submodel"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    submodel_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Relationships
    vehicles: Mapped[List["Vehicle"]] = relationship(
        "Vehicle", back_populates="submodel"
    )

    def __repr__(self) -> str:
        """Return string representation of SubModel instance.

        Returns:
            String representation.
        """
        return f"<SubModel {self.name} ({self.submodel_id})>"


class Region(Base):
    """Region entity representing geographic regions.

    Attributes:
        id: Primary key.
        region_id: VCdb specific ID.
        parent_id: Optional reference to parent region.
        abbr: Region abbreviation.
        name: Region name.
        children: Relationship to child regions.
        parent: Relationship to parent region.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "region"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    region_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("vcdb.region.region_id"), nullable=True
    )
    abbr: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    parent: Mapped["Region"] = relationship(
        "Region", remote_side="Region.region_id", back_populates="children"
    )
    children: Mapped[List["Region"]] = relationship(
        "Region", back_populates="parent", cascade="all, delete-orphan"
    )
    vehicles: Mapped[List["Vehicle"]] = relationship("Vehicle", back_populates="region")

    def __repr__(self) -> str:
        """Return string representation of Region instance.

        Returns:
            String representation.
        """
        return f"<Region {self.name} ({self.region_id})>"


class PublicationStage(Base):
    """PublicationStage entity representing publication stages for vehicle data.

    Attributes:
        id: Primary key.
        publication_stage_id: VCdb specific ID.
        name: Publication stage name.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "publication_stage"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    publication_stage_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # Relationships
    vehicles: Mapped[List["Vehicle"]] = relationship(
        "Vehicle", back_populates="publication_stage"
    )

    def __repr__(self) -> str:
        """Return string representation of PublicationStage instance.

        Returns:
            String representation.
        """
        return f"<PublicationStage {self.name} ({self.publication_stage_id})>"


class BaseVehicle(Base):
    """BaseVehicle entity representing basic vehicle identification.

    Attributes:
        id: Primary key.
        base_vehicle_id: VCdb specific ID.
        year_id: Reference to year.
        make_id: Reference to make.
        model_id: Reference to model.
        year: Relationship to year.
        make: Relationship to make.
        model: Relationship to model.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "base_vehicle"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    base_vehicle_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    year_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.year.year_id"), nullable=False
    )
    make_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.make.make_id"), nullable=False
    )
    model_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.model.model_id"), nullable=False
    )

    # Relationships
    year: Mapped["Year"] = relationship("Year", back_populates="base_vehicles")
    make: Mapped["Make"] = relationship("Make", back_populates="base_vehicles")
    model: Mapped["Model"] = relationship("Model", back_populates="base_vehicles")
    vehicles: Mapped[List["Vehicle"]] = relationship(
        "Vehicle", back_populates="base_vehicle"
    )

    def __repr__(self) -> str:
        """Return string representation of BaseVehicle instance.

        Returns:
            String representation.
        """
        return f"<BaseVehicle {self.base_vehicle_id}>"


class Vehicle(Base):
    """Vehicle entity representing specific vehicle configurations.

    Attributes:
        id: Primary key.
        vehicle_id: VCdb specific ID.
        base_vehicle_id: Reference to base vehicle.
        submodel_id: Reference to submodel.
        region_id: Reference to region.
        source: Data source information.
        publication_stage_id: Reference to publication stage.
        publication_stage_source: Source of publication stage.
        publication_stage_date: Date of publication stage.
        base_vehicle: Relationship to base vehicle.
        submodel: Relationship to submodel.
        region: Relationship to region.
        publication_stage: Relationship to publication stage.
        make: Relationship to make (through base_vehicle).
        year: Year value (through base_vehicle.year).
        model: Model name (through base_vehicle.model).
    """

    __tablename__ = "vehicle"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vehicle_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    base_vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.base_vehicle.base_vehicle_id"), nullable=False
    )
    submodel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.submodel.submodel_id"), nullable=False
    )
    region_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.region.region_id"), nullable=False
    )
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    publication_stage_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.publication_stage.publication_stage_id"),
        nullable=False,
        default=4,
    )
    publication_stage_source: Mapped[str] = mapped_column(String(100), nullable=False)
    publication_stage_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )

    # Relationships
    base_vehicle: Mapped["BaseVehicle"] = relationship(
        "BaseVehicle", back_populates="vehicles"
    )
    submodel: Mapped["SubModel"] = relationship("SubModel", back_populates="vehicles")
    region: Mapped["Region"] = relationship("Region", back_populates="vehicles")
    publication_stage: Mapped["PublicationStage"] = relationship(
        "PublicationStage", back_populates="vehicles"
    )

    # Vehicle attributes relationships
    drive_types: Mapped[List["DriveType"]] = relationship(
        "DriveType", secondary="vcdb.vehicle_to_drive_type"
    )
    brake_configs: Mapped[List["BrakeConfig"]] = relationship(
        "BrakeConfig", secondary="vcdb.vehicle_to_brake_config"
    )
    bed_configs: Mapped[List["BedConfig"]] = relationship(
        "BedConfig", secondary="vcdb.vehicle_to_bed_config"
    )
    body_style_configs: Mapped[List["BodyStyleConfig"]] = relationship(
        "BodyStyleConfig", secondary="vcdb.vehicle_to_body_style_config"
    )
    mfr_body_codes: Mapped[List["MfrBodyCode"]] = relationship(
        "MfrBodyCode", secondary="vcdb.vehicle_to_mfr_body_code"
    )
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", secondary="vcdb.vehicle_to_engine_config"
    )
    spring_type_configs: Mapped[List["SpringTypeConfig"]] = relationship(
        "SpringTypeConfig", secondary="vcdb.vehicle_to_spring_type_config"
    )
    steering_configs: Mapped[List["SteeringConfig"]] = relationship(
        "SteeringConfig", secondary="vcdb.vehicle_to_steering_config"
    )
    transmissions: Mapped[List["Transmission"]] = relationship(
        "Transmission", secondary="vcdb.vehicle_to_transmission"
    )
    wheel_bases: Mapped[List["WheelBase"]] = relationship(
        "WheelBase", secondary="vcdb.vehicle_to_wheel_base"
    )

    # Properties for convenience
    @property
    def make(self) -> Make:
        """Get the make of this vehicle.

        Returns:
            Make object.
        """
        return self.base_vehicle.make

    @property
    def year(self) -> Optional[int]:
        """Get the year of this vehicle.

        Returns:
            Year value.
        """
        if self.base_vehicle and self.base_vehicle.year:
            return self.base_vehicle.year.year_id
        return None

    @property
    def model(self) -> str:
        """Get the model of this vehicle.

        Returns:
            Model name.
        """
        return self.base_vehicle.model.name

    def __repr__(self) -> str:
        """Return string representation of Vehicle instance.

        Returns:
            String representation.
        """
        return f"<Vehicle {self.vehicle_id}>"


# Vehicle attribute tables


class DriveType(Base):
    """DriveType entity representing types of drive systems.

    Attributes:
        id: Primary key.
        drive_type_id: VCdb specific ID.
        name: Drive type name.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "drive_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    drive_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    def __repr__(self) -> str:
        """Return string representation of DriveType instance.

        Returns:
            String representation.
        """
        return f"<DriveType {self.name} ({self.drive_type_id})>"


# Vehicle to DriveType association table
class VehicleToDriveType(Base):
    """
    Represents the VehicleToDriveType entity linking vehicles with drive types.

    This class defines the relationship between a vehicle and a drive type,
    providing a mapping structure used within the vcdb schema. It supports optional
    source metadata for tracking the origin of the data.

    Attributes:
        id (uuid.UUID): Primary key uniquely identifying each entry.
        vehicle_to_drive_type_id (int): Unique identifier for this specific vehicle-to-drive-type mapping.
        vehicle_id (int): Foreign key referencing the associated vehicle.
        drive_type_id (int): Foreign key referencing the associated drive type.
        source (Optional[str]): Optional metadata field indicating the data origin, limited to 10 characters.
    """

    __tablename__ = "vehicle_to_drive_type"
    __table_args__ = {"schema": "vcdb"}

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Unique mapping identifier
    vehicle_to_drive_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )

    # Foreign key linking to the vehicle
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.vehicle.vehicle_id"), nullable=False
    )

    # Foreign key linking to the drive type
    drive_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.drive_type.drive_type_id"), nullable=False
    )

    # Optional source metadata
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<VehicleToDriveType(id={self.id}, vehicle_to_drive_type_id={self.vehicle_to_drive_type_id}, "
            f"vehicle_id={self.vehicle_id}, drive_type_id={self.drive_type_id}, source={self.source})>"
        )


class BrakeType(Base):
    """BrakeType entity representing types of brake systems.

    Attributes:
        id: Primary key.
        brake_type_id: VCdb specific ID.
        name: Brake type name.
        front_brake_configs: Relationship to brake configs (as front).
        rear_brake_configs: Relationship to brake configs (as rear).
    """

    __tablename__ = "brake_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    brake_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    front_brake_configs: Mapped[List["BrakeConfig"]] = relationship(
        "BrakeConfig",
        primaryjoin="BrakeType.brake_type_id == BrakeConfig.front_brake_type_id",
        back_populates="front_brake_type",
    )
    rear_brake_configs: Mapped[List["BrakeConfig"]] = relationship(
        "BrakeConfig",
        primaryjoin="BrakeType.brake_type_id == BrakeConfig.rear_brake_type_id",
        back_populates="rear_brake_type",
    )

    def __repr__(self) -> str:
        """Return string representation of BrakeType instance.

        Returns:
            String representation.
        """
        return f"<BrakeType {self.name} ({self.brake_type_id})>"


class BrakeSystem(Base):
    """BrakeSystem entity representing brake system configurations.

    Attributes:
        id: Primary key.
        brake_system_id: VCdb specific ID.
        name: Brake system name.
        brake_configs: Relationship to brake configs.
    """

    __tablename__ = "brake_system"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    brake_system_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    brake_configs: Mapped[List["BrakeConfig"]] = relationship(
        "BrakeConfig", back_populates="brake_system"
    )

    def __repr__(self) -> str:
        """Return string representation of BrakeSystem instance.

        Returns:
            String representation.
        """
        return f"<BrakeSystem {self.name} ({self.brake_system_id})>"


class BrakeABS(Base):
    """BrakeABS entity representing ABS configurations.

    Attributes:
        id: Primary key.
        brake_abs_id: VCdb specific ID.
        name: ABS configuration name.
        brake_configs: Relationship to brake configs.
    """

    __tablename__ = "brake_abs"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    brake_abs_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    brake_configs: Mapped[List["BrakeConfig"]] = relationship(
        "BrakeConfig", back_populates="brake_abs"
    )

    def __repr__(self) -> str:
        """Return string representation of BrakeABS instance.

        Returns:
            String representation.
        """
        return f"<BrakeABS {self.name} ({self.brake_abs_id})>"


class BrakeConfig(Base):
    """BrakeConfig entity representing complete brake configurations.

    Attributes:
        id: Primary key.
        brake_config_id: VCdb specific ID.
        front_brake_type_id: Reference to front brake type.
        rear_brake_type_id: Reference to rear brake type.
        brake_system_id: Reference to brake system.
        brake_abs_id: Reference to ABS configuration.
        front_brake_type: Relationship to front brake type.
        rear_brake_type: Relationship to rear brake type.
        brake_system: Relationship to brake system.
        brake_abs: Relationship to ABS configuration.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "brake_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    brake_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    front_brake_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.brake_type.brake_type_id"), nullable=False
    )
    rear_brake_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.brake_type.brake_type_id"), nullable=False
    )
    brake_system_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.brake_system.brake_system_id"), nullable=False
    )
    brake_abs_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.brake_abs.brake_abs_id"), nullable=False
    )

    # Relationships
    front_brake_type: Mapped["BrakeType"] = relationship(
        "BrakeType",
        primaryjoin="BrakeConfig.front_brake_type_id == BrakeType.brake_type_id",
        back_populates="front_brake_configs",
    )
    rear_brake_type: Mapped["BrakeType"] = relationship(
        "BrakeType",
        primaryjoin="BrakeConfig.rear_brake_type_id == BrakeType.brake_type_id",
        back_populates="rear_brake_configs",
    )
    brake_system: Mapped["BrakeSystem"] = relationship(
        "BrakeSystem", back_populates="brake_configs"
    )
    brake_abs: Mapped["BrakeABS"] = relationship(
        "BrakeABS", back_populates="brake_configs"
    )

    def __repr__(self) -> str:
        """Return string representation of BrakeConfig instance.

        Returns:
            String representation.
        """
        return f"<BrakeConfig {self.brake_config_id}>"


# Vehicle to BrakeConfig association table
class VehicleToBrakeConfig(Base):
    """
    Represents the VehicleToBrakeConfig entity linking vehicles with brake configurations.

    This class maps the relationship between a vehicle and a brake configuration in the
    database, recording and storing the association along with optional metadata regarding
    the source system. It primarily serves as part of a schema in the vcdb module.

    Attributes:
        id (uuid.UUID): The primary key uniquely identifying each entry.
        config_id (int): The unique identifier for this specific vehicle to brake configuration.
        vehicle_id (int): Foreign key referencing the associated vehicle ID.
        brake_config_id (int): Foreign key referencing the associated brake configuration ID.
        source_system (Optional[str]): An optional metadata field indicating the data source
        of the configuration, limited to 10 characters for storage.
    """

    __tablename__ = "vehicle_to_brake_config"
    __table_args__ = {"schema": "vcdb"}

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Unique identifier for this configuration
    vehicle_to_brake_config_id: Mapped[int] = mapped_column(
        "vehicle_to_brake_config_id", Integer, nullable=False, unique=True, index=True
    )

    # Foreign key linking to the vehicle
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.vehicle.vehicle_id"), nullable=False
    )

    # Foreign key linking to the brake configuration
    brake_config_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.brake_config.brake_config_id"), nullable=False
    )

    # Optional metadata about the source system (e.g., data origin)
    source: Mapped[Optional[str]] = mapped_column("source", String(10), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<VehicleToBrakeConfig(id={self.id}, config_id={self.vehicle_to_brake_config_id}, "
            f"vehicle_id={self.vehicle_id}, brake_config_id={self.brake_config_id}, "
            f"source={self.source})>"
        )


class BedType(Base):
    """BedType entity representing types of vehicle beds.

    Attributes:
        id: Primary key.
        bed_type_id: VCdb specific ID.
        name: Bed type name.
        bed_configs: Relationship to bed configs.
    """

    __tablename__ = "bed_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    bed_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Relationships
    bed_configs: Mapped[List["BedConfig"]] = relationship(
        "BedConfig", back_populates="bed_type"
    )

    def __repr__(self) -> str:
        """Return string representation of BedType instance.

        Returns:
            String representation.
        """
        return f"<BedType {self.name} ({self.bed_type_id})>"


class BedLength(Base):
    """BedLength entity representing bed length measurements.

    Attributes:
        id: Primary key.
        bed_length_id: VCdb specific ID.
        length: Bed length in imperial units.
        length_metric: Bed length in metric units.
        bed_configs: Relationship to bed configs.
    """

    __tablename__ = "bed_length"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    bed_length_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    length: Mapped[str] = mapped_column(String(10), nullable=False)
    length_metric: Mapped[str] = mapped_column(String(10), nullable=False)

    # Relationships
    bed_configs: Mapped[List["BedConfig"]] = relationship(
        "BedConfig", back_populates="bed_length"
    )

    def __repr__(self) -> str:
        """Return string representation of BedLength instance.

        Returns:
            String representation.
        """
        return f"<BedLength {self.length} ({self.bed_length_id})>"


class BedConfig(Base):
    """BedConfig entity representing bed configurations.

    Attributes:
        id: Primary key.
        bed_config_id: VCdb specific ID.
        bed_length_id: Reference to bed length.
        bed_type_id: Reference to bed type.
        bed_length: Relationship to bed length.
        bed_type: Relationship to bed type.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "bed_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    bed_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    bed_length_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.bed_length.bed_length_id"), nullable=False
    )
    bed_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.bed_type.bed_type_id"), nullable=False
    )

    # Relationships
    bed_length: Mapped["BedLength"] = relationship(
        "BedLength", back_populates="bed_configs"
    )
    bed_type: Mapped["BedType"] = relationship("BedType", back_populates="bed_configs")

    def __repr__(self) -> str:
        """Return string representation of BedConfig instance.

        Returns:
            String representation.
        """
        return f"<BedConfig {self.bed_config_id}>"


class VehicleToBedConfig(Base):
    """
    Represents the association between a vehicle and a bed configuration in the VCDB schema.

    Attributes:
        id (UUID): Primary key, a universally unique identifier for the record.
        vehicle_to_bed_config_id (int): Unique identifier for the vehicle-to-bed configuration.
        vehicle_id (int): Foreign key referencing the vehicle table.
        bed_config_id (int): Foreign key referencing the bed configuration table.
        source (str): Represents the source information, optional.
    """

    __tablename__ = "vehicle_to_bed_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vehicle_to_bed_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.vehicle.vehicle_id"), nullable=False
    )
    bed_config_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.bed_config.bed_config_id"), nullable=False
    )
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    def __repr__(self) -> str:
        """
        Returns a string representation of the VehicleToBedConfig object.
        """
        return (
            f"<VehicleToBedConfig("
            f"id={self.id}, "
            f"vehicle_to_bed_config_id={self.vehicle_to_bed_config_id}, "
            f"vehicle_id={self.vehicle_id}, "
            f"bed_config_id={self.bed_config_id}, "
            f"source={self.source}"
            f")>"
        )


class BodyType(Base):
    """BodyType entity representing types of vehicle bodies.

    Attributes:
        id: Primary key.
        body_type_id: VCdb specific ID.
        name: Body type name.
        body_style_configs: Relationship to body style configs.
    """

    __tablename__ = "body_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    body_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Relationships
    body_style_configs: Mapped[List["BodyStyleConfig"]] = relationship(
        "BodyStyleConfig", back_populates="body_type"
    )

    def __repr__(self) -> str:
        """Return string representation of BodyType instance.

        Returns:
            String representation.
        """
        return f"<BodyType {self.name} ({self.body_type_id})>"


class BodyNumDoors(Base):
    """BodyNumDoors entity representing number of doors.

    Attributes:
        id: Primary key.
        body_num_doors_id: VCdb specific ID.
        num_doors: Number of doors string.
        body_style_configs: Relationship to body style configs.
    """

    __tablename__ = "body_num_doors"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    body_num_doors_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    num_doors: Mapped[str] = mapped_column(String(3), nullable=False)

    # Relationships
    body_style_configs: Mapped[List["BodyStyleConfig"]] = relationship(
        "BodyStyleConfig", back_populates="body_num_doors"
    )

    def __repr__(self) -> str:
        """Return string representation of BodyNumDoors instance.

        Returns:
            String representation.
        """
        return f"<BodyNumDoors {self.num_doors} ({self.body_num_doors_id})>"


class BodyStyleConfig(Base):
    """BodyStyleConfig entity representing body style configurations.

    Attributes:
        id: Primary key.
        body_style_config_id: VCdb specific ID.
        body_num_doors_id: Reference to body number of doors.
        body_type_id: Reference to body type.
        body_num_doors: Relationship to body number of doors.
        body_type: Relationship to body type.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "body_style_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    body_style_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    body_num_doors_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.body_num_doors.body_num_doors_id"), nullable=False
    )
    body_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.body_type.body_type_id"), nullable=False
    )

    # Relationships
    body_num_doors: Mapped["BodyNumDoors"] = relationship(
        "BodyNumDoors", back_populates="body_style_configs"
    )
    body_type: Mapped["BodyType"] = relationship(
        "BodyType", back_populates="body_style_configs"
    )

    def __repr__(self) -> str:
        """Return string representation of BodyStyleConfig instance.

        Returns:
            String representation.
        """
        return f"<BodyStyleConfig {self.body_style_config_id}>"


# Vehicle to BodyStyleConfig association table
class VehicleToBodyStyleConfig(Base):
    """
    Represents the mapping between vehicles and their associated body style configurations.

    Attributes:
        id (UUID): Primary key, a unique identifier for each mapping record, generated automatically.
        vehicle_to_body_style_config_id (int): A unique identifier for the relationship,
            indexed and must not be null.
        vehicle_id (int): Foreign key linking to the 'vehicle' table in the 'vcdb' schema, must not be null.
        body_style_config_id (int): Foreign key linking to the 'body_style_config' table
            in the 'vcdb' schema, must not be null.
        source (str): An optional string (up to 10 characters) to denote the source of the mapping.
    """

    __tablename__ = "vehicle_to_body_style_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vehicle_to_body_style_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.vehicle.vehicle_id"), nullable=False
    )
    body_style_config_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.body_style_config.body_style_config_id"),
        nullable=False,
    )
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<VehicleToBodyStyleConfig("
            f"id={self.id}, vehicle_to_body_style_config_id={self.vehicle_to_body_style_config_id}, "
            f"vehicle_id={self.vehicle_id}, body_style_config_id={self.body_style_config_id}, "
            f"source={self.source})>"
        )


class MfrBodyCode(Base):
    """MfrBodyCode entity representing manufacturer body codes.

    Attributes:
        id: Primary key.
        mfr_body_code_id: VCdb specific ID.
        code: Body code value.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "mfr_body_code"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    mfr_body_code_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)

    def __repr__(self) -> str:
        """Return string representation of MfrBodyCode instance.

        Returns:
            String representation.
        """
        return f"<MfrBodyCode {self.code} ({self.mfr_body_code_id})>"


# Vehicle to MfrBodyCode association table
class VehicleToMfrBodyCode(Base):
    """
    Represents the mapping between vehicles and their manufacturer-specific body codes.

    Attributes:
        id (UUID): Primary key, a unique identifier for each mapping record, generated automatically.
        vehicle_to_mfr_body_code_id (int): A unique identifier for the relationship,
            indexed and must not be null.
        vehicle_id (int): Foreign key linking to the 'vehicle' table in the 'vcdb' schema, must not be null.
        mfr_body_code_id (int): Foreign key linking to the 'mfr_body_code' table
            in the 'vcdb' schema, must not be null.
        source (str): An optional string (up to 10 characters) to denote the source of the mapping.
    """

    __tablename__ = "vehicle_to_mfr_body_code"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vehicle_to_mfr_body_code_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.vehicle.vehicle_id"), nullable=False
    )
    mfr_body_code_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.mfr_body_code.mfr_body_code_id"), nullable=False
    )
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<VehicleToMfrBodyCode("
            f"id={self.id}, vehicle_to_mfr_body_code_id={self.vehicle_to_mfr_body_code_id}, "
            f"vehicle_id={self.vehicle_id}, mfr_body_code_id={self.mfr_body_code_id}, "
            f"source={self.source})>"
        )


class EngineBlock(Base):
    """EngineBlock entity representing engine block specifications.

    Attributes:
        id: Primary key.
        engine_block_id: VCdb specific ID.
        liter: Engine size in liters.
        cc: Engine size in cubic centimeters.
        cid: Engine size in cubic inches displacement.
        cylinders: Number of cylinders.
        block_type: Engine block type.
        engine_bases: Relationship to engine bases.
    """

    __tablename__ = "engine_block"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    engine_block_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    liter: Mapped[str] = mapped_column(String(6), nullable=False)
    cc: Mapped[str] = mapped_column(String(8), nullable=False)
    cid: Mapped[str] = mapped_column(String(7), nullable=False)
    cylinders: Mapped[str] = mapped_column(String(2), nullable=False)
    block_type: Mapped[str] = mapped_column(String(2), nullable=False)

    # Relationships
    engine_bases: Mapped[List["EngineBase2"]] = relationship(
        "EngineBase2", back_populates="engine_block"
    )
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="engine_block"
    )

    def __repr__(self) -> str:
        """Return string representation of EngineBlock instance.

        Returns:
            String representation.
        """
        return (
            f"<EngineBlock {self.liter}L {self.cylinders}cyl ({self.engine_block_id})>"
        )


class EngineBoreStroke(Base):
    """EngineBoreStroke entity representing engine bore and stroke measurements.

    Attributes:
        id: Primary key.
        engine_bore_stroke_id: VCdb specific ID.
        bore_in: Bore measurement in inches.
        bore_metric: Bore measurement in metric.
        stroke_in: Stroke measurement in inches.
        stroke_metric: Stroke measurement in metric.
        engine_bases: Relationship to engine bases.
    """

    __tablename__ = "engine_bore_stroke"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    engine_bore_stroke_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    bore_in: Mapped[str] = mapped_column(String(10), nullable=False)
    bore_metric: Mapped[str] = mapped_column(String(10), nullable=False)
    stroke_in: Mapped[str] = mapped_column(String(10), nullable=False)
    stroke_metric: Mapped[str] = mapped_column(String(10), nullable=False)

    # Relationships
    engine_bases: Mapped[List["EngineBase2"]] = relationship(
        "EngineBase2", back_populates="engine_bore_stroke"
    )
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="engine_bore_stroke"
    )

    def __repr__(self) -> str:
        """Return string representation of EngineBoreStroke instance.

        Returns:
            String representation.
        """
        return f"<EngineBoreStroke {self.bore_in}x{self.stroke_in} ({self.engine_bore_stroke_id})>"


class EngineBase(Base):
    """Legacy EngineBase entity.

    This class is maintained for backward compatibility but has been replaced by EngineBase2.
    New code should use EngineBase2 instead.

    Attributes:
        id: Primary key.
        engine_base_id: VCdb specific ID.
        liter: Engine displacement in liters.
        cc: Engine displacement in cubic centimeters.
        cid: Engine displacement in cubic inches.
        cylinders: Number of cylinders.
        block_type: Configuration of the engine block.
        eng_bore_in: Engine bore in inches.
        eng_bore_metric: Engine bore in millimeters.
        eng_stroke_in: Engine stroke in inches.
        eng_stroke_metric: Engine stroke in millimeters.
    """

    __tablename__ = "engine_base"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    engine_base_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )

    # New fields based on provided data
    liter: Mapped[str] = mapped_column(String(10), nullable=False)
    cc: Mapped[str] = mapped_column(String(10), nullable=False)
    cid: Mapped[str] = mapped_column(String(10), nullable=False)
    cylinders: Mapped[str] = mapped_column(String(10), nullable=False)
    block_type: Mapped[str] = mapped_column(String(10), nullable=False)
    eng_bore_in: Mapped[str] = mapped_column(String(10), nullable=False)
    eng_bore_metric: Mapped[str] = mapped_column(String(10), nullable=False)
    eng_stroke_in: Mapped[str] = mapped_column(String(10), nullable=False)
    eng_stroke_metric: Mapped[str] = mapped_column(String(10), nullable=False)

    def __repr__(self) -> str:
        """Return string representation of EngineBase instance."""
        return f"<EngineBase {self.engine_base_id}>"


class EngineBase2(Base):
    """EngineBase entity representing base engine specifications.

    Attributes:
        id: Primary key.
        engine_base_id: VCdb specific ID.
        engine_block_id: Reference to engine block.
        engine_bore_stroke_id: Reference to engine bore stroke.
        engine_block: Relationship to engine block.
        engine_bore_stroke: Relationship to engine bore stroke.
        engine_configs: Relationship to engine configs.
    """

    __tablename__ = "engine_base2"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    engine_base_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    engine_block_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.engine_block.engine_block_id"), nullable=False
    )
    engine_bore_stroke_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.engine_bore_stroke.engine_bore_stroke_id"),
        nullable=False,
    )

    # Relationships
    engine_block: Mapped["EngineBlock"] = relationship(
        "EngineBlock", back_populates="engine_bases"
    )
    engine_bore_stroke: Mapped["EngineBoreStroke"] = relationship(
        "EngineBoreStroke", back_populates="engine_bases"
    )
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="engine_base"
    )

    def __repr__(self) -> str:
        """Return string representation of EngineBase2 instance.

        Returns:
            String representation.
        """
        return f"<EngineBase2 {self.engine_base_id}>"


class Aspiration(Base):
    """Aspiration entity representing engine aspiration types.

    Attributes:
        id: Primary key.
        aspiration_id: VCdb specific ID.
        name: Aspiration type name.
        engine_configs: Relationship to engine configs.
    """

    __tablename__ = "aspiration"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    aspiration_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="aspiration"
    )

    def __repr__(self) -> str:
        """Return string representation of Aspiration instance.

        Returns:
            String representation.
        """
        return f"<Aspiration {self.name} ({self.aspiration_id})>"


class FuelType(Base):
    """FuelType entity representing fuel types.

    Attributes:
        id: Primary key.
        fuel_type_id: VCdb specific ID.
        name: Fuel type name.
        engine_configs: Relationship to engine configs.
    """

    __tablename__ = "fuel_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fuel_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="fuel_type"
    )

    def __repr__(self) -> str:
        """Return string representation of FuelType instance.

        Returns:
            String representation.
        """
        return f"<FuelType {self.name} ({self.fuel_type_id})>"


class CylinderHeadType(Base):
    """CylinderHeadType entity representing cylinder head types.

    Attributes:
        id: Primary key.
        cylinder_head_type_id: VCdb specific ID.
        name: Cylinder head type name.
        engine_configs: Relationship to engine configs.
    """

    __tablename__ = "cylinder_head_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    cylinder_head_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="cylinder_head_type"
    )

    def __repr__(self) -> str:
        """Return string representation of CylinderHeadType instance.

        Returns:
            String representation.
        """
        return f"<CylinderHeadType {self.name} ({self.cylinder_head_type_id})>"


class EngineDesignation(Base):
    """EngineDesignation entity representing engine designation codes.

    Attributes:
        id: Primary key.
        engine_designation_id: VCdb specific ID.
        name: Engine designation name.
        engine_configs: Relationship to engine configs.
    """

    __tablename__ = "engine_designation"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    engine_designation_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="engine_designation"
    )

    def __repr__(self) -> str:
        """Return string representation of EngineDesignation instance.

        Returns:
            String representation.
        """
        return f"<EngineDesignation {self.name} ({self.engine_designation_id})>"


class EngineVIN(Base):
    """EngineVIN entity representing engine VIN codes.

    Attributes:
        id: Primary key.
        engine_vin_id: VCdb specific ID.
        code: Engine VIN code.
        engine_configs: Relationship to engine configs.
    """

    __tablename__ = "engine_vin"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    engine_vin_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    code: Mapped[str] = mapped_column(String(5), nullable=False, index=True)

    # Relationships
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="engine_vin"
    )

    def __repr__(self) -> str:
        """Return string representation of EngineVIN instance.

        Returns:
            String representation.
        """
        return f"<EngineVIN {self.code} ({self.engine_vin_id})>"


class EngineVersion(Base):
    """EngineVersion entity representing engine versions.

    Attributes:
        id: Primary key.
        engine_version_id: VCdb specific ID.
        version: Engine version value.
        engine_configs: Relationship to engine configs.
    """

    __tablename__ = "engine_version"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    engine_version_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    version: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # Relationships
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="engine_version"
    )

    def __repr__(self) -> str:
        """Return string representation of EngineVersion instance.

        Returns:
            String representation.
        """
        return f"<EngineVersion {self.version} ({self.engine_version_id})>"


class Mfr(Base):
    """Mfr entity representing manufacturers.

    Attributes:
        id: Primary key.
        mfr_id: VCdb specific ID.
        name: Manufacturer name.
        engine_configs: Relationship to engine configs (as engine manufacturer).
        transmission_configs: Relationship to transmission configs (as transmission manufacturer).
    """

    __tablename__ = "mfr"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    mfr_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="engine_mfr"
    )
    transmission_configs: Mapped[List["Transmission"]] = relationship(
        "Transmission", back_populates="transmission_mfr"
    )

    def __repr__(self) -> str:
        """Return string representation of Mfr instance.

        Returns:
            String representation.
        """
        return f"<Mfr {self.name} ({self.mfr_id})>"


class IgnitionSystemType(Base):
    """IgnitionSystemType entity representing ignition system types.

    Attributes:
        id: Primary key.
        ignition_system_type_id: VCdb specific ID.
        name: Ignition system type name.
        engine_configs: Relationship to engine configs.
    """

    __tablename__ = "ignition_system_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    ignition_system_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="ignition_system_type"
    )

    def __repr__(self) -> str:
        """Return string representation of IgnitionSystemType instance.

        Returns:
            String representation.
        """
        return f"<IgnitionSystemType {self.name} ({self.ignition_system_type_id})>"


class Valves(Base):
    """Valves entity representing number of engine valves.

    Attributes:
        id: Primary key.
        valves_id: VCdb specific ID.
        valves_per_engine: Number of valves per engine.
        engine_configs: Relationship to engine configs.
    """

    __tablename__ = "valves"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    valves_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    valves_per_engine: Mapped[str] = mapped_column(String(3), nullable=False)

    # Relationships
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="valves"
    )

    def __repr__(self) -> str:
        """Return string representation of Valves instance.

        Returns:
            String representation.
        """
        return f"<Valves {self.valves_per_engine} ({self.valves_id})>"


class FuelDeliveryType(Base):
    """FuelDeliveryType entity representing fuel delivery types.

    Attributes:
        id: Primary key.
        fuel_delivery_type_id: VCdb specific ID.
        name: Fuel delivery type name.
        fuel_delivery_configs: Relationship to fuel delivery configs.
    """

    __tablename__ = "fuel_delivery_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fuel_delivery_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Relationships
    fuel_delivery_configs: Mapped[List["FuelDeliveryConfig"]] = relationship(
        "FuelDeliveryConfig", back_populates="fuel_delivery_type"
    )

    def __repr__(self) -> str:
        """Return string representation of FuelDeliveryType instance.

        Returns:
            String representation.
        """
        return f"<FuelDeliveryType {self.name} ({self.fuel_delivery_type_id})>"


class FuelDeliverySubType(Base):
    """FuelDeliverySubType entity representing fuel delivery subtypes.

    Attributes:
        id: Primary key.
        fuel_delivery_subtype_id: VCdb specific ID.
        name: Fuel delivery subtype name.
        fuel_delivery_configs: Relationship to fuel delivery configs.
    """

    __tablename__ = "fuel_delivery_subtype"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fuel_delivery_subtype_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Relationships
    fuel_delivery_configs: Mapped[List["FuelDeliveryConfig"]] = relationship(
        "FuelDeliveryConfig", back_populates="fuel_delivery_subtype"
    )

    def __repr__(self) -> str:
        """Return string representation of FuelDeliverySubType instance.

        Returns:
            String representation.
        """
        return f"<FuelDeliverySubType {self.name} ({self.fuel_delivery_subtype_id})>"


class FuelSystemControlType(Base):
    """FuelSystemControlType entity representing fuel system control types.

    Attributes:
        id: Primary key.
        fuel_system_control_type_id: VCdb specific ID.
        name: Fuel system control type name.
        fuel_delivery_configs: Relationship to fuel delivery configs.
    """

    __tablename__ = "fuel_system_control_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fuel_system_control_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Relationships
    fuel_delivery_configs: Mapped[List["FuelDeliveryConfig"]] = relationship(
        "FuelDeliveryConfig", back_populates="fuel_system_control_type"
    )

    def __repr__(self) -> str:
        """Return string representation of FuelSystemControlType instance.

        Returns:
            String representation.
        """
        return (
            f"<FuelSystemControlType {self.name} ({self.fuel_system_control_type_id})>"
        )


class FuelSystemDesign(Base):
    """FuelSystemDesign entity representing fuel system design types.

    Attributes:
        id: Primary key.
        fuel_system_design_id: VCdb specific ID.
        name: Fuel system design name.
        fuel_delivery_configs: Relationship to fuel delivery configs.
    """

    __tablename__ = "fuel_system_design"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fuel_system_design_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Relationships
    fuel_delivery_configs: Mapped[List["FuelDeliveryConfig"]] = relationship(
        "FuelDeliveryConfig", back_populates="fuel_system_design"
    )

    def __repr__(self) -> str:
        """Return string representation of FuelSystemDesign instance.

        Returns:
            String representation.
        """
        return f"<FuelSystemDesign {self.name} ({self.fuel_system_design_id})>"


class FuelDeliveryConfig(Base):
    """FuelDeliveryConfig entity representing fuel delivery configurations.

    Attributes:
        id: Primary key.
        fuel_delivery_config_id: VCdb specific ID.
        fuel_delivery_type_id: Reference to fuel delivery type.
        fuel_delivery_subtype_id: Reference to fuel delivery subtype.
        fuel_system_control_type_id: Reference to fuel system control type.
        fuel_system_design_id: Reference to fuel system design.
        fuel_delivery_type: Relationship to fuel delivery type.
        fuel_delivery_subtype: Relationship to fuel delivery subtype.
        fuel_system_control_type: Relationship to fuel system control type.
        fuel_system_design: Relationship to fuel system design.
        engine_configs: Relationship to engine configs.
    """

    __tablename__ = "fuel_delivery_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    fuel_delivery_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    fuel_delivery_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.fuel_delivery_type.fuel_delivery_type_id"),
        nullable=False,
    )
    fuel_delivery_subtype_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.fuel_delivery_subtype.fuel_delivery_subtype_id"),
        nullable=False,
    )
    fuel_system_control_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.fuel_system_control_type.fuel_system_control_type_id"),
        nullable=False,
    )
    fuel_system_design_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.fuel_system_design.fuel_system_design_id"),
        nullable=False,
    )

    # Relationships
    fuel_delivery_type: Mapped["FuelDeliveryType"] = relationship(
        "FuelDeliveryType", back_populates="fuel_delivery_configs"
    )
    fuel_delivery_subtype: Mapped["FuelDeliverySubType"] = relationship(
        "FuelDeliverySubType", back_populates="fuel_delivery_configs"
    )
    fuel_system_control_type: Mapped["FuelSystemControlType"] = relationship(
        "FuelSystemControlType", back_populates="fuel_delivery_configs"
    )
    fuel_system_design: Mapped["FuelSystemDesign"] = relationship(
        "FuelSystemDesign", back_populates="fuel_delivery_configs"
    )
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="fuel_delivery_config"
    )

    def __repr__(self) -> str:
        """Return string representation of FuelDeliveryConfig instance.

        Returns:
            String representation.
        """
        return f"<FuelDeliveryConfig {self.fuel_delivery_config_id}>"


class PowerOutput(Base):
    """PowerOutput entity representing engine power output measurements.

    Attributes:
        id: Primary key.
        power_output_id: VCdb specific ID.
        horsepower: Horsepower value.
        kilowatt: Kilowatt value.
        engine_configs: Relationship to engine configs.
    """

    __tablename__ = "power_output"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    power_output_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    horsepower: Mapped[str] = mapped_column(String(10), nullable=False)
    kilowatt: Mapped[str] = mapped_column(String(10), nullable=False)

    # Relationships
    engine_configs: Mapped[List["EngineConfig2"]] = relationship(
        "EngineConfig2", back_populates="power_output"
    )

    def __repr__(self) -> str:
        """Return string representation of PowerOutput instance.

        Returns:
            String representation.
        """
        return f"<PowerOutput {self.horsepower}hp/{self.kilowatt}kw ({self.power_output_id})>"


class EngineConfig(Base):
    """Legacy EngineConfig entity.

    This class is maintained for backward compatibility but has been replaced by EngineConfig2.
    New code should use EngineConfig2 instead.

    Attributes:
        id: Primary key.
        engine_config_id: VCdb specific ID.
        engine_base_id: Reference to engine base.
        engine_designation_id: Reference to engine designation.
        engine_vin_id: Reference to engine VIN.
        valves_id: Reference to valves.
        fuel_delivery_config_id: Reference to fuel delivery config.
        aspiration_id: Reference to aspiration.
        cylinder_head_type_id: Reference to cylinder head type.
        fuel_type_id: Reference to fuel type.
        ignition_system_type_id: Reference to ignition system type.
        engine_mfr_id: Reference to engine manufacturer.
        engine_version_id: Reference to engine version.
        power_output_id: Reference to power output.
    """

    __tablename__ = "engine_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    engine_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    engine_base_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.engine_base.engine_base_id"), nullable=False
    )
    engine_designation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.engine_designation.engine_designation_id"),
        nullable=False,
    )
    engine_vin_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.engine_vin.engine_vin_id"), nullable=False
    )
    valves_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.valves.valves_id"), nullable=False
    )
    fuel_delivery_config_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.fuel_delivery_config.fuel_delivery_config_id"),
        nullable=False,
    )
    aspiration_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.aspiration.aspiration_id"), nullable=False
    )
    cylinder_head_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.cylinder_head_type.cylinder_head_type_id"),
        nullable=False,
    )
    fuel_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.fuel_type.fuel_type_id"), nullable=False
    )
    ignition_system_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.ignition_system_type.ignition_system_type_id"),
        nullable=False,
    )
    engine_mfr_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.mfr.mfr_id"), nullable=False
    )
    engine_version_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.engine_version.engine_version_id"), nullable=False
    )
    power_output_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.power_output.power_output_id"), nullable=False
    )

    def __repr__(self) -> str:
        """Return string representation of EngineConfig instance.

        Returns:
            String representation.
        """
        return f"<EngineConfig {self.engine_config_id}>"


class EngineConfig2(Base):
    """EngineConfig entity representing complete engine configurations.

    Attributes:
        id: Primary key.
        engine_config_id: VCdb specific ID.
        engine_base_id: Reference to engine base.
        engine_block_id: Reference to engine block.
        engine_bore_stroke_id: Reference to engine bore stroke.
        engine_designation_id: Reference to engine designation.
        engine_vin_id: Reference to engine VIN.
        valves_id: Reference to valves.
        fuel_delivery_config_id: Reference to fuel delivery config.
        aspiration_id: Reference to aspiration.
        cylinder_head_type_id: Reference to cylinder head type.
        fuel_type_id: Reference to fuel type.
        ignition_system_type_id: Reference to ignition system type.
        engine_mfr_id: Reference to engine manufacturer.
        engine_version_id: Reference to engine version.
        power_output_id: Reference to power output.
        engine_base: Relationship to engine base.
        engine_block: Relationship to engine block.
        engine_bore_stroke: Relationship to engine bore stroke.
        engine_designation: Relationship to engine designation.
        engine_vin: Relationship to engine VIN.
        valves: Relationship to valves.
        fuel_delivery_config: Relationship to fuel delivery config.
        aspiration: Relationship to aspiration.
        cylinder_head_type: Relationship to cylinder head type.
        fuel_type: Relationship to fuel type.
        ignition_system_type: Relationship to ignition system type.
        engine_mfr: Relationship to engine manufacturer.
        engine_version: Relationship to engine version.
        power_output: Relationship to power output.
    """

    __tablename__ = "engine_config2"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    engine_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    engine_base_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.engine_base2.engine_base_id"), nullable=False
    )
    engine_block_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.engine_block.engine_block_id"), nullable=False
    )
    engine_bore_stroke_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.engine_bore_stroke.engine_bore_stroke_id")
    )
    engine_designation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.engine_designation.engine_designation_id"),
        nullable=False,
    )
    engine_vin_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.engine_vin.engine_vin_id"), nullable=False
    )
    valves_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.valves.valves_id"), nullable=False
    )
    fuel_delivery_config_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.fuel_delivery_config.fuel_delivery_config_id"),
        nullable=False,
    )
    aspiration_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.aspiration.aspiration_id"), nullable=False
    )
    cylinder_head_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.cylinder_head_type.cylinder_head_type_id"),
        nullable=False,
    )
    fuel_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.fuel_type.fuel_type_id"), nullable=False
    )
    ignition_system_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.ignition_system_type.ignition_system_type_id"),
        nullable=False,
    )
    engine_mfr_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.mfr.mfr_id"), nullable=False
    )
    engine_version_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.engine_version.engine_version_id"), nullable=False
    )
    power_output_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.power_output.power_output_id"), nullable=False
    )

    # Relationships
    engine_base: Mapped["EngineBase2"] = relationship(
        "EngineBase2", back_populates="engine_configs"
    )
    engine_block: Mapped["EngineBlock"] = relationship(
        "EngineBlock", back_populates="engine_configs"
    )
    engine_bore_stroke: Mapped["EngineBoreStroke"] = relationship(
        "EngineBoreStroke", back_populates="engine_configs"
    )
    engine_designation: Mapped["EngineDesignation"] = relationship(
        "EngineDesignation", back_populates="engine_configs"
    )
    engine_vin: Mapped["EngineVIN"] = relationship(
        "EngineVIN", back_populates="engine_configs"
    )
    valves: Mapped["Valves"] = relationship("Valves", back_populates="engine_configs")
    fuel_delivery_config: Mapped["FuelDeliveryConfig"] = relationship(
        "FuelDeliveryConfig", back_populates="engine_configs"
    )
    aspiration: Mapped["Aspiration"] = relationship(
        "Aspiration", back_populates="engine_configs"
    )
    cylinder_head_type: Mapped["CylinderHeadType"] = relationship(
        "CylinderHeadType", back_populates="engine_configs"
    )
    fuel_type: Mapped["FuelType"] = relationship(
        "FuelType", back_populates="engine_configs"
    )
    ignition_system_type: Mapped["IgnitionSystemType"] = relationship(
        "IgnitionSystemType", back_populates="engine_configs"
    )
    engine_mfr: Mapped["Mfr"] = relationship("Mfr", back_populates="engine_configs")
    engine_version: Mapped["EngineVersion"] = relationship(
        "EngineVersion", back_populates="engine_configs"
    )
    power_output: Mapped["PowerOutput"] = relationship(
        "PowerOutput", back_populates="engine_configs"
    )

    def __repr__(self) -> str:
        """Return string representation of EngineConfig2 instance.

        Returns:
            String representation.
        """
        return f"<EngineConfig2 {self.engine_config_id}>"


# Vehicle to EngineConfig association table
class VehicleToEngineConfig(Base):
    """
    Represents the mapping between vehicles and their associated engine configurations.

    Attributes:
        id (UUID): Primary key, a unique identifier for each mapping record, generated automatically.
        vehicle_to_engine_config_id (int): A unique identifier for the relationship,
            indexed and must not be null.
        vehicle_id (int): Foreign key linking to the 'vehicle' table in the 'vcdb' schema, must not be null.
        engine_config_id (int): Foreign key linking to the 'engine_config2' table
            in the 'vcdb' schema, must not be null.
        source (str): An optional string (up to 10 characters) to denote the source of the mapping.
    """

    __tablename__ = "vehicle_to_engine_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vehicle_to_engine_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.vehicle.vehicle_id"), nullable=False
    )
    engine_config_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.engine_config2.engine_config_id"), nullable=False
    )
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<VehicleToEngineConfig("
            f"id={self.id}, vehicle_to_engine_config_id={self.vehicle_to_engine_config_id}, "
            f"vehicle_id={self.vehicle_id}, engine_config_id={self.engine_config_id}, "
            f"source={self.source})>"
        )


class SpringType(Base):
    """SpringType entity representing spring types.

    Attributes:
        id: Primary key.
        spring_type_id: VCdb specific ID.
        name: Spring type name.
        front_spring_configs: Relationship to spring configs (as front).
        rear_spring_configs: Relationship to spring configs (as rear).
    """

    __tablename__ = "spring_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    spring_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Relationships
    front_spring_configs: Mapped[List["SpringTypeConfig"]] = relationship(
        "SpringTypeConfig",
        primaryjoin="SpringType.spring_type_id == SpringTypeConfig.front_spring_type_id",
        back_populates="front_spring_type",
    )
    rear_spring_configs: Mapped[List["SpringTypeConfig"]] = relationship(
        "SpringTypeConfig",
        primaryjoin="SpringType.spring_type_id == SpringTypeConfig.rear_spring_type_id",
        back_populates="rear_spring_type",
    )

    def __repr__(self) -> str:
        """Return string representation of SpringType instance.

        Returns:
            String representation.
        """
        return f"<SpringType {self.name} ({self.spring_type_id})>"


class SpringTypeConfig(Base):
    """SpringTypeConfig entity representing spring type configurations.

    Attributes:
        id: Primary key.
        spring_type_config_id: VCdb specific ID.
        front_spring_type_id: Reference to front spring type.
        rear_spring_type_id: Reference to rear spring type.
        front_spring_type: Relationship to front spring type.
        rear_spring_type: Relationship to rear spring type.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "spring_type_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    spring_type_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    front_spring_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.spring_type.spring_type_id"), nullable=False
    )
    rear_spring_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.spring_type.spring_type_id"), nullable=False
    )

    # Relationships
    front_spring_type: Mapped["SpringType"] = relationship(
        "SpringType",
        primaryjoin="SpringTypeConfig.front_spring_type_id == SpringType.spring_type_id",
        back_populates="front_spring_configs",
    )
    rear_spring_type: Mapped["SpringType"] = relationship(
        "SpringType",
        primaryjoin="SpringTypeConfig.rear_spring_type_id == SpringType.spring_type_id",
        back_populates="rear_spring_configs",
    )

    def __repr__(self) -> str:
        """Return string representation of SpringTypeConfig instance.

        Returns:
            String representation.
        """
        return f"<SpringTypeConfig {self.spring_type_config_id}>"


# Vehicle to SpringTypeConfig association table
class VehicleToSpringTypeConfig(Base):
    """
    Represents the mapping between vehicles and their associated spring type configurations.

    Attributes:
        id (UUID): Primary key, a unique identifier for each mapping record, generated automatically.
        vehicle_to_spring_type_config_id (int): A unique identifier for the relationship,
            indexed and must not be null.
        vehicle_id (int): Foreign key linking to the 'vehicle' table in the 'vcdb' schema, must not be null.
        spring_type_config_id (int): Foreign key linking to the 'spring_type_config' table
            in the 'vcdb' schema, must not be null.
        source (str): An optional string (up to 10 characters) to denote the source of the mapping.
    """

    __tablename__ = "vehicle_to_spring_type_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vehicle_to_spring_type_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.vehicle.vehicle_id"), nullable=False
    )
    spring_type_config_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.spring_type_config.spring_type_config_id"),
        nullable=False,
    )
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<VehicleToSpringTypeConfig("
            f"id={self.id}, vehicle_to_spring_type_config_id={self.vehicle_to_spring_type_config_id}, "
            f"vehicle_id={self.vehicle_id}, spring_type_config_id={self.spring_type_config_id}, "
            f"source={self.source})>"
        )


class SteeringType(Base):
    """SteeringType entity representing steering types.

    Attributes:
        id: Primary key.
        steering_type_id: VCdb specific ID.
        name: Steering type name.
        steering_configs: Relationship to steering configs.
    """

    __tablename__ = "steering_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    steering_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    steering_configs: Mapped[List["SteeringConfig"]] = relationship(
        "SteeringConfig", back_populates="steering_type"
    )

    def __repr__(self) -> str:
        """Return string representation of SteeringType instance.

        Returns:
            String representation.
        """
        return f"<SteeringType {self.name} ({self.steering_type_id})>"


class SteeringSystem(Base):
    """SteeringSystem entity representing steering systems.

    Attributes:
        id: Primary key.
        steering_system_id: VCdb specific ID.
        name: Steering system name.
        steering_configs: Relationship to steering configs.
    """

    __tablename__ = "steering_system"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    steering_system_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    steering_configs: Mapped[List["SteeringConfig"]] = relationship(
        "SteeringConfig", back_populates="steering_system"
    )

    def __repr__(self) -> str:
        """Return string representation of SteeringSystem instance.

        Returns:
            String representation.
        """
        return f"<SteeringSystem {self.name} ({self.steering_system_id})>"


class SteeringConfig(Base):
    """SteeringConfig entity representing steering configurations.

    Attributes:
        id: Primary key.
        steering_config_id: VCdb specific ID.
        steering_type_id: Reference to steering type.
        steering_system_id: Reference to steering system.
        steering_type: Relationship to steering type.
        steering_system: Relationship to steering system.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "steering_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    steering_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    steering_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.steering_type.steering_type_id"), nullable=False
    )
    steering_system_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.steering_system.steering_system_id"),
        nullable=False,
    )

    # Relationships
    steering_type: Mapped["SteeringType"] = relationship(
        "SteeringType", back_populates="steering_configs"
    )
    steering_system: Mapped["SteeringSystem"] = relationship(
        "SteeringSystem", back_populates="steering_configs"
    )

    def __repr__(self) -> str:
        """Return string representation of SteeringConfig instance.

        Returns:
            String representation.
        """
        return f"<SteeringConfig {self.steering_config_id}>"


# Vehicle to SteeringConfig association table
class VehicleToSteeringConfig(Base):
    """
    Represents the mapping between vehicles and their associated steering configurations.

    Attributes:
        id (UUID): Primary key, a unique identifier for each mapping record, generated automatically.
        vehicle_to_steering_config_id (int): A unique identifier for the relationship,
            indexed and must not be null.
        vehicle_id (int): Foreign key linking to the 'vehicle' table in the 'vcdb' schema, must not be null.
        steering_config_id (int): Foreign key linking to the 'steering_config' table
            in the 'vcdb' schema, must not be null.
        source (str): An optional string (up to 10 characters) to denote the source of the mapping.
    """

    __tablename__ = "vehicle_to_steering_config"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vehicle_to_steering_config_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.vehicle.vehicle_id"), nullable=False
    )
    steering_config_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.steering_config.steering_config_id"), nullable=False
    )
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<VehicleToSteeringConfig("
            f"id={self.id}, vehicle_to_steering_config_id={self.vehicle_to_steering_config_id}, "
            f"vehicle_id={self.vehicle_id}, steering_config_id={self.steering_config_id}, "
            f"source={self.source})>"
        )


class TransmissionType(Base):
    """TransmissionType entity representing transmission types.

    Attributes:
        id: Primary key.
        transmission_type_id: VCdb specific ID.
        name: Transmission type name.
        transmission_bases: Relationship to transmission bases.
    """

    __tablename__ = "transmission_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transmission_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    transmission_bases: Mapped[List["TransmissionBase"]] = relationship(
        "TransmissionBase", back_populates="transmission_type"
    )

    def __repr__(self) -> str:
        """Return string representation of TransmissionType instance.

        Returns:
            String representation.
        """
        return f"<TransmissionType {self.name} ({self.transmission_type_id})>"


class TransmissionNumSpeeds(Base):
    """TransmissionNumSpeeds entity representing number of transmission speeds.

    Attributes:
        id: Primary key.
        transmission_num_speeds_id: VCdb specific ID.
        num_speeds: Number of speeds value.
        transmission_bases: Relationship to transmission bases.
    """

    __tablename__ = "transmission_num_speeds"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transmission_num_speeds_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    num_speeds: Mapped[str] = mapped_column(String(3), nullable=False, index=True)

    # Relationships
    transmission_bases: Mapped[List["TransmissionBase"]] = relationship(
        "TransmissionBase", back_populates="transmission_num_speeds"
    )

    def __repr__(self) -> str:
        """Return string representation of TransmissionNumSpeeds instance.

        Returns:
            String representation.
        """
        return f"<TransmissionNumSpeeds {self.num_speeds} ({self.transmission_num_speeds_id})>"


class TransmissionControlType(Base):
    """TransmissionControlType entity representing transmission control types.

    Attributes:
        id: Primary key.
        transmission_control_type_id: VCdb specific ID.
        name: Transmission control type name.
        transmission_bases: Relationship to transmission bases.
    """

    __tablename__ = "transmission_control_type"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transmission_control_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    transmission_bases: Mapped[List["TransmissionBase"]] = relationship(
        "TransmissionBase", back_populates="transmission_control_type"
    )

    def __repr__(self) -> str:
        """Return string representation of TransmissionControlType instance.

        Returns:
            String representation.
        """
        return f"<TransmissionControlType {self.name} ({self.transmission_control_type_id})>"


class TransmissionBase(Base):
    """TransmissionBase entity representing base transmission specifications.

    Attributes:
        id: Primary key.
        transmission_base_id: VCdb specific ID.
        transmission_type_id: Reference to transmission type.
        transmission_num_speeds_id: Reference to transmission number of speeds.
        transmission_control_type_id: Reference to transmission control type.
        transmission_type: Relationship to transmission type.
        transmission_num_speeds: Relationship to transmission number of speeds.
        transmission_control_type: Relationship to transmission control type.
        transmissions: Relationship to transmissions.
    """

    __tablename__ = "transmission_base"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transmission_base_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    transmission_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.transmission_type.transmission_type_id"),
        nullable=False,
    )
    transmission_num_speeds_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.transmission_num_speeds.transmission_num_speeds_id"),
        nullable=False,
    )
    transmission_control_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.transmission_control_type.transmission_control_type_id"),
        nullable=False,
    )

    # Relationships
    transmission_type: Mapped["TransmissionType"] = relationship(
        "TransmissionType", back_populates="transmission_bases"
    )
    transmission_num_speeds: Mapped["TransmissionNumSpeeds"] = relationship(
        "TransmissionNumSpeeds", back_populates="transmission_bases"
    )
    transmission_control_type: Mapped["TransmissionControlType"] = relationship(
        "TransmissionControlType", back_populates="transmission_bases"
    )
    transmissions: Mapped[List["Transmission"]] = relationship(
        "Transmission", back_populates="transmission_base"
    )

    def __repr__(self) -> str:
        """Return string representation of TransmissionBase instance.

        Returns:
            String representation.
        """
        return f"<TransmissionBase {self.transmission_base_id}>"


class TransmissionMfrCode(Base):
    """TransmissionMfrCode entity representing transmission manufacturer codes.

    Attributes:
        id: Primary key.
        transmission_mfr_code_id: VCdb specific ID.
        code: Manufacturer code value.
        transmissions: Relationship to transmissions.
    """

    __tablename__ = "transmission_mfr_code"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transmission_mfr_code_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    code: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # Relationships
    transmissions: Mapped[List["Transmission"]] = relationship(
        "Transmission", back_populates="transmission_mfr_code"
    )

    def __repr__(self) -> str:
        """Return string representation of TransmissionMfrCode instance.

        Returns:
            String representation.
        """
        return f"<TransmissionMfrCode {self.code} ({self.transmission_mfr_code_id})>"


class ElecControlled(Base):
    """ElecControlled entity representing electronic controlled status.

    Attributes:
        id: Primary key.
        elec_controlled_id: VCdb specific ID.
        value: Electronic controlled value.
        transmissions: Relationship to transmissions.
    """

    __tablename__ = "elec_controlled"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    elec_controlled_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    value: Mapped[str] = mapped_column(String(3), nullable=False, index=True)

    # Relationships
    transmissions: Mapped[List["Transmission"]] = relationship(
        "Transmission", back_populates="elec_controlled"
    )

    def __repr__(self) -> str:
        """Return string representation of ElecControlled instance.

        Returns:
            String representation.
        """
        return f"<ElecControlled {self.value} ({self.elec_controlled_id})>"


class Transmission(Base):
    """Transmission entity representing complete transmission configurations.

    Attributes:
        id: Primary key.
        transmission_id: VCdb specific ID.
        transmission_base_id: Reference to transmission base.
        transmission_mfr_code_id: Reference to transmission manufacturer code.
        elec_controlled_id: Reference to electronic controlled status.
        transmission_mfr_id: Reference to transmission manufacturer.
        transmission_base: Relationship to transmission base.
        transmission_mfr_code: Relationship to transmission manufacturer code.
        elec_controlled: Relationship to electronic controlled status.
        transmission_mfr: Relationship to transmission manufacturer.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "transmission"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transmission_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    transmission_base_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.transmission_base.transmission_base_id"),
        nullable=False,
    )
    transmission_mfr_code_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.transmission_mfr_code.transmission_mfr_code_id"),
        nullable=False,
    )
    elec_controlled_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vcdb.elec_controlled.elec_controlled_id"),
        nullable=False,
    )
    transmission_mfr_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.mfr.mfr_id"), nullable=False
    )

    # Relationships
    transmission_base: Mapped["TransmissionBase"] = relationship(
        "TransmissionBase", back_populates="transmissions"
    )
    transmission_mfr_code: Mapped["TransmissionMfrCode"] = relationship(
        "TransmissionMfrCode", back_populates="transmissions"
    )
    elec_controlled: Mapped["ElecControlled"] = relationship(
        "ElecControlled", back_populates="transmissions"
    )
    transmission_mfr: Mapped["Mfr"] = relationship(
        "Mfr", back_populates="transmission_configs"
    )

    def __repr__(self) -> str:
        """Return string representation of Transmission instance.

        Returns:
            String representation.
        """
        return f"<Transmission {self.transmission_id}>"


# Vehicle to Transmission association table
class VehicleToTransmission(Base):
    """
    Represents the mapping between vehicles and their associated transmissions.

    Attributes:
        id (UUID): Primary key, a unique identifier for each mapping record, generated automatically.
        vehicle_to_transmission_id (int): A unique identifier for the relationship,
            indexed and must not be null.
        vehicle_id (int): Foreign key linking to the 'vehicle' table in the 'vcdb' schema, must not be null.
        transmission_id (int): Foreign key linking to the 'transmission' table
            in the 'vcdb' schema, must not be null.
        source (str): An optional string (up to 10 characters) to denote the source of the mapping.
    """

    __tablename__ = "vehicle_to_transmission"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vehicle_to_transmission_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.vehicle.vehicle_id"), nullable=False
    )
    transmission_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.transmission.transmission_id"), nullable=False
    )
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<VehicleToTransmission("
            f"id={self.id}, vehicle_to_transmission_id={self.vehicle_to_transmission_id}, "
            f"vehicle_id={self.vehicle_id}, transmission_id={self.transmission_id}, "
            f"source={self.source}>"
        )


class WheelBase(Base):
    """WheelBase entity representing wheelbase measurements.

    Attributes:
        id: Primary key.
        wheel_base_id: VCdb specific ID.
        wheel_base: Wheelbase measurement in imperial units.
        wheel_base_metric: Wheelbase measurement in metric units.
        vehicles: Relationship to vehicles.
    """

    __tablename__ = "wheel_base"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    wheel_base_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    wheel_base: Mapped[str] = mapped_column(String(10), nullable=False)
    wheel_base_metric: Mapped[str] = mapped_column(String(10), nullable=False)

    def __repr__(self) -> str:
        """Return string representation of WheelBase instance.

        Returns:
            String representation.
        """
        return f"<WheelBase {self.wheel_base} ({self.wheel_base_id})>"


# Vehicle to WheelBase association table
class VehicleToWheelBase(Base):
    """
    Represents the mapping between vehicles and their associated wheel base configurations.

    Attributes:
        id (UUID): Primary key, a unique identifier for each mapping record, generated automatically.
        vehicle_to_wheel_base_id (int): A unique identifier for the relationship,
            indexed and must not be null.
        vehicle_id (int): Foreign key linking to the 'vehicle' table in the 'vcdb' schema, must not be null.
        wheel_base_id (int): Foreign key linking to the 'wheel_base' table
            in the 'vcdb' schema, must not be null.
        source (str): An optional string (up to 10 characters) to denote the source of the mapping.
    """

    __tablename__ = "vehicle_to_wheel_base"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vehicle_to_wheel_base_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.vehicle.vehicle_id"), nullable=False
    )
    wheel_base_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vcdb.wheel_base.wheel_base_id"), nullable=False
    )
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<VehicleToWheelBase("
            f"id={self.id}, vehicle_to_wheel_base_id={self.vehicle_to_wheel_base_id}, "
            f"vehicle_id={self.vehicle_id}, wheel_base_id={self.wheel_base_id}, "
            f"source={self.source}>"
        )


class VCdbVersion(Base):
    """VCdbVersion entity representing VCdb version information.

    Attributes:
        id: Primary key.
        version_date: Date of the version.
        is_current: Whether this is the current version.
    """

    __tablename__ = "vcdb_version"
    __table_args__ = {"schema": "vcdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    version_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        """Return string representation of VCdbVersion instance.

        Returns:
            String representation.
        """
        return f"<VCdbVersion {self.version_date.strftime('%Y-%m-%d')}>"
