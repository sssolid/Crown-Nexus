from __future__ import annotations
'Company repository implementation.\n\nThis module provides data access and persistence operations for Company entities.\n'
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.company.schemas import Company
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
class CompanyRepository(BaseRepository[Company, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Company, db=db)
    async def find_by_name(self, name: str) -> Optional[Company]:
        query = select(Company).where(Company.name == name, Company.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def find_by_account_number(self, account_number: str) -> Optional[Company]:
        query = select(Company).where(Company.account_number == account_number, Company.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def find_by_industry(self, industry: str) -> List[Company]:
        query = select(Company).where(Company.industry == industry, Company.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_active_companies(self, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(Company).where(Company.is_active == True, Company.is_deleted == False).order_by(Company.name)
        return await self.paginate(query, page, page_size)
    async def ensure_exists(self, company_id: uuid.UUID) -> Company:
        company = await self.get_by_id(company_id)
        if not company:
            raise ResourceNotFoundException(resource_type='Company', resource_id=str(company_id))
        return company