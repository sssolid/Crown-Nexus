from __future__ import annotations
'VCdb (Vehicle Component Database) models.\n\nThis module defines the SQLAlchemy models that correspond to the VCdb database schema.\nThese models represent vehicle information and their components according to\nAuto Care Association standards.\n'
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
class Make(Base):
    __tablename__ = 'make'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    make_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    vehicles: Mapped[List['Vehicle']] = relationship('Vehicle', secondary='vcdb.base_vehicle', primaryjoin='Make.make_id == BaseVehicle.make_id', secondaryjoin='BaseVehicle.base_vehicle_id == Vehicle.base_vehicle_id', viewonly=True)
    base_vehicles: Mapped[List['BaseVehicle']] = relationship('BaseVehicle', back_populates='make')
    def __repr__(self) -> str:
        return f'<Make {self.name} ({self.make_id})>'
class Year(Base):
    __tablename__ = 'year'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    year_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    base_vehicles: Mapped[List['BaseVehicle']] = relationship('BaseVehicle', back_populates='year')
    def __repr__(self) -> str:
        return f'<Year {self.year_id}>'
class Model(Base):
    __tablename__ = 'model'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    vehicle_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.vehicle_type.vehicle_type_id'), nullable=False)
    base_vehicles: Mapped[List['BaseVehicle']] = relationship('BaseVehicle', back_populates='model')
    vehicle_type: Mapped['VehicleType'] = relationship('VehicleType', back_populates='models')
    def __repr__(self) -> str:
        return f'<Model {self.name} ({self.model_id})>'
class VehicleType(Base):
    __tablename__ = 'vehicle_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    vehicle_type_group_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('vcdb.vehicle_type_group.vehicle_type_group_id'), nullable=True)
    models: Mapped[List['Model']] = relationship('Model', back_populates='vehicle_type')
    vehicle_type_group: Mapped['VehicleTypeGroup'] = relationship('VehicleTypeGroup', back_populates='vehicle_types')
    def __repr__(self) -> str:
        return f'<VehicleType {self.name} ({self.vehicle_type_id})>'
class VehicleTypeGroup(Base):
    __tablename__ = 'vehicle_type_group'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_type_group_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    vehicle_types: Mapped[List['VehicleType']] = relationship('VehicleType', back_populates='vehicle_type_group')
    def __repr__(self) -> str:
        return f'<VehicleTypeGroup {self.name} ({self.vehicle_type_group_id})>'
class SubModel(Base):
    __tablename__ = 'submodel'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submodel_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    vehicles: Mapped[List['Vehicle']] = relationship('Vehicle', back_populates='submodel')
    def __repr__(self) -> str:
        return f'<SubModel {self.name} ({self.submodel_id})>'
class Region(Base):
    __tablename__ = 'region'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    region_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('vcdb.region.region_id'), nullable=True)
    abbr: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    parent: Mapped['Region'] = relationship('Region', remote_side='Region.region_id', back_populates='children')
    children: Mapped[List['Region']] = relationship('Region', back_populates='parent', cascade='all, delete-orphan')
    vehicles: Mapped[List['Vehicle']] = relationship('Vehicle', back_populates='region')
    def __repr__(self) -> str:
        return f'<Region {self.name} ({self.region_id})>'
class PublicationStage(Base):
    __tablename__ = 'publication_stage'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_stage_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    vehicles: Mapped[List['Vehicle']] = relationship('Vehicle', back_populates='publication_stage')
    def __repr__(self) -> str:
        return f'<PublicationStage {self.name} ({self.publication_stage_id})>'
class BaseVehicle(Base):
    __tablename__ = 'base_vehicle'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    base_vehicle_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    year_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.year.year_id'), nullable=False)
    make_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.make.make_id'), nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.model.model_id'), nullable=False)
    year: Mapped['Year'] = relationship('Year', back_populates='base_vehicles')
    make: Mapped['Make'] = relationship('Make', back_populates='base_vehicles')
    model: Mapped['Model'] = relationship('Model', back_populates='base_vehicles')
    vehicles: Mapped[List['Vehicle']] = relationship('Vehicle', back_populates='base_vehicle')
    def __repr__(self) -> str:
        return f'<BaseVehicle {self.base_vehicle_id}>'
