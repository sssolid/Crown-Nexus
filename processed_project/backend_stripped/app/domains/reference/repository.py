from __future__ import annotations
'Reference repository implementation.\n\nThis module provides data access and persistence operations for reference entities.\n'
import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.reference.models import Color, TariffCode, UnspscCode, Warehouse
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
class ColorRepository(BaseRepository[Color, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Color, db=db)
    async def find_by_name(self, name: str) -> Optional[Color]:
        query = select(Color).where(Color.name.ilike(name), Color.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def find_by_hex(self, hex_code: str) -> Optional[Color]:
        if hex_code and (not hex_code.startswith('#')):
            hex_code = f'#{hex_code}'
        query = select(Color).where(Color.hex_code == hex_code, Color.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def ensure_exists(self, color_id: uuid.UUID) -> Color:
        color = await self.get_by_id(color_id)
        if not color:
            raise ResourceNotFoundException(resource_type='Color', resource_id=str(color_id))
        return color
class WarehouseRepository(BaseRepository[Warehouse, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Warehouse, db=db)
    async def find_by_name(self, name: str) -> Optional[Warehouse]:
        query = select(Warehouse).where(Warehouse.name.ilike(name), Warehouse.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_active_warehouses(self) -> List[Warehouse]:
        query = select(Warehouse).where(Warehouse.is_active == True, Warehouse.is_deleted == False).order_by(Warehouse.name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def ensure_exists(self, warehouse_id: uuid.UUID) -> Warehouse:
        warehouse = await self.get_by_id(warehouse_id)
        if not warehouse:
            raise ResourceNotFoundException(resource_type='Warehouse', resource_id=str(warehouse_id))
        return warehouse
class TariffCodeRepository(BaseRepository[TariffCode, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=TariffCode, db=db)
    async def find_by_code(self, code: str) -> List[TariffCode]:
        query = select(TariffCode).where(TariffCode.code.ilike(f'%{code}%'), TariffCode.is_deleted == False).order_by(TariffCode.code)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_country(self, country_id: uuid.UUID) -> List[TariffCode]:
        query = select(TariffCode).where(TariffCode.country_id == country_id, TariffCode.is_deleted == False).order_by(TariffCode.code)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def ensure_exists(self, tariff_code_id: uuid.UUID) -> TariffCode:
        tariff_code = await self.get_by_id(tariff_code_id)
        if not tariff_code:
            raise ResourceNotFoundException(resource_type='TariffCode', resource_id=str(tariff_code_id))
        return tariff_code
class UnspscCodeRepository(BaseRepository[UnspscCode, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=UnspscCode, db=db)
    async def find_by_code(self, code: str) -> Optional[UnspscCode]:
        query = select(UnspscCode).where(UnspscCode.code == code, UnspscCode.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def find_by_segment(self, segment: str) -> List[UnspscCode]:
        query = select(UnspscCode).where(UnspscCode.segment.ilike(f'%{segment}%'), UnspscCode.is_deleted == False).order_by(UnspscCode.code)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def find_by_description(self, description: str) -> List[UnspscCode]:
        query = select(UnspscCode).where(UnspscCode.description.ilike(f'%{description}%'), UnspscCode.is_deleted == False).order_by(UnspscCode.code)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def ensure_exists(self, unspsc_code_id: uuid.UUID) -> UnspscCode:
        unspsc_code = await self.get_by_id(unspsc_code_id)
        if not unspsc_code:
            raise ResourceNotFoundException(resource_type='UnspscCode', resource_id=str(unspsc_code_id))
        return unspsc_code