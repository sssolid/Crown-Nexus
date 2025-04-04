from __future__ import annotations

"""Compliance model definition.

This module defines models for regulatory compliance, hazardous materials,
warnings, and approval statuses for products.
"""

import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, Enum as SQLAEnum, ForeignKey
from sqlalchemy import Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.domains.products.models import Product
    from app.domains.users.models import User


class ChemicalType(str, Enum):
    """Types of chemicals for regulatory compliance.

    Attributes:
        CARCINOGEN: Cancer-causing chemicals.
        REPRODUCTIVE_TOXICANT: Chemicals harmful to reproduction.
        BOTH: Chemicals that are both carcinogenic and reproductive toxicants.
    """

    CARCINOGEN = "Carcinogen"
    REPRODUCTIVE_TOXICANT = "Reproductive Toxicant"
    BOTH = "Both"


class ExposureScenario(str, Enum):
    """Scenarios for potential chemical exposure.

    Attributes:
        CONSUMER: Exposure to general consumers.
        OCCUPATIONAL: Exposure in occupational settings.
        ENVIRONMENTAL: Environmental exposure.
    """

    CONSUMER = "Consumer"
    OCCUPATIONAL = "Occupational"
    ENVIRONMENTAL = "Environmental"


class ApprovalStatus(str, Enum):
    """Status of regulatory approvals.

    Attributes:
        APPROVED: Fully approved.
        PENDING: Approval pending.
        REVOKED: Approval revoked.
        NOT_REQUIRED: Approval not required.
    """

    APPROVED = "Approved"
    PENDING = "Pending"
    REVOKED = "Revoked"
    NOT_REQUIRED = "Not Required"


class TransportRestriction(str, Enum):
    """Restrictions on product transportation methods.

    Attributes:
        NONE: No restrictions.
        AIR: Air transport restricted.
        GROUND: Ground transport restricted.
        SEA: Sea transport restricted.
        ALL: All transport methods restricted.
    """

    NONE = "NONE"
    AIR = "AIR"
    GROUND = "GROUND"
    SEA = "SEA"
    ALL = "ALL"


class Prop65Chemical(Base):
    """California Proposition 65 chemical entity.

    Attributes:
        id: Unique identifier.
        name: Chemical name.
        cas_number: CAS Registry Number (unique chemical identifier).
        type: Type of chemical hazard.
        exposure_limit: Safe harbor exposure limit if applicable.
        updated_at: Last update timestamp.
    """

    __tablename__ = "prop65_chemical"
    __table_args__ = {"schema": "compliance"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
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
    warnings: Mapped[List["Warning"]] = relationship(
        "Warning", back_populates="chemical"
    )
    products: Mapped[List["ProductChemical"]] = relationship(
        "ProductChemical", back_populates="chemical"
    )

    def __repr__(self) -> str:
        """Return string representation of Prop65Chemical instance.

        Returns:
            String representation including name and CAS number.
        """
        return f"<Prop65Chemical {self.name} ({self.cas_number})>"


class Warning(Base):
    """Warning entity for products containing regulated chemicals.

    Attributes:
        id: Unique identifier.
        product_id: ID of the product requiring the warning.
        chemical_id: ID of the chemical in the warning.
        warning_text: Text of the warning label.
        last_updated: Last update timestamp.
    """

    __tablename__ = "warning"
    __table_args__ = {"schema": "compliance"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False, index=True
    )
    chemical_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("compliance.prop65_chemical.id"), nullable=False, index=True
    )
    warning_text: Mapped[str] = mapped_column(Text, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product")
    chemical: Mapped["Prop65Chemical"] = relationship(
        "Prop65Chemical", back_populates="warnings"
    )

    def __repr__(self) -> str:
        """Return string representation of Warning instance.

        Returns:
            String representation including product ID and chemical ID.
        """
        return (
            f"<Warning for Product {self.product_id} and Chemical {self.chemical_id}>"
        )


class ProductChemical(Base):
    """Product-chemical association entity.

    Attributes:
        id: Unique identifier.
        product_id: ID of the product containing the chemical.
        chemical_id: ID of the chemical in the product.
        exposure_scenario: Type of exposure scenario.
        warning_required: Whether a warning label is required.
        warning_label: Text of the required warning label if applicable.
    """

    __tablename__ = "product_chemical"
    __table_args__ = {"schema": "compliance"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False, index=True
    )
    chemical_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("compliance.prop65_chemical.id"), nullable=False, index=True
    )
    exposure_scenario: Mapped[ExposureScenario] = mapped_column(
        SQLAEnum(ExposureScenario), nullable=False
    )
    warning_required: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    warning_label: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product")
    chemical: Mapped["Prop65Chemical"] = relationship(
        "Prop65Chemical", back_populates="products"
    )

    def __repr__(self) -> str:
        """Return string representation of ProductChemical instance.

        Returns:
            String representation including product ID and chemical ID.
        """
        return f"<ProductChemical for Product {self.product_id} and Chemical {self.chemical_id}>"


class ProductDOTApproval(Base):
    """Department of Transportation approval entity for products.

    Attributes:
        id: Unique identifier.
        product_id: ID of the approved product.
        approval_status: Status of the approval.
        approval_number: DOT approval number if applicable.
        approved_by: Name of the approver.
        approval_date: Date of approval.
        expiration_date: Expiration date of the approval.
        reason: Reason for the approval status.
        changed_by_id: ID of the user who last changed the approval.
        changed_at: When the approval was last changed.
    """

    __tablename__ = "product_dot_approval"
    __table_args__ = {"schema": "compliance"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False, index=True
    )
    approval_status: Mapped[ApprovalStatus] = mapped_column(
        SQLAEnum(ApprovalStatus), nullable=False, index=True
    )
    approval_number: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, index=True
    )
    approved_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    approval_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    expiration_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    changed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user.id"), nullable=True
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product")
    changed_by: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        """Return string representation of ProductDOTApproval instance.

        Returns:
            String representation including product ID and approval status.
        """
        return f"<ProductDOTApproval for Product {self.product_id}: {self.approval_status}>"


class HazardousMaterial(Base):
    """Hazardous material information entity for products.

    Attributes:
        id: Unique identifier.
        product_id: ID of the hazardous product.
        un_number: UN number for hazardous material.
        hazard_class: DOT hazard class.
        packing_group: Packing group (I, II, III).
        handling_instructions: Special handling instructions.
        restricted_transport: Transport restrictions.
        created_at: Creation timestamp.
    """

    __tablename__ = "hazardous_material"
    __table_args__ = {"schema": "compliance"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False, index=True
    )
    un_number: Mapped[Optional[str]] = mapped_column(
        String(18), nullable=True, index=True
    )
    hazard_class: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, index=True
    )
    packing_group: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    handling_instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    restricted_transport: Mapped[TransportRestriction] = mapped_column(
        SQLAEnum(TransportRestriction),
        default=TransportRestriction.NONE,
        server_default=TransportRestriction.NONE.value,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product")

    def __repr__(self) -> str:
        """Return string representation of HazardousMaterial instance.

        Returns:
            String representation including product ID.
        """
        return f"<HazardousMaterial for Product {self.product_id}>"
