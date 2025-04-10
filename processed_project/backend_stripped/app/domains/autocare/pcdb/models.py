from __future__ import annotations
'PCdb (Product Component Database) models.\n\nThis module defines the SQLAlchemy models that correspond to the PCdb database schema.\nThese models represent product parts terminology, categories, positions, and part\nattributes according to Auto Care Association standards.\n'
import uuid
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Table, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
class Parts(Base):
    __tablename__ = 'parts'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    part_terminology_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    part_terminology_name: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    parts_description_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('pcdb.parts_description.parts_description_id'), nullable=True)
    rev_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    description: Mapped['PartsDescription'] = relationship('PartsDescription', back_populates='parts')
    categories: Mapped[List['PartCategory']] = relationship('PartCategory', back_populates='part')
    positions: Mapped[List['PartPosition']] = relationship('PartPosition', back_populates='part')
    attributes: Mapped[List['PartAttributeAssignment']] = relationship('PartAttributeAssignment', back_populates='part')
    supersessions: Mapped[List['PartsSupersession']] = relationship('PartsSupersession', foreign_keys='[PartsSupersession.new_part_terminology_id]', primaryjoin='Parts.part_terminology_id==PartsSupersession.new_part_terminology_id', backref='new_part')
    superseded_by: Mapped['PartsSupersession'] = relationship('PartsSupersession', foreign_keys='[PartsSupersession.old_part_terminology_id]', primaryjoin='Parts.part_terminology_id==PartsSupersession.old_part_terminology_id', backref='old_part')
    def __repr__(self) -> str:
        return f'<Parts {self.part_terminology_name} ({self.part_terminology_id})>'
class PartsDescription(Base):
    __tablename__ = 'parts_description'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parts_description_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    parts_description: Mapped[str] = mapped_column(String(500), nullable=False)
    parts: Mapped[List['Parts']] = relationship('Parts', back_populates='description')
    def __repr__(self) -> str:
        return f'<PartsDescription {self.parts_description_id}: {self.parts_description[:30]}...>'
class Category(Base):
    __tablename__ = 'category'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    part_categories: Mapped[List['PartCategory']] = relationship('PartCategory', back_populates='category')
    code_masters: Mapped[List['CodeMaster']] = relationship('CodeMaster', back_populates='category')
    def __repr__(self) -> str:
        return f'<Category {self.category_name} ({self.category_id})>'
class SubCategory(Base):
    __tablename__ = 'subcategory'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subcategory_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    subcategory_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    part_categories: Mapped[List['PartCategory']] = relationship('PartCategory', back_populates='subcategory')
    code_masters: Mapped[List['CodeMaster']] = relationship('CodeMaster', back_populates='subcategory')
    def __repr__(self) -> str:
        return f'<SubCategory {self.subcategory_name} ({self.subcategory_id})>'
class Position(Base):
    __tablename__ = 'position'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    position_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    position: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    part_positions: Mapped[List['PartPosition']] = relationship('PartPosition', back_populates='position')
    code_masters: Mapped[List['CodeMaster']] = relationship('CodeMaster', back_populates='position')
    def __repr__(self) -> str:
        return f'<Position {self.position} ({self.position_id})>'
class PartCategory(Base):
    __tablename__ = 'part_category'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    part_category_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    part_terminology_id: Mapped[int] = mapped_column(Integer, ForeignKey('pcdb.parts.part_terminology_id'), nullable=False)
    subcategory_id: Mapped[int] = mapped_column(Integer, ForeignKey('pcdb.subcategory.subcategory_id'), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('pcdb.category.category_id'), nullable=False)
    part: Mapped['Parts'] = relationship('Parts', back_populates='categories')
    subcategory: Mapped['SubCategory'] = relationship('SubCategory', back_populates='part_categories')
    category: Mapped['Category'] = relationship('Category', back_populates='part_categories')
    def __repr__(self) -> str:
        return f'<PartCategory {self.part_category_id}: {self.part_terminology_id}>'
