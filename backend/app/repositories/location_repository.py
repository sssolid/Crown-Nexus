from __future__ import annotations

"""Location repository implementation.

This module provides data access and persistence operations for Location entities.
"""

import uuid
from typing import List, Optional, Dict, Any

from sqlalchemy import select, and_, or_, func, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.models.location import Country, Address
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException


class CountryRepository(BaseRepository[Country, uuid.UUID]):
    """Repository for Country entity operations.

    Provides methods for querying, creating, updating, and deleting
    Country entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the country repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Country, db=db)

    async def find_by_iso_code(self, iso_code: str) -> Optional[Country]:
        """Find a country by ISO code (alpha-2 or alpha-3).

        Args:
            iso_code: The ISO code to search for.

        Returns:
            The country if found, None otherwise.
        """
        iso_code = iso_code.upper()
        query = select(Country).where(
            or_(
                Country.iso_alpha_2 == iso_code,
                Country.iso_alpha_3 == iso_code,
                Country.iso_numeric == iso_code,
            ),
            Country.is_deleted == False,
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_name(self, name: str) -> List[Country]:
        """Find countries by name (partial match).

        Args:
            name: The country name to search for.

        Returns:
            List of countries with matching names.
        """
        query = (
            select(Country)
            .where(Country.name.ilike(f"%{name}%"), Country.is_deleted == False)
            .order_by(Country.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_region(self, region: str) -> List[Country]:
        """Get countries in a specific region.

        Args:
            region: The region to filter by.

        Returns:
            List of countries in the specified region.
        """
        query = (
            select(Country)
            .where(Country.region == region, Country.is_deleted == False)
            .order_by(Country.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_currency(self, currency_code: str) -> List[Country]:
        """Get countries using a specific currency.

        Args:
            currency_code: The ISO 4217 currency code.

        Returns:
            List of countries using the specified currency.
        """
        currency_code = currency_code.upper()
        query = (
            select(Country)
            .where(Country.currency == currency_code, Country.is_deleted == False)
            .order_by(Country.name)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def ensure_exists(self, country_id: uuid.UUID) -> Country:
        """Ensure a country exists by ID, raising an exception if not found.

        Args:
            country_id: The country ID to check.

        Returns:
            The country if found.

        Raises:
            ResourceNotFoundException: If the country is not found.
        """
        country = await self.get_by_id(country_id)
        if not country:
            raise ResourceNotFoundException(
                resource_type="Country", resource_id=str(country_id)
            )
        return country


class AddressRepository(BaseRepository[Address, uuid.UUID]):
    """Repository for Address entity operations.

    Provides methods for querying, creating, updating, and deleting
    Address entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the address repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Address, db=db)

    async def find_by_postal_code(
        self, postal_code: str, country_id: Optional[uuid.UUID] = None
    ) -> List[Address]:
        """Find addresses by postal code.

        Args:
            postal_code: The postal code to search for.
            country_id: Optional country ID to restrict search.

        Returns:
            List of addresses with matching postal code.
        """
        conditions = [Address.postal_code == postal_code, Address.is_deleted == False]

        if country_id:
            conditions.append(Address.country_id == country_id)

        query = (
            select(Address)
            .where(and_(*conditions))
            .order_by(Address.city, Address.street)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def find_by_city(
        self, city: str, country_id: Optional[uuid.UUID] = None
    ) -> List[Address]:
        """Find addresses by city.

        Args:
            city: The city name to search for.
            country_id: Optional country ID to restrict search.

        Returns:
            List of addresses in the specified city.
        """
        conditions = [Address.city.ilike(f"%{city}%"), Address.is_deleted == False]

        if country_id:
            conditions.append(Address.country_id == country_id)

        query = (
            select(Address)
            .where(and_(*conditions))
            .order_by(Address.postal_code, Address.street)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def search(
        self, search_term: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Search addresses by various fields.

        Args:
            search_term: The term to search for.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(Address)
            .where(
                or_(
                    Address.street.ilike(f"%{search_term}%"),
                    Address.city.ilike(f"%{search_term}%"),
                    Address.state.ilike(f"%{search_term}%"),
                    Address.postal_code.ilike(f"%{search_term}%"),
                ),
                Address.is_deleted == False,
            )
            .order_by(Address.country_id, Address.city, Address.postal_code)
        )

        return await self.paginate(query, page, page_size)

    async def ensure_exists(self, address_id: uuid.UUID) -> Address:
        """Ensure an address exists by ID, raising an exception if not found.

        Args:
            address_id: The address ID to check.

        Returns:
            The address if found.

        Raises:
            ResourceNotFoundException: If the address is not found.
        """
        address = await self.get_by_id(address_id)
        if not address:
            raise ResourceNotFoundException(
                resource_type="Address", resource_id=str(address_id)
            )
        return address
