from __future__ import annotations
'VCdb (Vehicle Component Database) models.\n\nThis module defines the SQLAlchemy models that correspond to the VCdb database schema.\nThese models represent vehicle information and their components according to\nAuto Care Association standards.\n'
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
class Make(Base):
    __tablename__ = 'autocare_make'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    make_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    vehicles = relationship('Vehicle', back_populates='make')
    base_vehicles = relationship('BaseVehicle', back_populates='make')
    def __repr__(self) -> str:
        return f'<Make {self.name} ({self.make_id})>'
class Year(Base):
    __tablename__ = 'autocare_year'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    year_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    base_vehicles = relationship('BaseVehicle', back_populates='year')
    def __repr__(self) -> str:
        return f'<Year {self.year} ({self.year_id})>'
class Model(Base):
    __tablename__ = 'autocare_model'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    vehicle_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_vehicle_type.vehicle_type_id'), nullable=False)
    base_vehicles = relationship('BaseVehicle', back_populates='model')
    vehicle_type = relationship('VehicleType', back_populates='models')
    def __repr__(self) -> str:
        return f'<Model {self.name} ({self.model_id})>'
class VehicleType(Base):
    __tablename__ = 'autocare_vehicle_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    vehicle_type_group_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('autocare_vehicle_type_group.vehicle_type_group_id'), nullable=True)
    models = relationship('Model', back_populates='vehicle_type')
    vehicle_type_group = relationship('VehicleTypeGroup', back_populates='vehicle_types')
    def __repr__(self) -> str:
        return f'<VehicleType {self.name} ({self.vehicle_type_id})>'
class VehicleTypeGroup(Base):
    __tablename__ = 'autocare_vehicle_type_group'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_type_group_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    vehicle_types = relationship('VehicleType', back_populates='vehicle_type_group')
    def __repr__(self) -> str:
        return f'<VehicleTypeGroup {self.name} ({self.vehicle_type_group_id})>'
class SubModel(Base):
    __tablename__ = 'autocare_submodel'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submodel_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    vehicles = relationship('Vehicle', back_populates='submodel')
    def __repr__(self) -> str:
        return f'<SubModel {self.name} ({self.submodel_id})>'
class Region(Base):
    __tablename__ = 'autocare_region'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    region_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('autocare_region.region_id'), nullable=True)
    abbr: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    children = relationship('Region', back_populates='parent', remote_side=[region_id])
    parent = relationship('Region', back_populates='children', remote_side=[id])
    vehicles = relationship('Vehicle', back_populates='region')
    def __repr__(self) -> str:
        return f'<Region {self.name} ({self.region_id})>'
class PublicationStage(Base):
    __tablename__ = 'autocare_publication_stage'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_stage_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    vehicles = relationship('Vehicle', back_populates='publication_stage')
    def __repr__(self) -> str:
        return f'<PublicationStage {self.name} ({self.publication_stage_id})>'
class BaseVehicle(Base):
    __tablename__ = 'autocare_base_vehicle'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    base_vehicle_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    year_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_year.year_id'), nullable=False)
    make_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_make.make_id'), nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_model.model_id'), nullable=False)
    year = relationship('Year', back_populates='base_vehicles')
    make = relationship('Make', back_populates='base_vehicles')
    model = relationship('Model', back_populates='base_vehicles')
    vehicles = relationship('Vehicle', back_populates='base_vehicle')
    def __repr__(self) -> str:
        return f'<BaseVehicle {self.base_vehicle_id}>'