class Vehicle(Base):
    __tablename__ = 'vehicle'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    base_vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.base_vehicle.base_vehicle_id'), nullable=False)
    submodel_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.submodel.submodel_id'), nullable=False)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.region.region_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    publication_stage_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.publication_stage.publication_stage_id'), nullable=False, default=4)
    publication_stage_source: Mapped[str] = mapped_column(String(100), nullable=False)
    publication_stage_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    base_vehicle: Mapped['BaseVehicle'] = relationship('BaseVehicle', back_populates='vehicles')
    submodel: Mapped['SubModel'] = relationship('SubModel', back_populates='vehicles')
    region: Mapped['Region'] = relationship('Region', back_populates='vehicles')
    publication_stage: Mapped['PublicationStage'] = relationship('PublicationStage', back_populates='vehicles')
    drive_types: Mapped[List['DriveType']] = relationship('DriveType', secondary='vcdb.vehicle_to_drive_type')
    brake_configs: Mapped[List['BrakeConfig']] = relationship('BrakeConfig', secondary='vcdb.vehicle_to_brake_config')
    bed_configs: Mapped[List['BedConfig']] = relationship('BedConfig', secondary='vcdb.vehicle_to_bed_config')
    body_style_configs: Mapped[List['BodyStyleConfig']] = relationship('BodyStyleConfig', secondary='vcdb.vehicle_to_body_style_config')
    mfr_body_codes: Mapped[List['MfrBodyCode']] = relationship('MfrBodyCode', secondary='vcdb.vehicle_to_mfr_body_code')
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', secondary='vcdb.vehicle_to_engine_config', primaryjoin='Vehicle.vehicle_id == VehicleToEngineConfig.vehicle_id', secondaryjoin='VehicleToEngineConfig.engine_config_id == EngineConfig2.engine_config_id')
    spring_type_configs: Mapped[List['SpringTypeConfig']] = relationship('SpringTypeConfig', secondary='vcdb.vehicle_to_spring_type_config')
    steering_configs: Mapped[List['SteeringConfig']] = relationship('SteeringConfig', secondary='vcdb.vehicle_to_steering_config')
    transmissions: Mapped[List['Transmission']] = relationship('Transmission', secondary='vcdb.vehicle_to_transmission')
    wheel_bases: Mapped[List['WheelBase']] = relationship('WheelBase', secondary='vcdb.vehicle_to_wheel_base')
    @property
    def make(self) -> Make:
        return self.base_vehicle.make
    @property
    def year(self) -> Optional[int]:
        if self.base_vehicle and self.base_vehicle.year:
            return self.base_vehicle.year.year_id
        return None
    @property
    def model(self) -> str:
        return self.base_vehicle.model.name
    def __repr__(self) -> str:
        return f'<Vehicle {self.vehicle_id}>'
class DriveType(Base):
    __tablename__ = 'drive_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    drive_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    def __repr__(self) -> str:
        return f'<DriveType {self.name} ({self.drive_type_id})>'
class VehicleToDriveType(Base):
    __tablename__ = 'vehicle_to_drive_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_to_drive_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.vehicle.vehicle_id'), nullable=False)
    drive_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.drive_type.drive_type_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    def __repr__(self) -> str:
        return f'<VehicleToDriveType(id={self.id}, vehicle_to_drive_type_id={self.vehicle_to_drive_type_id}, vehicle_id={self.vehicle_id}, drive_type_id={self.drive_type_id}, source={self.source})>'
class BrakeType(Base):
    __tablename__ = 'brake_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brake_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    front_brake_configs: Mapped[List['BrakeConfig']] = relationship('BrakeConfig', primaryjoin='BrakeType.brake_type_id == BrakeConfig.front_brake_type_id', back_populates='front_brake_type')
    rear_brake_configs: Mapped[List['BrakeConfig']] = relationship('BrakeConfig', primaryjoin='BrakeType.brake_type_id == BrakeConfig.rear_brake_type_id', back_populates='rear_brake_type')
    def __repr__(self) -> str:
        return f'<BrakeType {self.name} ({self.brake_type_id})>'
class BrakeSystem(Base):
    __tablename__ = 'brake_system'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brake_system_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    brake_configs: Mapped[List['BrakeConfig']] = relationship('BrakeConfig', back_populates='brake_system')
    def __repr__(self) -> str:
        return f'<BrakeSystem {self.name} ({self.brake_system_id})>'
class BrakeABS(Base):
    __tablename__ = 'brake_abs'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brake_abs_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    brake_configs: Mapped[List['BrakeConfig']] = relationship('BrakeConfig', back_populates='brake_abs')
    def __repr__(self) -> str:
        return f'<BrakeABS {self.name} ({self.brake_abs_id})>'
