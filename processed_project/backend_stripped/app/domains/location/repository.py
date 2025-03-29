from __future__ import annotations
'Location repository implementation.\n\nThis module provides data access and persistence operations for Location entities.\n'
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.location.models import Country, Address
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
class CountryRepository(BaseRepository[Country, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Country, db=db)
    async def find_by_iso_code(self, iso_code: str) -> Optional[Country]:
        iso_code = iso_code.upper()
        query = select(Country).where(or_(Country.iso_alpha_2 == iso_code, Country.iso_alpha_3 == iso_code, Country.iso_numeric == iso_code), Country.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def find_by_name(self, name: str) -> List[Country]:
        query = select(Country).where(Country.name.ilike(f'%{name}%'), Country.is_deleted == False).order_by(Country.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_region(self, region: str) -> List[Country]:
        query = select(Country).where(Country.region == region, Country.is_deleted == False).order_by(Country.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_currency(self, currency_code: str) -> List[Country]:
        currency_code = currency_code.upper()
        query = select(Country).where(Country.currency == currency_code, Country.is_deleted == False).order_by(Country.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def ensure_exists(self, country_id: uuid.UUID) -> Country:
        country = await self.get_by_id(country_id)
        if not country:
            raise ResourceNotFoundException(resource_type='Country', resource_id=str(country_id))
        return country
class AddressRepository(BaseRepository[Address, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Address, db=db)
    async def find_by_postal_code(self, postal_code: str, country_id: Optional[uuid.UUID]=None) -> List[Address]:
        conditions = [Address.postal_code == postal_code, Address.is_deleted == False]
        if country_id:
            conditions.append(Address.country_id == country_id)
        query = select(Address).where(and_(*conditions)).order_by(Address.city, Address.street)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def find_by_city(self, city: str, country_id: Optional[uuid.UUID]=None) -> List[Address]:
        conditions = [Address.city.ilike(f'%{city}%'), Address.is_deleted == False]
        if country_id:
            conditions.append(Address.country_id == country_id)
        query = select(Address).where(and_(*conditions)).order_by(Address.postal_code, Address.street)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def search(self, search_term: str, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(Address).where(or_(Address.street.ilike(f'%{search_term}%'), Address.city.ilike(f'%{search_term}%'), Address.state.ilike(f'%{search_term}%'), Address.postal_code.ilike(f'%{search_term}%')), Address.is_deleted == False).order_by(Address.country_id, Address.city, Address.postal_code)
        return await self.paginate(query, page, page_size)
    async def ensure_exists(self, address_id: uuid.UUID) -> Address:
        address = await self.get_by_id(address_id)
        if not address:
            raise ResourceNotFoundException(resource_type='Address', resource_id=str(address_id))
        return address