class Vehicle(Base):
    __tablename__ = 'autocare_vehicle'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    base_vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_base_vehicle.base_vehicle_id'), nullable=False)
    submodel_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_submodel.submodel_id'), nullable=False)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_region.region_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    publication_stage_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_publication_stage.publication_stage_id'), nullable=False, default=4)
    publication_stage_source: Mapped[str] = mapped_column(String(100), nullable=False)
    publication_stage_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    base_vehicle = relationship('BaseVehicle', back_populates='vehicles')
    submodel = relationship('SubModel', back_populates='vehicles')
    region = relationship('Region', back_populates='vehicles')
    publication_stage = relationship('PublicationStage', back_populates='vehicles')
    drive_types = relationship('DriveType', secondary='autocare_vehicle_to_drive_type')
    brake_configs = relationship('BrakeConfig', secondary='autocare_vehicle_to_brake_config')
    bed_configs = relationship('BedConfig', secondary='autocare_vehicle_to_bed_config')
    body_style_configs = relationship('BodyStyleConfig', secondary='autocare_vehicle_to_body_style_config')
    mfr_body_codes = relationship('MfrBodyCode', secondary='autocare_vehicle_to_mfr_body_code')
    engine_configs = relationship('EngineConfig', secondary='autocare_vehicle_to_engine_config')
    spring_type_configs = relationship('SpringTypeConfig', secondary='autocare_vehicle_to_spring_type_config')
    steering_configs = relationship('SteeringConfig', secondary='autocare_vehicle_to_steering_config')
    transmissions = relationship('Transmission', secondary='autocare_vehicle_to_transmission')
    wheel_bases = relationship('WheelBase', secondary='autocare_vehicle_to_wheel_base')
    @property
    def make(self) -> Make:
        return self.base_vehicle.make
    @property
    def year(self) -> int:
        return self.base_vehicle.year.year
    @property
    def model(self) -> str:
        return self.base_vehicle.model.name
    def __repr__(self) -> str:
        return f'<Vehicle {self.vehicle_id}>'
class DriveType(Base):
    __tablename__ = 'autocare_drive_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    drive_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    def __repr__(self) -> str:
        return f'<DriveType {self.name} ({self.drive_type_id})>'
vehicle_to_drive_type = Table('autocare_vehicle_to_drive_type', Base.metadata, Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), Column('vehicle_id', Integer, ForeignKey('autocare_vehicle.vehicle_id'), nullable=False), Column('drive_type_id', Integer, ForeignKey('autocare_drive_type.drive_type_id'), nullable=False), Column('source', String(10), nullable=True))
class BrakeType(Base):
    __tablename__ = 'autocare_brake_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brake_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    front_brake_configs = relationship('BrakeConfig', foreign_keys='[BrakeConfig.front_brake_type_id]', back_populates='front_brake_type')
    rear_brake_configs = relationship('BrakeConfig', foreign_keys='[BrakeConfig.rear_brake_type_id]', back_populates='rear_brake_type')
    def __repr__(self) -> str:
        return f'<BrakeType {self.name} ({self.brake_type_id})>'
class BrakeSystem(Base):
    __tablename__ = 'autocare_brake_system'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brake_system_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    brake_configs = relationship('BrakeConfig', back_populates='brake_system')
    def __repr__(self) -> str:
        return f'<BrakeSystem {self.name} ({self.brake_system_id})>'
class BrakeABS(Base):
    __tablename__ = 'autocare_brake_abs'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brake_abs_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    brake_configs = relationship('BrakeConfig', back_populates='brake_abs')
    def __repr__(self) -> str:
        return f'<BrakeABS {self.name} ({self.brake_abs_id})>'
class BrakeConfig(Base):
    __tablename__ = 'autocare_brake_config'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brake_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    front_brake_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_brake_type.brake_type_id'), nullable=False)
    rear_brake_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_brake_type.brake_type_id'), nullable=False)
    brake_system_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_brake_system.brake_system_id'), nullable=False)
    brake_abs_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_brake_abs.brake_abs_id'), nullable=False)
    front_brake_type = relationship('BrakeType', foreign_keys=[front_brake_type_id], back_populates='front_brake_configs')
    rear_brake_type = relationship('BrakeType', foreign_keys=[rear_brake_type_id], back_populates='rear_brake_configs')
    brake_system = relationship('BrakeSystem', back_populates='brake_configs')
    brake_abs = relationship('BrakeABS', back_populates='brake_configs')
    def __repr__(self) -> str:
        return f'<BrakeConfig {self.brake_config_id}>'
vehicle_to_brake_config = Table('autocare_vehicle_to_brake_config', Base.metadata, Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), Column('vehicle_id', Integer, ForeignKey('autocare_vehicle.vehicle_id'), nullable=False), Column('brake_config_id', Integer, ForeignKey('autocare_brake_config.brake_config_id'), nullable=False), Column('source', String(10), nullable=True))
class BedType(Base):
    __tablename__ = 'autocare_bed_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bed_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    bed_configs = relationship('BedConfig', back_populates='bed_type')
    def __repr__(self) -> str:
        return f'<BedType {self.name} ({self.bed_type_id})>'