class BrakeConfig(Base):
    __tablename__ = 'brake_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brake_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    front_brake_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.brake_type.brake_type_id'), nullable=False)
    rear_brake_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.brake_type.brake_type_id'), nullable=False)
    brake_system_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.brake_system.brake_system_id'), nullable=False)
    brake_abs_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.brake_abs.brake_abs_id'), nullable=False)
    front_brake_type: Mapped['BrakeType'] = relationship('BrakeType', primaryjoin='BrakeConfig.front_brake_type_id == BrakeType.brake_type_id', back_populates='front_brake_configs')
    rear_brake_type: Mapped['BrakeType'] = relationship('BrakeType', primaryjoin='BrakeConfig.rear_brake_type_id == BrakeType.brake_type_id', back_populates='rear_brake_configs')
    brake_system: Mapped['BrakeSystem'] = relationship('BrakeSystem', back_populates='brake_configs')
    brake_abs: Mapped['BrakeABS'] = relationship('BrakeABS', back_populates='brake_configs')
    def __repr__(self) -> str:
        return f'<BrakeConfig {self.brake_config_id}>'
class VehicleToBrakeConfig(Base):
    __tablename__ = 'vehicle_to_brake_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_to_brake_config_id: Mapped[int] = mapped_column('vehicle_to_brake_config_id', Integer, nullable=False, unique=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.vehicle.vehicle_id'), nullable=False)
    brake_config_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.brake_config.brake_config_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column('source', String(10), nullable=True)
    def __repr__(self) -> str:
        return f'<VehicleToBrakeConfig(id={self.id}, config_id={self.vehicle_to_brake_config_id}, vehicle_id={self.vehicle_id}, brake_config_id={self.brake_config_id}, source={self.source})>'
class BedType(Base):
    __tablename__ = 'bed_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bed_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    bed_configs: Mapped[List['BedConfig']] = relationship('BedConfig', back_populates='bed_type')
    def __repr__(self) -> str:
        return f'<BedType {self.name} ({self.bed_type_id})>'
class BedLength(Base):
    __tablename__ = 'bed_length'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bed_length_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    length: Mapped[str] = mapped_column(String(10), nullable=False)
    length_metric: Mapped[str] = mapped_column(String(10), nullable=False)
    bed_configs: Mapped[List['BedConfig']] = relationship('BedConfig', back_populates='bed_length')
    def __repr__(self) -> str:
        return f'<BedLength {self.length} ({self.bed_length_id})>'
class BedConfig(Base):
    __tablename__ = 'bed_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bed_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    bed_length_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.bed_length.bed_length_id'), nullable=False)
    bed_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.bed_type.bed_type_id'), nullable=False)
    bed_length: Mapped['BedLength'] = relationship('BedLength', back_populates='bed_configs')
    bed_type: Mapped['BedType'] = relationship('BedType', back_populates='bed_configs')
    def __repr__(self) -> str:
        return f'<BedConfig {self.bed_config_id}>'
class VehicleToBedConfig(Base):
    __tablename__ = 'vehicle_to_bed_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_to_bed_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.vehicle.vehicle_id'), nullable=False)
    bed_config_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.bed_config.bed_config_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    def __repr__(self) -> str:
        return f'<VehicleToBedConfig(id={self.id}, vehicle_to_bed_config_id={self.vehicle_to_bed_config_id}, vehicle_id={self.vehicle_id}, bed_config_id={self.bed_config_id}, source={self.source})>'
class BodyType(Base):
    __tablename__ = 'body_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    body_style_configs: Mapped[List['BodyStyleConfig']] = relationship('BodyStyleConfig', back_populates='body_type')
    def __repr__(self) -> str:
        return f'<BodyType {self.name} ({self.body_type_id})>'
class BodyNumDoors(Base):
    __tablename__ = 'body_num_doors'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body_num_doors_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    num_doors: Mapped[str] = mapped_column(String(3), nullable=False)
    body_style_configs: Mapped[List['BodyStyleConfig']] = relationship('BodyStyleConfig', back_populates='body_num_doors')
    def __repr__(self) -> str:
        return f'<BodyNumDoors {self.num_doors} ({self.body_num_doors_id})>'
class BodyStyleConfig(Base):
    __tablename__ = 'body_style_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body_style_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    body_num_doors_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.body_num_doors.body_num_doors_id'), nullable=False)
    body_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.body_type.body_type_id'), nullable=False)
    body_num_doors: Mapped['BodyNumDoors'] = relationship('BodyNumDoors', back_populates='body_style_configs')
    body_type: Mapped['BodyType'] = relationship('BodyType', back_populates='body_style_configs')
    def __repr__(self) -> str:
        return f'<BodyStyleConfig {self.body_style_config_id}>'
