from __future__ import annotations

"""Qdb (Qualifier Database) models.

This module defines the SQLAlchemy models that correspond to the Qdb database schema.
These models represent qualifiers and their translations according to Auto Care
Association standards.
"""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    ForeignKeyConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class QualifierType(Base):
    """Model for qualifier types."""

    __tablename__ = "qualifier_type"
    __table_args__ = {"schema": "qdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    qualifier_type_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    qualifier_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships with explicit join conditions
    qualifiers: Mapped[List["Qualifier"]] = relationship(
        "Qualifier",
        primaryjoin="QualifierType.qualifier_type_id == Qualifier.qualifier_type_id",
        back_populates="qualifier_type",
    )

    def __repr__(self) -> str:
        return f"<QualifierType {self.qualifier_type} ({self.qualifier_type_id})>"


class Qualifier(Base):
    """Model for qualifiers."""

    __tablename__ = "qualifier"
    __table_args__ = (
        ForeignKeyConstraint(
            ["new_qualifier_id"],
            ["qdb.qualifier.qualifier_id"],
            deferrable=True,
            initially="DEFERRED",
        ),
        {"schema": "qdb"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    qualifier_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    qualifier_text: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    example_text: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    qualifier_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("qdb.qualifier_type.qualifier_type_id"), nullable=False
    )
    new_qualifier_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    when_modified: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    # Relationships with explicit join conditions
    qualifier_type: Mapped["QualifierType"] = relationship(
        "QualifierType",
        primaryjoin="Qualifier.qualifier_type_id == QualifierType.qualifier_type_id",
        back_populates="qualifiers",
    )

    translations: Mapped[List["QualifierTranslation"]] = relationship(
        "QualifierTranslation",
        primaryjoin="Qualifier.qualifier_id == QualifierTranslation.qualifier_id",
        back_populates="qualifier",
    )

    groups: Mapped[List["QualifierGroup"]] = relationship(  # Fixed to List
        "QualifierGroup",
        primaryjoin="Qualifier.qualifier_id == QualifierGroup.qualifier_id",
        back_populates="qualifier",
    )

    # Self-referential relationship with explicit join
    superseded_by: Mapped[Optional["Qualifier"]] = relationship(
        "Qualifier",
        primaryjoin="Qualifier.new_qualifier_id == Qualifier.qualifier_id",
        foreign_keys=[new_qualifier_id],
        remote_side=[qualifier_id],
        backref="supersedes",
    )

    def __repr__(self) -> str:
        text = self.qualifier_text or ""
        return f"<Qualifier {self.qualifier_id}: {text[:30]}...>"


class Language(Base):
    """Model for languages."""

    __tablename__ = "language"
    __table_args__ = {"schema": "qdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    language_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    language_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    dialect_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships with explicit join conditions
    translations: Mapped[List["QualifierTranslation"]] = relationship(
        "QualifierTranslation",
        primaryjoin="Language.language_id == QualifierTranslation.language_id",
        back_populates="language",
    )

    def __repr__(self) -> str:
        return f"<Language {self.language_name} ({self.language_id})>"


class QualifierTranslation(Base):
    """Model for qualifier translations."""

    __tablename__ = "qualifier_translation"
    __table_args__ = {"schema": "qdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    qualifier_translation_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    qualifier_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("qdb.qualifier.qualifier_id"), nullable=False
    )
    language_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("qdb.language.language_id"), nullable=False
    )
    translation_text: Mapped[str] = mapped_column(String(500), nullable=False)

    # Relationships with explicit join conditions
    qualifier: Mapped["Qualifier"] = relationship(
        "Qualifier",
        primaryjoin="QualifierTranslation.qualifier_id == Qualifier.qualifier_id",
        back_populates="translations",
    )

    language: Mapped["Language"] = relationship(
        "Language",
        primaryjoin="QualifierTranslation.language_id == Language.language_id",
        back_populates="translations",
    )

    def __repr__(self) -> str:
        return f"<QualifierTranslation {self.qualifier_translation_id}: {self.translation_text[:30]}...>"


class GroupNumber(Base):
    """Model for qualifier group numbers."""

    __tablename__ = "group_number"
    __table_args__ = {"schema": "qdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    group_number_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    group_description: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships with explicit join conditions
    qualifier_groups: Mapped[List["QualifierGroup"]] = relationship(
        "QualifierGroup",
        primaryjoin="GroupNumber.group_number_id == QualifierGroup.group_number_id",
        back_populates="group_number",
    )

    def __repr__(self) -> str:
        return f"<GroupNumber {self.group_number_id}: {self.group_description}>"


class QualifierGroup(Base):
    """Model for qualifier groups."""

    __tablename__ = "qualifier_group"
    __table_args__ = {"schema": "qdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    qualifier_group_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, index=True
    )
    group_number_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("qdb.group_number.group_number_id"), nullable=False
    )
    qualifier_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("qdb.qualifier.qualifier_id"), nullable=False
    )

    # Relationships with explicit join conditions
    group_number: Mapped["GroupNumber"] = relationship(
        "GroupNumber",
        primaryjoin="QualifierGroup.group_number_id == GroupNumber.group_number_id",
        back_populates="qualifier_groups",
    )

    qualifier: Mapped["Qualifier"] = relationship(
        "Qualifier",
        primaryjoin="QualifierGroup.qualifier_id == Qualifier.qualifier_id",
        back_populates="groups",
    )

    def __repr__(self) -> str:
        return f"<QualifierGroup {self.qualifier_group_id}: {self.group_number_id}/{self.qualifier_id}>"


class QdbVersion(Base):
    """Model for Qdb version tracking."""

    __tablename__ = "qdb_version"
    __table_args__ = {"schema": "qdb"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    version_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<QdbVersion {self.version_date.strftime('%Y-%m-%d')}>"