class BedLength(Base):
    __tablename__ = 'autocare_bed_length'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bed_length_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    length: Mapped[str] = mapped_column(String(10), nullable=False)
    length_metric: Mapped[str] = mapped_column(String(10), nullable=False)
    bed_configs = relationship('BedConfig', back_populates='bed_length')
    def __repr__(self) -> str:
        return f'<BedLength {self.length} ({self.bed_length_id})>'
class BedConfig(Base):
    __tablename__ = 'autocare_bed_config'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bed_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    bed_length_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_bed_length.bed_length_id'), nullable=False)
    bed_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_bed_type.bed_type_id'), nullable=False)
    bed_length = relationship('BedLength', back_populates='bed_configs')
    bed_type = relationship('BedType', back_populates='bed_configs')
    def __repr__(self) -> str:
        return f'<BedConfig {self.bed_config_id}>'
vehicle_to_bed_config = Table('autocare_vehicle_to_bed_config', Base.metadata, Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), Column('vehicle_id', Integer, ForeignKey('autocare_vehicle.vehicle_id'), nullable=False), Column('bed_config_id', Integer, ForeignKey('autocare_bed_config.bed_config_id'), nullable=False), Column('source', String(10), nullable=True))
class BodyType(Base):
    __tablename__ = 'autocare_body_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    body_style_configs = relationship('BodyStyleConfig', back_populates='body_type')
    def __repr__(self) -> str:
        return f'<BodyType {self.name} ({self.body_type_id})>'
class BodyNumDoors(Base):
    __tablename__ = 'autocare_body_num_doors'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body_num_doors_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    num_doors: Mapped[str] = mapped_column(String(3), nullable=False)
    body_style_configs = relationship('BodyStyleConfig', back_populates='body_num_doors')
    def __repr__(self) -> str:
        return f'<BodyNumDoors {self.num_doors} ({self.body_num_doors_id})>'
class BodyStyleConfig(Base):
    __tablename__ = 'autocare_body_style_config'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body_style_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    body_num_doors_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_body_num_doors.body_num_doors_id'), nullable=False)
    body_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_body_type.body_type_id'), nullable=False)
    body_num_doors = relationship('BodyNumDoors', back_populates='body_style_configs')
    body_type = relationship('BodyType', back_populates='body_style_configs')
    def __repr__(self) -> str:
        return f'<BodyStyleConfig {self.body_style_config_id}>'
vehicle_to_body_style_config = Table('autocare_vehicle_to_body_style_config', Base.metadata, Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), Column('vehicle_id', Integer, ForeignKey('autocare_vehicle.vehicle_id'), nullable=False), Column('body_style_config_id', Integer, ForeignKey('autocare_body_style_config.body_style_config_id'), nullable=False), Column('source', String(10), nullable=True))
class MfrBodyCode(Base):
    __tablename__ = 'autocare_mfr_body_code'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mfr_body_code_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    def __repr__(self) -> str:
        return f'<MfrBodyCode {self.code} ({self.mfr_body_code_id})>'
vehicle_to_mfr_body_code = Table('autocare_vehicle_to_mfr_body_code', Base.metadata, Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), Column('vehicle_id', Integer, ForeignKey('autocare_vehicle.vehicle_id'), nullable=False), Column('mfr_body_code_id', Integer, ForeignKey('autocare_mfr_body_code.mfr_body_code_id'), nullable=False), Column('source', String(10), nullable=True))
class EngineBlock(Base):
    __tablename__ = 'autocare_engine_block'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_block_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    liter: Mapped[str] = mapped_column(String(6), nullable=False)
    cc: Mapped[str] = mapped_column(String(8), nullable=False)
    cid: Mapped[str] = mapped_column(String(7), nullable=False)
    cylinders: Mapped[str] = mapped_column(String(2), nullable=False)
    block_type: Mapped[str] = mapped_column(String(2), nullable=False)
    engine_bases = relationship('EngineBase', back_populates='engine_block')
    def __repr__(self) -> str:
        return f'<EngineBlock {self.liter}L {self.cylinders}cyl ({self.engine_block_id})>'