class VehicleToBodyStyleConfig(Base):
    __tablename__ = 'vehicle_to_body_style_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_to_body_style_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.vehicle.vehicle_id'), nullable=False)
    body_style_config_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.body_style_config.body_style_config_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    def __repr__(self) -> str:
        return f'<VehicleToBodyStyleConfig(id={self.id}, vehicle_to_body_style_config_id={self.vehicle_to_body_style_config_id}, vehicle_id={self.vehicle_id}, body_style_config_id={self.body_style_config_id}, source={self.source})>'
class MfrBodyCode(Base):
    __tablename__ = 'mfr_body_code'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mfr_body_code_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    def __repr__(self) -> str:
        return f'<MfrBodyCode {self.code} ({self.mfr_body_code_id})>'
class VehicleToMfrBodyCode(Base):
    __tablename__ = 'vehicle_to_mfr_body_code'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_to_mfr_body_code_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.vehicle.vehicle_id'), nullable=False)
    mfr_body_code_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.mfr_body_code.mfr_body_code_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    def __repr__(self) -> str:
        return f'<VehicleToMfrBodyCode(id={self.id}, vehicle_to_mfr_body_code_id={self.vehicle_to_mfr_body_code_id}, vehicle_id={self.vehicle_id}, mfr_body_code_id={self.mfr_body_code_id}, source={self.source})>'
class EngineBlock(Base):
    __tablename__ = 'engine_block'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_block_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    liter: Mapped[str] = mapped_column(String(6), nullable=False)
    cc: Mapped[str] = mapped_column(String(8), nullable=False)
    cid: Mapped[str] = mapped_column(String(7), nullable=False)
    cylinders: Mapped[str] = mapped_column(String(2), nullable=False)
    block_type: Mapped[str] = mapped_column(String(2), nullable=False)
    engine_bases: Mapped[List['EngineBase2']] = relationship('EngineBase2', back_populates='engine_block')
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='engine_block')
    def __repr__(self) -> str:
        return f'<EngineBlock {self.liter}L {self.cylinders}cyl ({self.engine_block_id})>'
class EngineBoreStroke(Base):
    __tablename__ = 'engine_bore_stroke'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_bore_stroke_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    bore_in: Mapped[str] = mapped_column(String(10), nullable=False)
    bore_metric: Mapped[str] = mapped_column(String(10), nullable=False)
    stroke_in: Mapped[str] = mapped_column(String(10), nullable=False)
    stroke_metric: Mapped[str] = mapped_column(String(10), nullable=False)
    engine_bases: Mapped[List['EngineBase2']] = relationship('EngineBase2', back_populates='engine_bore_stroke')
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='engine_bore_stroke')
    def __repr__(self) -> str:
        return f'<EngineBoreStroke {self.bore_in}x{self.stroke_in} ({self.engine_bore_stroke_id})>'
class EngineBase(Base):
    __tablename__ = 'engine_base'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_base_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
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
        return f'<EngineBase {self.engine_base_id}>'
class EngineBase2(Base):
    __tablename__ = 'engine_base2'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_base_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    engine_block_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_block.engine_block_id'), nullable=False)
    engine_bore_stroke_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_bore_stroke.engine_bore_stroke_id'), nullable=False)
    engine_block: Mapped['EngineBlock'] = relationship('EngineBlock', back_populates='engine_bases')
    engine_bore_stroke: Mapped['EngineBoreStroke'] = relationship('EngineBoreStroke', back_populates='engine_bases')
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='engine_base')
    def __repr__(self) -> str:
        return f'<EngineBase2 {self.engine_base_id}>'
class Aspiration(Base):
    __tablename__ = 'aspiration'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aspiration_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='aspiration')
    def __repr__(self) -> str:
        return f'<Aspiration {self.name} ({self.aspiration_id})>'
class FuelType(Base):
    __tablename__ = 'fuel_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='fuel_type')
    def __repr__(self) -> str:
        return f'<FuelType {self.name} ({self.fuel_type_id})>'
class CylinderHeadType(Base):
    __tablename__ = 'cylinder_head_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cylinder_head_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='cylinder_head_type')
    def __repr__(self) -> str:
        return f'<CylinderHeadType {self.name} ({self.cylinder_head_type_id})>'
class EngineDesignation(Base):
    __tablename__ = 'engine_designation'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_designation_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='engine_designation')
    def __repr__(self) -> str:
        return f'<EngineDesignation {self.name} ({self.engine_designation_id})>'
