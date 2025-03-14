# backend/app/models/compliance.py
"""
Compliance models.

This module defines models for compliance-related data:
- Proposition 65 chemicals and warnings
- DOT approvals
- Hazardous materials information
- Other regulatory compliance data

These models support product compliance with various regulations
and provide necessary information for documentation and labeling.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum as SQLAEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.db.base_class import Base

# For type hints only, not runtime imports
if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.user import User


class ChemicalType(str, Enum):
    """
    Types of chemical hazards under Proposition 65.

    Defines the categories of chemical hazards recognized by
    California's Proposition 65.
    """
    CARCINOGEN = "Carcinogen"
    REPRODUCTIVE_TOXICANT = "Reproductive Toxicant"
    BOTH = "Both"


class ExposureScenario(str, Enum):
    """
    Types of exposure scenarios for chemicals.

    Defines the different contexts in which chemical exposure
    might occur.
    """
    CONSUMER = "Consumer"
    OCCUPATIONAL = "Occupational"
    ENVIRONMENTAL = "Environmental"


class ApprovalStatus(str, Enum):
    """
    Statuses for regulatory approvals.

    Defines the possible states of a regulatory approval.
    """
    APPROVED = "Approved"
    PENDING = "Pending"
    REVOKED = "Revoked"
    NOT_REQUIRED = "Not Required"


class TransportRestriction(str, Enum):
    """
    Types of transportation restrictions.

    Defines the possible transportation restrictions for
    hazardous materials.
    """
    NONE = "None"
    AIR = "Air"
    GROUND = "Ground"
    SEA = "Sea"
    ALL = "All"


class Prop65Chemical(Base):
    """
    Proposition 65 chemical model.

    Represents chemicals listed under California's Proposition 65.

    Attributes:
        id: Primary key UUID
        name: Chemical name
        cas_number: Chemical Abstracts Service (CAS) Number
        type: Type of hazard (Carcinogen, Reproductive Toxicant, Both)
        exposure_limit: Exposure limit if applicable
        updated_at: Last update timestamp
    """
    __tablename__ = "prop65_chemical"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    cas_number: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )
    type: Mapped[ChemicalType] = mapped_column(
        SQLAEnum(ChemicalType), nullable=False, index=True
    )
    exposure_limit: Mapped[Optional[float]] = mapped_column(
        Numeric(18, 9), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    warnings: Mapped[List["Warning"]] = relationship("Warning", back_populates="chemical")
    products: Mapped[List["ProductChemical"]] = relationship("ProductChemical", back_populates="chemical")

    def __repr__(self) -> str:
        """
        String representation of the chemical.

        Returns:
            str: Chemical representation
        """
        return f"<Prop65Chemical {self.name} ({self.cas_number})>"


class Warning(Base):
    """
    Warning model.

    Represents warning text for chemicals in products.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        chemical_id: Reference to chemical
        warning_text: Warning text
        last_updated: Last update timestamp
    """
    __tablename__ = "warning"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )
    chemical_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prop65_chemical.id"), nullable=False, index=True
    )
    warning_text: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product")
    chemical: Mapped["Prop65Chemical"] = relationship("Prop65Chemical", back_populates="warnings")

    def __repr__(self) -> str:
        """
        String representation of the warning.

        Returns:
            str: Warning representation
        """
        return f"<Warning for Product {self.product_id} and Chemical {self.chemical_id}>"


class ProductChemical(Base):
    """
    Product chemical association model.

    Represents relationships between products and chemicals,
    including exposure scenarios and warning requirements.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        chemical_id: Reference to chemical
        exposure_scenario: Scenario (Consumer, Occupational, Environmental)
        warning_required: Whether a warning is required
        warning_label: Warning text for label
    """
    __tablename__ = "product_chemical"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )
    chemical_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prop65_chemical.id"), nullable=False, index=True
    )
    exposure_scenario: Mapped[ExposureScenario] = mapped_column(
        SQLAEnum(ExposureScenario), nullable=False
    )
    warning_required: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    warning_label: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product")
    chemical: Mapped["Prop65Chemical"] = relationship("Prop65Chemical", back_populates="products")

    def __repr__(self) -> str:
        """
        String representation of the product chemical association.

        Returns:
            str: Product chemical association representation
        """
        return f"<ProductChemical for Product {self.product_id} and Chemical {self.chemical_id}>"


class ProductDOTApproval(Base):
    """
    Product DOT approval model.

    Represents Department of Transportation approvals for products.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        approval_status: Status (Approved, Pending, Revoked, Not Required)
        approval_number: Official DOT approval number
        approved_by: Entity or agency that approved the product
        approval_date: When the product was approved
        expiration_date: If the approval has an expiration date
        reason: If revoked or pending, store reason
        changed_by_id: User who made the change
        changed_at: When the change occurred
    """
    __tablename__ = "product_dot_approval"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )
    approval_status: Mapped[ApprovalStatus] = mapped_column(
        SQLAEnum(ApprovalStatus), nullable=False, index=True
    )
    approval_number: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, index=True
    )
    approved_by: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    approval_date: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True
    )
    expiration_date: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True
    )
    reason: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )
    changed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=True
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product")
    changed_by: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        """
        String representation of the DOT approval.

        Returns:
            str: DOT approval representation
        """
        return f"<ProductDOTApproval for Product {self.product_id}: {self.approval_status}>"


class HazardousMaterial(Base):
    """
    Hazardous material model.

    Represents hazardous material information for products.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        un_number: UN/NA Number (e.g., 1993 for flammable liquids)
        hazard_class: Hazard Classification (e.g., Flammable Liquid)
        packing_group: Packing Group (I, II, III)
        handling_instructions: Storage or transport precautions
        restricted_transport: Restrictions (Air, Ground, Sea, None)
        created_at: Creation timestamp
    """
    __tablename__ = "hazardous_material"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )
    un_number: Mapped[Optional[str]] = mapped_column(
        String(18), nullable=True, index=True
    )
    hazard_class: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, index=True
    )
    packing_group: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True
    )
    handling_instructions: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )
    restricted_transport: Mapped[TransportRestriction] = mapped_column(
        SQLAEnum(TransportRestriction), default=TransportRestriction.NONE,
        server_default=TransportRestriction.NONE.value, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product")

    def __repr__(self) -> str:
        """
        String representation of the hazardous material.

        Returns:
            str: Hazardous material representation
        """
        return f"<HazardousMaterial for Product {self.product_id}>"