class EngineBoreStroke(Base):
    __tablename__ = 'autocare_engine_bore_stroke'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_bore_stroke_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    bore_in: Mapped[str] = mapped_column(String(10), nullable=False)
    bore_metric: Mapped[str] = mapped_column(String(10), nullable=False)
    stroke_in: Mapped[str] = mapped_column(String(10), nullable=False)
    stroke_metric: Mapped[str] = mapped_column(String(10), nullable=False)
    engine_bases = relationship('EngineBase', back_populates='engine_bore_stroke')
    def __repr__(self) -> str:
        return f'<EngineBoreStroke {self.bore_in}x{self.stroke_in} ({self.engine_bore_stroke_id})>'
class EngineBase(Base):
    __tablename__ = 'autocare_engine_base'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_base_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    engine_block_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_engine_block.engine_block_id'), nullable=False)
    engine_bore_stroke_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_engine_bore_stroke.engine_bore_stroke_id'), nullable=False)
    engine_block = relationship('EngineBlock', back_populates='engine_bases')
    engine_bore_stroke = relationship('EngineBoreStroke', back_populates='engine_bases')
    engine_configs = relationship('EngineConfig', back_populates='engine_base')
    def __repr__(self) -> str:
        return f'<EngineBase {self.engine_base_id}>'
class Aspiration(Base):
    __tablename__ = 'autocare_aspiration'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aspiration_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs = relationship('EngineConfig', back_populates='aspiration')
    def __repr__(self) -> str:
        return f'<Aspiration {self.name} ({self.aspiration_id})>'
class FuelType(Base):
    __tablename__ = 'autocare_fuel_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs = relationship('EngineConfig', back_populates='fuel_type')
    def __repr__(self) -> str:
        return f'<FuelType {self.name} ({self.fuel_type_id})>'
class CylinderHeadType(Base):
    __tablename__ = 'autocare_cylinder_head_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cylinder_head_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs = relationship('EngineConfig', back_populates='cylinder_head_type')
    def __repr__(self) -> str:
        return f'<CylinderHeadType {self.name} ({self.cylinder_head_type_id})>'
class EngineDesignation(Base):
    __tablename__ = 'autocare_engine_designation'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_designation_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs = relationship('EngineConfig', back_populates='engine_designation')
    def __repr__(self) -> str:
        return f'<EngineDesignation {self.name} ({self.engine_designation_id})>'
class EngineVIN(Base):
    __tablename__ = 'autocare_engine_vin'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_vin_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    code: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    engine_configs = relationship('EngineConfig', back_populates='engine_vin')
    def __repr__(self) -> str:
        return f'<EngineVIN {self.code} ({self.engine_vin_id})>'
class EngineVersion(Base):
    __tablename__ = 'autocare_engine_version'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_version_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    version: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    engine_configs = relationship('EngineConfig', back_populates='engine_version')
    def __repr__(self) -> str:
        return f'<EngineVersion {self.version} ({self.engine_version_id})>'
class Mfr(Base):
    __tablename__ = 'autocare_mfr'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mfr_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs = relationship('EngineConfig', back_populates='engine_mfr')
    transmission_configs = relationship('Transmission', back_populates='transmission_mfr')
    def __repr__(self) -> str:
        return f'<Mfr {self.name} ({self.mfr_id})>'
class IgnitionSystemType(Base):
    __tablename__ = 'autocare_ignition_system_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ignition_system_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs = relationship('EngineConfig', back_populates='ignition_system_type')
    def __repr__(self) -> str:
        return f'<IgnitionSystemType {self.name} ({self.ignition_system_type_id})>'
class Valves(Base):
    __tablename__ = 'autocare_valves'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    valves_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    valves_per_engine: Mapped[str] = mapped_column(String(3), nullable=False)
    engine_configs = relationship('EngineConfig', back_populates='valves')
    def __repr__(self) -> str:
        return f'<Valves {self.valves_per_engine} ({self.valves_id})>'
class FuelDeliveryType(Base):
    __tablename__ = 'autocare_fuel_delivery_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_delivery_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    fuel_delivery_configs = relationship('FuelDeliveryConfig', back_populates='fuel_delivery_type')
    def __repr__(self) -> str:
        return f'<FuelDeliveryType {self.name} ({self.fuel_delivery_type_id})>'