class EngineVIN(Base):
    __tablename__ = 'engine_vin'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_vin_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    code: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='engine_vin')
    def __repr__(self) -> str:
        return f'<EngineVIN {self.code} ({self.engine_vin_id})>'
class EngineVersion(Base):
    __tablename__ = 'engine_version'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_version_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    version: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='engine_version')
    def __repr__(self) -> str:
        return f'<EngineVersion {self.version} ({self.engine_version_id})>'
class Mfr(Base):
    __tablename__ = 'mfr'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mfr_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='engine_mfr')
    transmission_configs: Mapped[List['Transmission']] = relationship('Transmission', back_populates='transmission_mfr')
    def __repr__(self) -> str:
        return f'<Mfr {self.name} ({self.mfr_id})>'
class IgnitionSystemType(Base):
    __tablename__ = 'ignition_system_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ignition_system_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='ignition_system_type')
    def __repr__(self) -> str:
        return f'<IgnitionSystemType {self.name} ({self.ignition_system_type_id})>'
class Valves(Base):
    __tablename__ = 'valves'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    valves_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    valves_per_engine: Mapped[str] = mapped_column(String(3), nullable=False)
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='valves')
    def __repr__(self) -> str:
        return f'<Valves {self.valves_per_engine} ({self.valves_id})>'
class FuelDeliveryType(Base):
    __tablename__ = 'fuel_delivery_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_delivery_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    fuel_delivery_configs: Mapped[List['FuelDeliveryConfig']] = relationship('FuelDeliveryConfig', back_populates='fuel_delivery_type')
    def __repr__(self) -> str:
        return f'<FuelDeliveryType {self.name} ({self.fuel_delivery_type_id})>'
class FuelDeliverySubType(Base):
    __tablename__ = 'fuel_delivery_subtype'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_delivery_subtype_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    fuel_delivery_configs: Mapped[List['FuelDeliveryConfig']] = relationship('FuelDeliveryConfig', back_populates='fuel_delivery_subtype')
    def __repr__(self) -> str:
        return f'<FuelDeliverySubType {self.name} ({self.fuel_delivery_subtype_id})>'
class FuelSystemControlType(Base):
    __tablename__ = 'fuel_system_control_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_system_control_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    fuel_delivery_configs: Mapped[List['FuelDeliveryConfig']] = relationship('FuelDeliveryConfig', back_populates='fuel_system_control_type')
    def __repr__(self) -> str:
        return f'<FuelSystemControlType {self.name} ({self.fuel_system_control_type_id})>'
class FuelSystemDesign(Base):
    __tablename__ = 'fuel_system_design'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_system_design_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    fuel_delivery_configs: Mapped[List['FuelDeliveryConfig']] = relationship('FuelDeliveryConfig', back_populates='fuel_system_design')
    def __repr__(self) -> str:
        return f'<FuelSystemDesign {self.name} ({self.fuel_system_design_id})>'
class FuelDeliveryConfig(Base):
    __tablename__ = 'fuel_delivery_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fuel_delivery_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    fuel_delivery_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.fuel_delivery_type.fuel_delivery_type_id'), nullable=False)
    fuel_delivery_subtype_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.fuel_delivery_subtype.fuel_delivery_subtype_id'), nullable=False)
    fuel_system_control_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.fuel_system_control_type.fuel_system_control_type_id'), nullable=False)
    fuel_system_design_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.fuel_system_design.fuel_system_design_id'), nullable=False)
    fuel_delivery_type: Mapped['FuelDeliveryType'] = relationship('FuelDeliveryType', back_populates='fuel_delivery_configs')
    fuel_delivery_subtype: Mapped['FuelDeliverySubType'] = relationship('FuelDeliverySubType', back_populates='fuel_delivery_configs')
    fuel_system_control_type: Mapped['FuelSystemControlType'] = relationship('FuelSystemControlType', back_populates='fuel_delivery_configs')
    fuel_system_design: Mapped['FuelSystemDesign'] = relationship('FuelSystemDesign', back_populates='fuel_delivery_configs')
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='fuel_delivery_config')
    def __repr__(self) -> str:
        return f'<FuelDeliveryConfig {self.fuel_delivery_config_id}>'
class PowerOutput(Base):
    __tablename__ = 'power_output'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    power_output_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    horsepower: Mapped[str] = mapped_column(String(10), nullable=False)
    kilowatt: Mapped[str] = mapped_column(String(10), nullable=False)
    engine_configs: Mapped[List['EngineConfig2']] = relationship('EngineConfig2', back_populates='power_output')
    def __repr__(self) -> str:
        return f'<PowerOutput {self.horsepower}hp/{self.kilowatt}kw ({self.power_output_id})>'
