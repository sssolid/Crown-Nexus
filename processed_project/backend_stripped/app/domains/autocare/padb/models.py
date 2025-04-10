from __future__ import annotations
'PAdb (Part Attribute Database) models.\n\nThis module defines the SQLAlchemy models that correspond to the PAdb database schema.\nThese models represent part attribute definitions, metadata, and valid values according\nto Auto Care Association standards.\n'
import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
class PartAttribute(Base):
    __tablename__ = 'part_attribute'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pa_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    pa_name: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    pa_descr: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    assignments: Mapped[List['PartAttributeAssignment']] = relationship('PartAttributeAssignment', back_populates='attribute')
    def __repr__(self) -> str:
        return f'<PartAttribute {self.pa_name} ({self.pa_id})>'
class MetaData(Base):
    __tablename__ = 'metadata'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meta_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    meta_name: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    meta_descr: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    meta_format: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    data_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    min_length: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_length: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    assignments: Mapped[List['PartAttributeAssignment']] = relationship('PartAttributeAssignment', back_populates='metadata_info')
    def __repr__(self) -> str:
        return f'<MetaData {self.meta_name} ({self.meta_id})>'
class MeasurementGroup(Base):
    __tablename__ = 'measurement_group'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    measurement_group_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    measurement_group_name: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    uom_codes: Mapped[List['MetaUOMCode']] = relationship('MetaUOMCode', back_populates='measurement_group')
    def __repr__(self) -> str:
        return f'<MeasurementGroup {self.measurement_group_name} ({self.measurement_group_id})>'
class MetaUOMCode(Base):
    __tablename__ = 'meta_uom_code'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meta_uom_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    uom_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    uom_description: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    uom_label: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    measurement_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('padb.measurement_group.measurement_group_id'), nullable=False)
    measurement_group: Mapped['MeasurementGroup'] = relationship('MeasurementGroup', back_populates='uom_codes')
    assignments: Mapped[List['MetaUomCodeAssignment']] = relationship('MetaUomCodeAssignment', back_populates='meta_uom')
    def __repr__(self) -> str:
        return f'<MetaUOMCode {self.uom_code} ({self.meta_uom_id})>'
class PartAttributeAssignment(Base):
    __tablename__ = 'part_attribute_assignment'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    papt_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    part_terminology_id: Mapped[int] = mapped_column(Integer, ForeignKey('pcdb.parts.part_terminology_id'), nullable=False)
    pa_id: Mapped[int] = mapped_column(Integer, ForeignKey('padb.part_attribute.pa_id'), nullable=False)
    meta_id: Mapped[int] = mapped_column(Integer, ForeignKey('padb.metadata.meta_id'), nullable=False)
    part: Mapped['Parts'] = relationship('Parts', primaryjoin='PartAttributeAssignment.part_terminology_id == Parts.part_terminology_id')
    attribute: Mapped['PartAttribute'] = relationship('PartAttribute', back_populates='assignments')
    metadata_info: Mapped['MetaData'] = relationship('MetaData', back_populates='assignments')
    uom_assignments: Mapped[List['MetaUomCodeAssignment']] = relationship('MetaUomCodeAssignment', back_populates='attribute_assignment')
    valid_value_assignments: Mapped[List['ValidValueAssignment']] = relationship('ValidValueAssignment', back_populates='attribute_assignment')
    style: Mapped['PartAttributeStyle'] = relationship('PartAttributeStyle', back_populates='attribute_assignment')
    def __repr__(self) -> str:
        return f'<PartAttributeAssignment {self.papt_id}: {self.part_terminology_id}>'
class MetaUomCodeAssignment(Base):
    __tablename__ = 'meta_uom_code_assignment'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meta_uom_code_assignment_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    papt_id: Mapped[int] = mapped_column(Integer, ForeignKey('padb.part_attribute_assignment.papt_id'), nullable=False)
    meta_uom_id: Mapped[int] = mapped_column(Integer, ForeignKey('padb.meta_uom_code.meta_uom_id'), nullable=False)
    attribute_assignment: Mapped['PartAttributeAssignment'] = relationship('PartAttributeAssignment', back_populates='uom_assignments')
    meta_uom: Mapped['MetaUOMCode'] = relationship('MetaUOMCode', back_populates='assignments')
    def __repr__(self) -> str:
        return f'<MetaUomCodeAssignment {self.meta_uom_code_assignment_id}>'
class ValidValue(Base):
    __tablename__ = 'valid_value'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    valid_value_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    valid_value: Mapped[str] = mapped_column(String(500), nullable=False)
    assignments: Mapped[List['ValidValueAssignment']] = relationship('ValidValueAssignment', back_populates='valid_value')
    def __repr__(self) -> str:
        return f'<ValidValue {self.valid_value_id}: {self.valid_value[:30]}...>'
class ValidValueAssignment(Base):
    __tablename__ = 'valid_value_assignment'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    valid_value_assignment_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    papt_id: Mapped[int] = mapped_column(Integer, ForeignKey('padb.part_attribute_assignment.papt_id'), nullable=False)
    valid_value_id: Mapped[int] = mapped_column(Integer, ForeignKey('padb.valid_value.valid_value_id'), nullable=False)
    attribute_assignment: Mapped['PartAttributeAssignment'] = relationship('PartAttributeAssignment', back_populates='valid_value_assignments')
    valid_value: Mapped['ValidValue'] = relationship('ValidValue', back_populates='assignments')
    def __repr__(self) -> str:
        return f'<ValidValueAssignment {self.valid_value_assignment_id}>'
class Style(Base):
    __tablename__ = 'style'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    style_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, unique=True, index=True)
    style_name: Mapped[Optional[str]] = mapped_column(String(225), nullable=True)
    part_attribute_styles: Mapped[List['PartAttributeStyle']] = relationship('PartAttributeStyle', primaryjoin='foreign(PartAttributeStyle.style_id) == Style.style_id', back_populates='style', viewonly=True)
    part_type_styles: Mapped[List['PartTypeStyle']] = relationship('PartTypeStyle', back_populates='style')
    def __repr__(self) -> str:
        return f'<Style {self.style_name} ({self.style_id})>'
class PartAttributeStyle(Base):
    __tablename__ = 'part_attribute_style'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    style_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    papt_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('padb.part_attribute_assignment.papt_id'), nullable=True)
    style: Mapped[Optional['Style']] = relationship('Style', primaryjoin='foreign(PartAttributeStyle.style_id) == Style.style_id', back_populates='part_attribute_styles', viewonly=True)
    attribute_assignment: Mapped['PartAttributeAssignment'] = relationship('PartAttributeAssignment', back_populates='style')
    def __repr__(self) -> str:
        return f'<PartAttributeStyle {self.id}: {self.papt_id}>'
class PartTypeStyle(Base):
    __tablename__ = 'part_type_style'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    style_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('padb.style.style_id'), nullable=True)
    part_terminology_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('pcdb.parts.part_terminology_id'), nullable=True)
    style: Mapped['Style'] = relationship('Style', back_populates='part_type_styles')
    part: Mapped['Parts'] = relationship('Parts', foreign_keys=[part_terminology_id])
    def __repr__(self) -> str:
        return f'<PartTypeStyle {self.id}: {self.part_terminology_id}>'
class PAdbVersion(Base):
    __tablename__ = 'padb_version'
    __table_args__ = {'schema': 'padb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    def __repr__(self) -> str:
        return f"<PAdbVersion {self.version_date.strftime('%Y-%m-%d')}>"