class FuelDeliverySubType(Base):
    __tablename__ = 'autocare_fuel_delivery_subtype'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_delivery_subtype_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    fuel_delivery_configs = relationship('FuelDeliveryConfig', back_populates='fuel_delivery_subtype')
    def __repr__(self) -> str:
        return f'<FuelDeliverySubType {self.name} ({self.fuel_delivery_subtype_id})>'
class FuelSystemControlType(Base):
    __tablename__ = 'autocare_fuel_system_control_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_system_control_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    fuel_delivery_configs = relationship('FuelDeliveryConfig', back_populates='fuel_system_control_type')
    def __repr__(self) -> str:
        return f'<FuelSystemControlType {self.name} ({self.fuel_system_control_type_id})>'
class FuelSystemDesign(Base):
    __tablename__ = 'autocare_fuel_system_design'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_system_design_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    fuel_delivery_configs = relationship('FuelDeliveryConfig', back_populates='fuel_system_design')
    def __repr__(self) -> str:
        return f'<FuelSystemDesign {self.name} ({self.fuel_system_design_id})>'
class FuelDeliveryConfig(Base):
    __tablename__ = 'autocare_fuel_delivery_config'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_delivery_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    fuel_delivery_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_fuel_delivery_type.fuel_delivery_type_id'), nullable=False)
    fuel_delivery_subtype_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_fuel_delivery_subtype.fuel_delivery_subtype_id'), nullable=False)
    fuel_system_control_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_fuel_system_control_type.fuel_system_control_type_id'), nullable=False)
    fuel_system_design_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_fuel_system_design.fuel_system_design_id'), nullable=False)
    fuel_delivery_type = relationship('FuelDeliveryType', back_populates='fuel_delivery_configs')
    fuel_delivery_subtype = relationship('FuelDeliverySubType', back_populates='fuel_delivery_configs')
    fuel_system_control_type = relationship('FuelSystemControlType', back_populates='fuel_delivery_configs')
    fuel_system_design = relationship('FuelSystemDesign', back_populates='fuel_delivery_configs')
    engine_configs = relationship('EngineConfig', back_populates='fuel_delivery_config')
    def __repr__(self) -> str:
        return f'<FuelDeliveryConfig {self.fuel_delivery_config_id}>'
class PowerOutput(Base):
    __tablename__ = 'autocare_power_output'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    power_output_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    horsepower: Mapped[str] = mapped_column(String(10), nullable=False)
    kilowatt: Mapped[str] = mapped_column(String(10), nullable=False)
    engine_configs = relationship('EngineConfig', back_populates='power_output')
    def __repr__(self) -> str:
        return f'<PowerOutput {self.horsepower}hp/{self.kilowatt}kw ({self.power_output_id})>'
class EngineConfig(Base):
    __tablename__ = 'autocare_engine_config'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    engine_base_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_engine_base.engine_base_id'), nullable=False)
    engine_designation_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_engine_designation.engine_designation_id'), nullable=False)
    engine_vin_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_engine_vin.engine_vin_id'), nullable=False)
    valves_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_valves.valves_id'), nullable=False)
    fuel_delivery_config_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_fuel_delivery_config.fuel_delivery_config_id'), nullable=False)
    aspiration_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_aspiration.aspiration_id'), nullable=False)
    cylinder_head_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_cylinder_head_type.cylinder_head_type_id'), nullable=False)
    fuel_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_fuel_type.fuel_type_id'), nullable=False)
    ignition_system_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_ignition_system_type.ignition_system_type_id'), nullable=False)
    engine_mfr_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_mfr.mfr_id'), nullable=False)
    engine_version_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_engine_version.engine_version_id'), nullable=False)
    power_output_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_power_output.power_output_id'), nullable=False)
    engine_base = relationship('EngineBase', back_populates='engine_configs')
    engine_designation = relationship('EngineDesignation', back_populates='engine_configs')
    engine_vin = relationship('EngineVIN', back_populates='engine_configs')
    valves = relationship('Valves', back_populates='engine_configs')
    fuel_delivery_config = relationship('FuelDeliveryConfig', back_populates='engine_configs')
    aspiration = relationship('Aspiration', back_populates='engine_configs')
    cylinder_head_type = relationship('CylinderHeadType', back_populates='engine_configs')
    fuel_type = relationship('FuelType', back_populates='engine_configs')
    ignition_system_type = relationship('IgnitionSystemType', back_populates='engine_configs')
    engine_mfr = relationship('Mfr', back_populates='engine_configs')
    engine_version = relationship('EngineVersion', back_populates='engine_configs')
    power_output = relationship('PowerOutput', back_populates='engine_configs')
    def __repr__(self) -> str:
        return f'<EngineConfig {self.engine_config_id}>'