class EngineConfig(Base):
    __tablename__ = 'engine_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    engine_base_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_base.engine_base_id'), nullable=False)
    engine_designation_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_designation.engine_designation_id'), nullable=False)
    engine_vin_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_vin.engine_vin_id'), nullable=False)
    valves_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.valves.valves_id'), nullable=False)
    fuel_delivery_config_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.fuel_delivery_config.fuel_delivery_config_id'), nullable=False)
    aspiration_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.aspiration.aspiration_id'), nullable=False)
    cylinder_head_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.cylinder_head_type.cylinder_head_type_id'), nullable=False)
    fuel_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.fuel_type.fuel_type_id'), nullable=False)
    ignition_system_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.ignition_system_type.ignition_system_type_id'), nullable=False)
    engine_mfr_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.mfr.mfr_id'), nullable=False)
    engine_version_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_version.engine_version_id'), nullable=False)
    power_output_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.power_output.power_output_id'), nullable=False)
    def __repr__(self) -> str:
        return f'<EngineConfig {self.engine_config_id}>'
class EngineConfig2(Base):
    __tablename__ = 'engine_config2'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    engine_base_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_base2.engine_base_id'), nullable=False)
    engine_block_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_block.engine_block_id'), nullable=False)
    engine_bore_stroke_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_bore_stroke.engine_bore_stroke_id'))
    engine_designation_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_designation.engine_designation_id'), nullable=False)
    engine_vin_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_vin.engine_vin_id'), nullable=False)
    valves_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.valves.valves_id'), nullable=False)
    fuel_delivery_config_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.fuel_delivery_config.fuel_delivery_config_id'), nullable=False)
    aspiration_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.aspiration.aspiration_id'), nullable=False)
    cylinder_head_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.cylinder_head_type.cylinder_head_type_id'), nullable=False)
    fuel_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.fuel_type.fuel_type_id'), nullable=False)
    ignition_system_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.ignition_system_type.ignition_system_type_id'), nullable=False)
    engine_mfr_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.mfr.mfr_id'), nullable=False)
    engine_version_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_version.engine_version_id'), nullable=False)
    power_output_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.power_output.power_output_id'), nullable=False)
    engine_base: Mapped['EngineBase2'] = relationship('EngineBase2', back_populates='engine_configs')
    engine_block: Mapped['EngineBlock'] = relationship('EngineBlock', back_populates='engine_configs')
    engine_bore_stroke: Mapped['EngineBoreStroke'] = relationship('EngineBoreStroke', back_populates='engine_configs')
    engine_designation: Mapped['EngineDesignation'] = relationship('EngineDesignation', back_populates='engine_configs')
    engine_vin: Mapped['EngineVIN'] = relationship('EngineVIN', back_populates='engine_configs')
    valves: Mapped['Valves'] = relationship('Valves', back_populates='engine_configs')
    fuel_delivery_config: Mapped['FuelDeliveryConfig'] = relationship('FuelDeliveryConfig', back_populates='engine_configs')
    aspiration: Mapped['Aspiration'] = relationship('Aspiration', back_populates='engine_configs')
    cylinder_head_type: Mapped['CylinderHeadType'] = relationship('CylinderHeadType', back_populates='engine_configs')
    fuel_type: Mapped['FuelType'] = relationship('FuelType', back_populates='engine_configs')
    ignition_system_type: Mapped['IgnitionSystemType'] = relationship('IgnitionSystemType', back_populates='engine_configs')
    engine_mfr: Mapped['Mfr'] = relationship('Mfr', back_populates='engine_configs')
    engine_version: Mapped['EngineVersion'] = relationship('EngineVersion', back_populates='engine_configs')
    power_output: Mapped['PowerOutput'] = relationship('PowerOutput', back_populates='engine_configs')
    def __repr__(self) -> str:
        return f'<EngineConfig2 {self.engine_config_id}>'
class VehicleToEngineConfig(Base):
    __tablename__ = 'vehicle_to_engine_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_to_engine_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.vehicle.vehicle_id'), nullable=False)
    engine_config_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.engine_config2.engine_config_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    def __repr__(self) -> str:
        return f'<VehicleToEngineConfig(id={self.id}, vehicle_to_engine_config_id={self.vehicle_to_engine_config_id}, vehicle_id={self.vehicle_id}, engine_config_id={self.engine_config_id}, source={self.source})>'
