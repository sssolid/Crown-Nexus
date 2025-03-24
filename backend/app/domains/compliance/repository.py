from __future__ import annotations

"""Compliance repository implementation.

This module provides data access and persistence operations for Compliance entities.
"""

import uuid
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.compliance.models import (
    Prop65Chemical,
    Warning,
    ProductChemical,
    ProductDOTApproval,
    HazardousMaterial,
    ApprovalStatus,
    ChemicalType,
    ExposureScenario,
)
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException


class Prop65ChemicalRepository(BaseRepository[Prop65Chemical, uuid.UUID]):
    """Repository for Prop65Chemical entity operations.

    Provides methods for querying, creating, updating, and deleting
    Prop65Chemical entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the Prop65Chemical repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Prop65Chemical, db=db)

    async def find_by_cas_number(self, cas_number: str) -> Optional[Prop65Chemical]:
        """Find a chemical by its CAS number.

        Args:
            cas_number: The CAS number to search for.

        Returns:
            The chemical if found, None otherwise.
        """
        query = select(Prop65Chemical).where(
            Prop65Chemical.cas_number == cas_number, Prop65Chemical.is_deleted == False
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_name(self, name: str) -> List[Prop65Chemical]:
        """Find chemicals by name (partial match).

        Args:
            name: The chemical name to search for.

        Returns:
            List of chemicals with matching names.
        """
        query = (
            select(Prop65Chemical)
            .where(
                Prop65Chemical.name.ilike(f"%{name}%"),
                Prop65Chemical.is_deleted == False,
            )
            .order_by(Prop65Chemical.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_type(self, chemical_type: ChemicalType) -> List[Prop65Chemical]:
        """Get chemicals of a specific type.

        Args:
            chemical_type: The chemical type to filter by.

        Returns:
            List of chemicals of the specified type.
        """
        query = (
            select(Prop65Chemical)
            .where(
                Prop65Chemical.type == chemical_type, Prop65Chemical.is_deleted == False
            )
            .order_by(Prop65Chemical.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def ensure_exists(self, chemical_id: uuid.UUID) -> Prop65Chemical:
        """Ensure a chemical exists by ID, raising an exception if not found.

        Args:
            chemical_id: The chemical ID to check.

        Returns:
            The chemical if found.

        Raises:
            ResourceNotFoundException: If the chemical is not found.
        """
        chemical = await self.get_by_id(chemical_id)
        if not chemical:
            raise ResourceNotFoundException(
                resource_type="Prop65Chemical", resource_id=str(chemical_id)
            )
        return chemical


class WarningRepository(BaseRepository[Warning, uuid.UUID]):
    """Repository for Warning entity operations.

    Provides methods for querying, creating, updating, and deleting
    Warning entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the Warning repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Warning, db=db)

    async def get_by_product(self, product_id: uuid.UUID) -> List[Warning]:
        """Get warnings for a specific product.

        Args:
            product_id: The product ID to filter by.

        Returns:
            List of warnings for the product.
        """
        query = select(Warning).where(
            Warning.product_id == product_id, Warning.is_deleted == False
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_chemical(self, chemical_id: uuid.UUID) -> List[Warning]:
        """Get warnings for a specific chemical.

        Args:
            chemical_id: The chemical ID to filter by.

        Returns:
            List of warnings for the chemical.
        """
        query = select(Warning).where(
            Warning.chemical_id == chemical_id, Warning.is_deleted == False
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def ensure_exists(self, warning_id: uuid.UUID) -> Warning:
        """Ensure a warning exists by ID, raising an exception if not found.

        Args:
            warning_id: The warning ID to check.

        Returns:
            The warning if found.

        Raises:
            ResourceNotFoundException: If the warning is not found.
        """
        warning = await self.get_by_id(warning_id)
        if not warning:
            raise ResourceNotFoundException(
                resource_type="Warning", resource_id=str(warning_id)
            )
        return warning


class ProductChemicalRepository(BaseRepository[ProductChemical, uuid.UUID]):
    """Repository for ProductChemical entity operations.

    Provides methods for querying, creating, updating, and deleting
    ProductChemical entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the ProductChemical repository.

        Args:
            db: The database session.
        """
        super().__init__(model=ProductChemical, db=db)

    async def find_by_product_and_chemical(
        self, product_id: uuid.UUID, chemical_id: uuid.UUID
    ) -> Optional[ProductChemical]:
        """Find a product chemical association by product and chemical IDs.

        Args:
            product_id: The product ID.
            chemical_id: The chemical ID.

        Returns:
            The product chemical association if found, None otherwise.
        """
        query = select(ProductChemical).where(
            ProductChemical.product_id == product_id,
            ProductChemical.chemical_id == chemical_id,
            ProductChemical.is_deleted == False,
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_product(self, product_id: uuid.UUID) -> List[ProductChemical]:
        """Get chemical associations for a specific product.

        Args:
            product_id: The product ID to filter by.

        Returns:
            List of product chemical associations for the product.
        """
        query = select(ProductChemical).where(
            ProductChemical.product_id == product_id,
            ProductChemical.is_deleted == False,
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_exposure_scenario(
        self, scenario: ExposureScenario
    ) -> List[ProductChemical]:
        """Get product chemical associations with a specific exposure scenario.

        Args:
            scenario: The exposure scenario to filter by.

        Returns:
            List of product chemical associations with the specified scenario.
        """
        query = select(ProductChemical).where(
            ProductChemical.exposure_scenario == scenario,
            ProductChemical.is_deleted == False,
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_products_with_warnings(self) -> List[uuid.UUID]:
        """Get IDs of products that require warnings.

        Returns:
            List of product IDs that require warnings.
        """
        query = (
            select(ProductChemical.product_id)
            .distinct()
            .where(
                ProductChemical.warning_required == True,
                ProductChemical.is_deleted == False,
            )
        )

        result = await self.db.execute(query)
        return [row[0] for row in result.all()]

    async def ensure_exists(self, association_id: uuid.UUID) -> ProductChemical:
        """Ensure a product chemical association exists by ID, raising an exception if not found.

        Args:
            association_id: The association ID to check.

        Returns:
            The product chemical association if found.

        Raises:
            ResourceNotFoundException: If the association is not found.
        """
        association = await self.get_by_id(association_id)
        if not association:
            raise ResourceNotFoundException(
                resource_type="ProductChemical", resource_id=str(association_id)
            )
        return association


class ProductDOTApprovalRepository(BaseRepository[ProductDOTApproval, uuid.UUID]):
    """Repository for ProductDOTApproval entity operations.

    Provides methods for querying, creating, updating, and deleting
    ProductDOTApproval entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the ProductDOTApproval repository.

        Args:
            db: The database session.
        """
        super().__init__(model=ProductDOTApproval, db=db)

    async def find_by_product(
        self, product_id: uuid.UUID
    ) -> Optional[ProductDOTApproval]:
        """Find a DOT approval for a specific product.

        Args:
            product_id: The product ID.

        Returns:
            The DOT approval if found, None otherwise.
        """
        query = select(ProductDOTApproval).where(
            ProductDOTApproval.product_id == product_id,
            ProductDOTApproval.is_deleted == False,
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_approval_number(
        self, approval_number: str
    ) -> Optional[ProductDOTApproval]:
        """Find a DOT approval by approval number.

        Args:
            approval_number: The approval number to search for.

        Returns:
            The DOT approval if found, None otherwise.
        """
        query = select(ProductDOTApproval).where(
            ProductDOTApproval.approval_number == approval_number,
            ProductDOTApproval.is_deleted == False,
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_status(self, status: ApprovalStatus) -> List[ProductDOTApproval]:
        """Get DOT approvals with a specific status.

        Args:
            status: The approval status to filter by.

        Returns:
            List of DOT approvals with the specified status.
        """
        query = select(ProductDOTApproval).where(
            ProductDOTApproval.approval_status == status,
            ProductDOTApproval.is_deleted == False,
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_expiring_soon(self, days: int = 30) -> List[ProductDOTApproval]:
        """Get DOT approvals that are expiring soon.

        Args:
            days: Number of days to consider "soon".

        Returns:
            List of DOT approvals expiring within the specified number of days.
        """
        today = date.today()
        expiry_cutoff = today + datetime.timedelta(days=days)

        query = (
            select(ProductDOTApproval)
            .where(
                ProductDOTApproval.expiration_date <= expiry_cutoff,
                ProductDOTApproval.expiration_date >= today,
                ProductDOTApproval.approval_status == ApprovalStatus.APPROVED,
                ProductDOTApproval.is_deleted == False,
            )
            .order_by(ProductDOTApproval.expiration_date)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def ensure_exists(self, approval_id: uuid.UUID) -> ProductDOTApproval:
        """Ensure a DOT approval exists by ID, raising an exception if not found.

        Args:
            approval_id: The approval ID to check.

        Returns:
            The DOT approval if found.

        Raises:
            ResourceNotFoundException: If the approval is not found.
        """
        approval = await self.get_by_id(approval_id)
        if not approval:
            raise ResourceNotFoundException(
                resource_type="ProductDOTApproval", resource_id=str(approval_id)
            )
        return approval


class HazardousMaterialRepository(BaseRepository[HazardousMaterial, uuid.UUID]):
    """Repository for HazardousMaterial entity operations.

    Provides methods for querying, creating, updating, and deleting
    HazardousMaterial entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the HazardousMaterial repository.

        Args:
            db: The database session.
        """
        super().__init__(model=HazardousMaterial, db=db)

    async def find_by_product(
        self, product_id: uuid.UUID
    ) -> Optional[HazardousMaterial]:
        """Find hazardous material information for a specific product.

        Args:
            product_id: The product ID.

        Returns:
            The hazardous material information if found, None otherwise.
        """
        query = select(HazardousMaterial).where(
            HazardousMaterial.product_id == product_id,
            HazardousMaterial.is_deleted == False,
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_un_number(self, un_number: str) -> List[HazardousMaterial]:
        """Find hazardous materials by UN number.

        Args:
            un_number: The UN number to search for.

        Returns:
            List of hazardous materials with the specified UN number.
        """
        query = select(HazardousMaterial).where(
            HazardousMaterial.un_number == un_number,
            HazardousMaterial.is_deleted == False,
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_hazard_class(self, hazard_class: str) -> List[HazardousMaterial]:
        """Get hazardous materials with a specific hazard class.

        Args:
            hazard_class: The hazard class to filter by.

        Returns:
            List of hazardous materials with the specified hazard class.
        """
        query = select(HazardousMaterial).where(
            HazardousMaterial.hazard_class == hazard_class,
            HazardousMaterial.is_deleted == False,
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def ensure_exists(self, hazmat_id: uuid.UUID) -> HazardousMaterial:
        """Ensure hazardous material information exists by ID, raising an exception if not found.

        Args:
            hazmat_id: The hazardous material ID to check.

        Returns:
            The hazardous material information if found.

        Raises:
            ResourceNotFoundException: If the information is not found.
        """
        hazmat = await self.get_by_id(hazmat_id)
        if not hazmat:
            raise ResourceNotFoundException(
                resource_type="HazardousMaterial", resource_id=str(hazmat_id)
            )
        return hazmat