class PartPosition(Base):
    __tablename__ = 'part_position'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    part_position_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    part_terminology_id: Mapped[int] = mapped_column(Integer, ForeignKey('pcdb.parts.part_terminology_id'), nullable=False)
    position_id: Mapped[int] = mapped_column(Integer, ForeignKey('pcdb.position.position_id'), nullable=False)
    rev_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    part: Mapped['Part'] = relationship('Parts', back_populates='positions')
    position: Mapped['Position'] = relationship('Position', back_populates='part_positions')
    def __repr__(self) -> str:
        return f'<PartPosition {self.part_position_id}: {self.part_terminology_id}>'
class PartsSupersession(Base):
    __tablename__ = 'parts_supersession'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parts_supersession_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    old_part_terminology_id: Mapped[int] = mapped_column(Integer, nullable=False)
    old_part_terminology_name: Mapped[str] = mapped_column(String(256), nullable=False)
    new_part_terminology_id: Mapped[int] = mapped_column(Integer, nullable=False)
    new_part_terminology_name: Mapped[str] = mapped_column(String(256), nullable=False)
    rev_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    note: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    old_part_terminology: Mapped[Optional['Parts']] = relationship('Parts', primaryjoin='foreign(PartsSupersession.old_part_terminology_id) == Parts.part_terminology_id', viewonly=True)
    new_part_terminology: Mapped[Optional['Parts']] = relationship('Parts', primaryjoin='foreign(PartsSupersession.new_part_terminology_id) == Parts.part_terminology_id', viewonly=True)
    def __repr__(self) -> str:
        return f'<PartsSupersession {self.parts_supersession_id}: {self.old_part_terminology_id} -> {self.new_part_terminology_id}>'
class CodeMaster(Base):
    __tablename__ = 'code_master'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code_master_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    part_terminology_id: Mapped[int] = mapped_column(Integer, ForeignKey('pcdb.parts.part_terminology_id'), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('pcdb.category.category_id'), nullable=False)
    subcategory_id: Mapped[int] = mapped_column(Integer, ForeignKey('pcdb.subcategory.subcategory_id'), nullable=False)
    position_id: Mapped[int] = mapped_column(Integer, ForeignKey('pcdb.position.position_id'), nullable=False)
    rev_date: Mapped[date] = mapped_column(Date, nullable=False)
    part: Mapped['Part'] = relationship('Parts', foreign_keys=[part_terminology_id])
    category: Mapped['Category'] = relationship('Category', back_populates='code_masters')
    subcategory: Mapped['SubCategory'] = relationship('SubCategory', back_populates='code_masters')
    position: Mapped['Position'] = relationship('Position', back_populates='code_masters')
    def __repr__(self) -> str:
        return f'<CodeMaster {self.code_master_id}: {self.part_terminology_id}>'
class Alias(Base):
    __tablename__ = 'alias'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alias_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    alias_name: Mapped[str] = mapped_column(String(100), nullable=False)
    def __repr__(self) -> str:
        return f'<Alias {self.alias_name} ({self.alias_id})>'
parts_to_alias = Table('parts_to_alias', Base.metadata, Column('part_terminology_id', Integer, ForeignKey('pcdb.parts.part_terminology_id'), primary_key=True), Column('alias_id', Integer, ForeignKey('pcdb.alias.alias_id'), primary_key=True), schema='pcdb')
class Use(Base):
    __tablename__ = 'use'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    use_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    use_description: Mapped[str] = mapped_column(String(100), nullable=False)
    def __repr__(self) -> str:
        return f'<Use {self.use_description} ({self.use_id})>'
parts_to_use = Table('parts_to_use', Base.metadata, Column('part_terminology_id', Integer, ForeignKey('pcdb.parts.part_terminology_id'), primary_key=True), Column('use_id', Integer, ForeignKey('pcdb.use.use_id'), primary_key=True), schema='pcdb')
class PCdbVersion(Base):
    __tablename__ = 'pcdb_version'
    __table_args__ = {'schema': 'pcdb'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    def __repr__(self) -> str:
        return f"<PCdbVersion {self.version_date.strftime('%Y-%m-%d')}>"