class SpringType(Base):
    __tablename__ = 'spring_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    spring_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    front_spring_configs: Mapped[List['SpringTypeConfig']] = relationship('SpringTypeConfig', primaryjoin='SpringType.spring_type_id == SpringTypeConfig.front_spring_type_id', back_populates='front_spring_type')
    rear_spring_configs: Mapped[List['SpringTypeConfig']] = relationship('SpringTypeConfig', primaryjoin='SpringType.spring_type_id == SpringTypeConfig.rear_spring_type_id', back_populates='rear_spring_type')
    def __repr__(self) -> str:
        return f'<SpringType {self.name} ({self.spring_type_id})>'
class SpringTypeConfig(Base):
    __tablename__ = 'spring_type_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    spring_type_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    front_spring_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.spring_type.spring_type_id'), nullable=False)
    rear_spring_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.spring_type.spring_type_id'), nullable=False)
    front_spring_type: Mapped['SpringType'] = relationship('SpringType', primaryjoin='SpringTypeConfig.front_spring_type_id == SpringType.spring_type_id', back_populates='front_spring_configs')
    rear_spring_type: Mapped['SpringType'] = relationship('SpringType', primaryjoin='SpringTypeConfig.rear_spring_type_id == SpringType.spring_type_id', back_populates='rear_spring_configs')
    def __repr__(self) -> str:
        return f'<SpringTypeConfig {self.spring_type_config_id}>'
class VehicleToSpringTypeConfig(Base):
    __tablename__ = 'vehicle_to_spring_type_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_to_spring_type_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.vehicle.vehicle_id'), nullable=False)
    spring_type_config_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.spring_type_config.spring_type_config_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    def __repr__(self) -> str:
        return f'<VehicleToSpringTypeConfig(id={self.id}, vehicle_to_spring_type_config_id={self.vehicle_to_spring_type_config_id}, vehicle_id={self.vehicle_id}, spring_type_config_id={self.spring_type_config_id}, source={self.source})>'
class SteeringType(Base):
    __tablename__ = 'steering_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    steering_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    steering_configs: Mapped[List['SteeringConfig']] = relationship('SteeringConfig', back_populates='steering_type')
    def __repr__(self) -> str:
        return f'<SteeringType {self.name} ({self.steering_type_id})>'
class SteeringSystem(Base):
    __tablename__ = 'steering_system'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    steering_system_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    steering_configs: Mapped[List['SteeringConfig']] = relationship('SteeringConfig', back_populates='steering_system')
    def __repr__(self) -> str:
        return f'<SteeringSystem {self.name} ({self.steering_system_id})>'
class SteeringConfig(Base):
    __tablename__ = 'steering_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    steering_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    steering_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.steering_type.steering_type_id'), nullable=False)
    steering_system_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.steering_system.steering_system_id'), nullable=False)
    steering_type: Mapped['SteeringType'] = relationship('SteeringType', back_populates='steering_configs')
    steering_system: Mapped['SteeringSystem'] = relationship('SteeringSystem', back_populates='steering_configs')
    def __repr__(self) -> str:
        return f'<SteeringConfig {self.steering_config_id}>'
class VehicleToSteeringConfig(Base):
    __tablename__ = 'vehicle_to_steering_config'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_to_steering_config_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.vehicle.vehicle_id'), nullable=False)
    steering_config_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.steering_config.steering_config_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    def __repr__(self) -> str:
        return f'<VehicleToSteeringConfig(id={self.id}, vehicle_to_steering_config_id={self.vehicle_to_steering_config_id}, vehicle_id={self.vehicle_id}, steering_config_id={self.steering_config_id}, source={self.source})>'
class TransmissionType(Base):
    __tablename__ = 'transmission_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    transmission_bases: Mapped[List['TransmissionBase']] = relationship('TransmissionBase', back_populates='transmission_type')
    def __repr__(self) -> str:
        return f'<TransmissionType {self.name} ({self.transmission_type_id})>'
class TransmissionNumSpeeds(Base):
    __tablename__ = 'transmission_num_speeds'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_num_speeds_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    num_speeds: Mapped[str] = mapped_column(String(3), nullable=False, index=True)
    transmission_bases: Mapped[List['TransmissionBase']] = relationship('TransmissionBase', back_populates='transmission_num_speeds')
    def __repr__(self) -> str:
        return f'<TransmissionNumSpeeds {self.num_speeds} ({self.transmission_num_speeds_id})>'
class TransmissionControlType(Base):
    __tablename__ = 'transmission_control_type'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_control_type_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    transmission_bases: Mapped[List['TransmissionBase']] = relationship('TransmissionBase', back_populates='transmission_control_type')
    def __repr__(self) -> str:
        return f'<TransmissionControlType {self.name} ({self.transmission_control_type_id})>'