vehicle_to_engine_config = Table('autocare_vehicle_to_engine_config', Base.metadata, Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), Column('vehicle_id', Integer, ForeignKey('autocare_vehicle.vehicle_id'), nullable=False), Column('engine_config_id', Integer, ForeignKey('autocare_engine_config.engine_config_id'), nullable=False), Column('source', String(10), nullable=True))
class SpringType(Base):
    __tablename__ = 'autocare_spring_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    spring_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    front_spring_configs = relationship('SpringTypeConfig', foreign_keys='[SpringTypeConfig.front_spring_type_id]', back_populates='front_spring_type')
    rear_spring_configs = relationship('SpringTypeConfig', foreign_keys='[SpringTypeConfig.rear_spring_type_id]', back_populates='rear_spring_type')
    def __repr__(self) -> str:
        return f'<SpringType {self.name} ({self.spring_type_id})>'
class SpringTypeConfig(Base):
    __tablename__ = 'autocare_spring_type_config'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    spring_type_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    front_spring_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_spring_type.spring_type_id'), nullable=False)
    rear_spring_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_spring_type.spring_type_id'), nullable=False)
    front_spring_type = relationship('SpringType', foreign_keys=[front_spring_type_id], back_populates='front_spring_configs')
    rear_spring_type = relationship('SpringType', foreign_keys=[rear_spring_type_id], back_populates='rear_spring_configs')
    def __repr__(self) -> str:
        return f'<SpringTypeConfig {self.spring_type_config_id}>'
vehicle_to_spring_type_config = Table('autocare_vehicle_to_spring_type_config', Base.metadata, Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), Column('vehicle_id', Integer, ForeignKey('autocare_vehicle.vehicle_id'), nullable=False), Column('spring_type_config_id', Integer, ForeignKey('autocare_spring_type_config.spring_type_config_id'), nullable=False), Column('source', String(10), nullable=True))
class SteeringType(Base):
    __tablename__ = 'autocare_steering_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    steering_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    steering_configs = relationship('SteeringConfig', back_populates='steering_type')
    def __repr__(self) -> str:
        return f'<SteeringType {self.name} ({self.steering_type_id})>'
class SteeringSystem(Base):
    __tablename__ = 'autocare_steering_system'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    steering_system_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    steering_configs = relationship('SteeringConfig', back_populates='steering_system')
    def __repr__(self) -> str:
        return f'<SteeringSystem {self.name} ({self.steering_system_id})>'
class SteeringConfig(Base):
    __tablename__ = 'autocare_steering_config'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    steering_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    steering_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_steering_type.steering_type_id'), nullable=False)
    steering_system_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_steering_system.steering_system_id'), nullable=False)
    steering_type = relationship('SteeringType', back_populates='steering_configs')
    steering_system = relationship('SteeringSystem', back_populates='steering_configs')
    def __repr__(self) -> str:
        return f'<SteeringConfig {self.steering_config_id}>'
vehicle_to_steering_config = Table('autocare_vehicle_to_steering_config', Base.metadata, Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), Column('vehicle_id', Integer, ForeignKey('autocare_vehicle.vehicle_id'), nullable=False), Column('steering_config_id', Integer, ForeignKey('autocare_steering_config.steering_config_id'), nullable=False), Column('source', String(10), nullable=True))
class TransmissionType(Base):
    __tablename__ = 'autocare_transmission_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    transmission_bases = relationship('TransmissionBase', back_populates='transmission_type')
    def __repr__(self) -> str:
        return f'<TransmissionType {self.name} ({self.transmission_type_id})>'
class TransmissionNumSpeeds(Base):
    __tablename__ = 'autocare_transmission_num_speeds'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_num_speeds_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    num_speeds: Mapped[str] = mapped_column(String(3), nullable=False, index=True)
    transmission_bases = relationship('TransmissionBase', back_populates='transmission_num_speeds')
    def __repr__(self) -> str:
        return f'<TransmissionNumSpeeds {self.num_speeds} ({self.transmission_num_speeds_id})>'
