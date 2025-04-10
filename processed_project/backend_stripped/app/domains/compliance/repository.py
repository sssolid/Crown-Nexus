from __future__ import annotations
'Compliance repository implementation.\n\nThis module provides data access and persistence operations for Compliance entities.\n'
import uuid
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.compliance.models import Prop65Chemical, Warning, ProductChemical, ProductDOTApproval, HazardousMaterial, ApprovalStatus, ChemicalType, ExposureScenario
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
class Prop65ChemicalRepository(BaseRepository[Prop65Chemical, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Prop65Chemical, db=db)
    async def find_by_cas_number(self, cas_number: str) -> Optional[Prop65Chemical]:
        query = select(Prop65Chemical).where(Prop65Chemical.cas_number == cas_number, Prop65Chemical.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def find_by_name(self, name: str) -> List[Prop65Chemical]:
        query = select(Prop65Chemical).where(Prop65Chemical.name.ilike(f'%{name}%'), Prop65Chemical.is_deleted == False).order_by(Prop65Chemical.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_type(self, chemical_type: ChemicalType) -> List[Prop65Chemical]:
        query = select(Prop65Chemical).where(Prop65Chemical.type == chemical_type, Prop65Chemical.is_deleted == False).order_by(Prop65Chemical.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def ensure_exists(self, chemical_id: uuid.UUID) -> Prop65Chemical:
        chemical = await self.get_by_id(chemical_id)
        if not chemical:
            raise ResourceNotFoundException(resource_type='Prop65Chemical', resource_id=str(chemical_id))
        return chemical
class WarningRepository(BaseRepository[Warning, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Warning, db=db)
    async def get_by_product(self, product_id: uuid.UUID) -> List[Warning]:
        query = select(Warning).where(Warning.product_id == product_id, Warning.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_chemical(self, chemical_id: uuid.UUID) -> List[Warning]:
        query = select(Warning).where(Warning.chemical_id == chemical_id, Warning.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def ensure_exists(self, warning_id: uuid.UUID) -> Warning:
        warning = await self.get_by_id(warning_id)
        if not warning:
            raise ResourceNotFoundException(resource_type='Warning', resource_id=str(warning_id))
        return warning
class ProductChemicalRepository(BaseRepository[ProductChemical, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=ProductChemical, db=db)
    async def find_by_product_and_chemical(self, product_id: uuid.UUID, chemical_id: uuid.UUID) -> Optional[ProductChemical]:
        query = select(ProductChemical).where(ProductChemical.product_id == product_id, ProductChemical.chemical_id == chemical_id, ProductChemical.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_product(self, product_id: uuid.UUID) -> List[ProductChemical]:
        query = select(ProductChemical).where(ProductChemical.product_id == product_id, ProductChemical.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_exposure_scenario(self, scenario: ExposureScenario) -> List[ProductChemical]:
        query = select(ProductChemical).where(ProductChemical.exposure_scenario == scenario, ProductChemical.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_products_with_warnings(self) -> List[uuid.UUID]:
        query = select(ProductChemical.product_id).distinct().where(ProductChemical.warning_required == True, ProductChemical.is_deleted == False)
        result = await self.db.execute(query)
        return [row[0] for row in result.all()]
    async def ensure_exists(self, association_id: uuid.UUID) -> ProductChemical:
        association = await self.get_by_id(association_id)
        if not association:
            raise ResourceNotFoundException(resource_type='ProductChemical', resource_id=str(association_id))
        return association
class ProductDOTApprovalRepository(BaseRepository[ProductDOTApproval, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=ProductDOTApproval, db=db)
    async def find_by_product(self, product_id: uuid.UUID) -> Optional[ProductDOTApproval]:
        query = select(ProductDOTApproval).where(ProductDOTApproval.product_id == product_id, ProductDOTApproval.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def find_by_approval_number(self, approval_number: str) -> Optional[ProductDOTApproval]:
        query = select(ProductDOTApproval).where(ProductDOTApproval.approval_number == approval_number, ProductDOTApproval.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_status(self, status: ApprovalStatus) -> List[ProductDOTApproval]:
        query = select(ProductDOTApproval).where(ProductDOTApproval.approval_status == status, ProductDOTApproval.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_expiring_soon(self, days: int=30) -> List[ProductDOTApproval]:
        today = date.today()
        expiry_cutoff = today + datetime.timedelta(days=days)
        query = select(ProductDOTApproval).where(ProductDOTApproval.expiration_date <= expiry_cutoff, ProductDOTApproval.expiration_date >= today, ProductDOTApproval.approval_status == ApprovalStatus.APPROVED, ProductDOTApproval.is_deleted == False).order_by(ProductDOTApproval.expiration_date)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def ensure_exists(self, approval_id: uuid.UUID) -> ProductDOTApproval:
        approval = await self.get_by_id(approval_id)
        if not approval:
            raise ResourceNotFoundException(resource_type='ProductDOTApproval', resource_id=str(approval_id))
        return approval
class HazardousMaterialRepository(BaseRepository[HazardousMaterial, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=HazardousMaterial, db=db)
    async def find_by_product(self, product_id: uuid.UUID) -> Optional[HazardousMaterial]:
        query = select(HazardousMaterial).where(HazardousMaterial.product_id == product_id, HazardousMaterial.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def find_by_un_number(self, un_number: str) -> List[HazardousMaterial]:
        query = select(HazardousMaterial).where(HazardousMaterial.un_number == un_number, HazardousMaterial.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_hazard_class(self, hazard_class: str) -> List[HazardousMaterial]:
        query = select(HazardousMaterial).where(HazardousMaterial.hazard_class == hazard_class, HazardousMaterial.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def ensure_exists(self, hazmat_id: uuid.UUID) -> HazardousMaterial:
        hazmat = await self.get_by_id(hazmat_id)
        if not hazmat:
            raise ResourceNotFoundException(resource_type='HazardousMaterial', resource_id=str(hazmat_id))
        return hazmat