class TransmissionBase(Base):
    __tablename__ = 'transmission_base'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_base_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    transmission_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.transmission_type.transmission_type_id'), nullable=False)
    transmission_num_speeds_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.transmission_num_speeds.transmission_num_speeds_id'), nullable=False)
    transmission_control_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.transmission_control_type.transmission_control_type_id'), nullable=False)
    transmission_type: Mapped['TransmissionType'] = relationship('TransmissionType', back_populates='transmission_bases')
    transmission_num_speeds: Mapped['TransmissionNumSpeeds'] = relationship('TransmissionNumSpeeds', back_populates='transmission_bases')
    transmission_control_type: Mapped['TransmissionControlType'] = relationship('TransmissionControlType', back_populates='transmission_bases')
    transmissions: Mapped[List['Transmission']] = relationship('Transmission', back_populates='transmission_base')
    def __repr__(self) -> str:
        return f'<TransmissionBase {self.transmission_base_id}>'
class TransmissionMfrCode(Base):
    __tablename__ = 'transmission_mfr_code'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_mfr_code_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    transmissions: Mapped[List['Transmission']] = relationship('Transmission', back_populates='transmission_mfr_code')
    def __repr__(self) -> str:
        return f'<TransmissionMfrCode {self.code} ({self.transmission_mfr_code_id})>'
class ElecControlled(Base):
    __tablename__ = 'elec_controlled'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    elec_controlled_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    value: Mapped[str] = mapped_column(String(3), nullable=False, index=True)
    transmissions: Mapped[List['Transmission']] = relationship('Transmission', back_populates='elec_controlled')
    def __repr__(self) -> str:
        return f'<ElecControlled {self.value} ({self.elec_controlled_id})>'
class Transmission(Base):
    __tablename__ = 'transmission'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transmission_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    transmission_base_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.transmission_base.transmission_base_id'), nullable=False)
    transmission_mfr_code_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.transmission_mfr_code.transmission_mfr_code_id'), nullable=False)
    elec_controlled_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.elec_controlled.elec_controlled_id'), nullable=False)
    transmission_mfr_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.mfr.mfr_id'), nullable=False)
    transmission_base: Mapped['TransmissionBase'] = relationship('TransmissionBase', back_populates='transmissions')
    transmission_mfr_code: Mapped['TransmissionMfrCode'] = relationship('TransmissionMfrCode', back_populates='transmissions')
    elec_controlled: Mapped['ElecControlled'] = relationship('ElecControlled', back_populates='transmissions')
    transmission_mfr: Mapped['Mfr'] = relationship('Mfr', back_populates='transmission_configs')
    def __repr__(self) -> str:
        return f'<Transmission {self.transmission_id}>'
class VehicleToTransmission(Base):
    __tablename__ = 'vehicle_to_transmission'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_to_transmission_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.vehicle.vehicle_id'), nullable=False)
    transmission_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.transmission.transmission_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    def __repr__(self) -> str:
        return f'<VehicleToTransmission(id={self.id}, vehicle_to_transmission_id={self.vehicle_to_transmission_id}, vehicle_id={self.vehicle_id}, transmission_id={self.transmission_id}, source={self.source}>'
class WheelBase(Base):
    __tablename__ = 'wheel_base'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wheel_base_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    wheel_base: Mapped[str] = mapped_column(String(10), nullable=False)
    wheel_base_metric: Mapped[str] = mapped_column(String(10), nullable=False)
    def __repr__(self) -> str:
        return f'<WheelBase {self.wheel_base} ({self.wheel_base_id})>'
class VehicleToWheelBase(Base):
    __tablename__ = 'vehicle_to_wheel_base'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_to_wheel_base_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.vehicle.vehicle_id'), nullable=False)
    wheel_base_id: Mapped[int] = mapped_column(Integer, ForeignKey('vcdb.wheel_base.wheel_base_id'), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    def __repr__(self) -> str:
        return f'<VehicleToWheelBase(id={self.id}, vehicle_to_wheel_base_id={self.vehicle_to_wheel_base_id}, vehicle_id={self.vehicle_id}, wheel_base_id={self.wheel_base_id}, source={self.source}>'
class VCdbVersion(Base):
    __tablename__ = 'vcdb_version'
    __table_args__ = {'schema': 'vcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    def __repr__(self) -> str:
        return f"<VCdbVersion {self.version_date.strftime('%Y-%m-%d')}>"