class TransmissionControlType(Base):
    __tablename__ = 'autocare_transmission_control_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_control_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    transmission_bases = relationship('TransmissionBase', back_populates='transmission_control_type')
    def __repr__(self) -> str:
        return f'<TransmissionControlType {self.name} ({self.transmission_control_type_id})>'
class TransmissionBase(Base):
    __tablename__ = 'autocare_transmission_base'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_base_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    transmission_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_transmission_type.transmission_type_id'), nullable=False)
    transmission_num_speeds_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_transmission_num_speeds.transmission_num_speeds_id'), nullable=False)
    transmission_control_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_transmission_control_type.transmission_control_type_id'), nullable=False)
    transmission_type = relationship('TransmissionType', back_populates='transmission_bases')
    transmission_num_speeds = relationship('TransmissionNumSpeeds', back_populates='transmission_bases')
    transmission_control_type = relationship('TransmissionControlType', back_populates='transmission_bases')
    transmissions = relationship('Transmission', back_populates='transmission_base')
    def __repr__(self) -> str:
        return f'<TransmissionBase {self.transmission_base_id}>'
class TransmissionMfrCode(Base):
    __tablename__ = 'autocare_transmission_mfr_code'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_mfr_code_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    transmissions = relationship('Transmission', back_populates='transmission_mfr_code')
    def __repr__(self) -> str:
        return f'<TransmissionMfrCode {self.code} ({self.transmission_mfr_code_id})>'
class ElecControlled(Base):
    __tablename__ = 'autocare_elec_controlled'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    elec_controlled_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    value: Mapped[str] = mapped_column(String(3), nullable=False, index=True)
    transmissions = relationship('Transmission', back_populates='elec_controlled')
    def __repr__(self) -> str:
        return f'<ElecControlled {self.value} ({self.elec_controlled_id})>'
class Transmission(Base):
    __tablename__ = 'autocare_transmission'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    transmission_base_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_transmission_base.transmission_base_id'), nullable=False)
    transmission_mfr_code_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_transmission_mfr_code.transmission_mfr_code_id'), nullable=False)
    elec_controlled_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_elec_controlled.elec_controlled_id'), nullable=False)
    transmission_mfr_id: Mapped[int] = mapped_column(Integer, ForeignKey('autocare_mfr.mfr_id'), nullable=False)
    transmission_base = relationship('TransmissionBase', back_populates='transmissions')
    transmission_mfr_code = relationship('TransmissionMfrCode', back_populates='transmissions')
    elec_controlled = relationship('ElecControlled', back_populates='transmissions')
    transmission_mfr = relationship('Mfr', back_populates='transmission_configs')
    def __repr__(self) -> str:
        return f'<Transmission {self.transmission_id}>'
vehicle_to_transmission = Table('autocare_vehicle_to_transmission', Base.metadata, Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), Column('vehicle_id', Integer, ForeignKey('autocare_vehicle.vehicle_id'), nullable=False), Column('transmission_id', Integer, ForeignKey('autocare_transmission.transmission_id'), nullable=False), Column('source', String(10), nullable=True))
class WheelBase(Base):
    __tablename__ = 'autocare_wheel_base'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wheel_base_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    wheel_base: Mapped[str] = mapped_column(String(10), nullable=False)
    wheel_base_metric: Mapped[str] = mapped_column(String(10), nullable=False)
    def __repr__(self) -> str:
        return f'<WheelBase {self.wheel_base} ({self.wheel_base_id})>'
vehicle_to_wheel_base = Table('autocare_vehicle_to_wheel_base', Base.metadata, Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4), Column('vehicle_id', Integer, ForeignKey('autocare_vehicle.vehicle_id'), nullable=False), Column('wheel_base_id', Integer, ForeignKey('autocare_wheel_base.wheel_base_id'), nullable=False), Column('source', String(10), nullable=True))
class VCdbVersion(Base):
    __tablename__ = 'autocare_vcdb_version'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    def __repr__(self) -> str:
        return f"<VCdbVersion {self.version_date.strftime('%Y-%m-%d')}>"