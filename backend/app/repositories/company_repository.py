from __future__ import annotations

"""Company repository implementation.

This module provides data access and persistence operations for Company entities.
"""

import uuid
from typing import List, Optional, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException


class CompanyRepository(BaseRepository[Company, uuid.UUID]):
    """Repository for Company entity operations.

    Provides methods for querying, creating, updating, and deleting
    Company entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the company repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Company, db=db)

    async def find_by_name(self, name: str) -> Optional[Company]:
        """Find a company by its name.

        Args:
            name: The company name to search for.

        Returns:
            The company if found, None otherwise.
        """
        query = select(Company).where(Company.name == name, Company.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_account_number(self, account_number: str) -> Optional[Company]:
        """Find a company by its account number.

        Args:
            account_number: The account number to search for.

        Returns:
            The company if found, None otherwise.
        """
        query = select(Company).where(
            Company.account_number == account_number, Company.is_deleted == False
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_industry(self, industry: str) -> List[Company]:
        """Find companies by industry.

        Args:
            industry: The industry to filter by.

        Returns:
            List of companies in the specified industry.
        """
        query = select(Company).where(
            Company.industry == industry, Company.is_deleted == False
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_active_companies(
        self, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated list of active companies.

        Args:
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(Company)
            .where(Company.is_active == True, Company.is_deleted == False)
            .order_by(Company.name)
        )

        return await self.paginate(query, page, page_size)

    async def ensure_exists(self, company_id: uuid.UUID) -> Company:
        """Ensure a company exists by ID, raising an exception if not found.

        Args:
            company_id: The company ID to check.

        Returns:
            The company if found.

        Raises:
            ResourceNotFoundException: If the company is not found.
        """
        company = await self.get_by_id(company_id)
        if not company:
            raise ResourceNotFoundException(
                resource_type="Company", resource_id=str(company_id)
            )
        return company
