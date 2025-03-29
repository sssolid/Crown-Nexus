from __future__ import annotations
'PAdb repository implementation.\n\nThis module provides data access and persistence operations for PAdb entities.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.padb.models import PartAttribute, MetaData, MetaUOMCode, PartAttributeAssignment, MetaUomCodeAssignment, ValidValue, ValidValueAssignment, PAdbVersion
class PAdbRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.attribute_repo = PartAttributeRepository(db)
        self.metadata_repo = MetaDataRepository(db)
        self.valid_value_repo = ValidValueRepository(db)
        self.uom_repo = MetaUOMCodeRepository(db)
    async def get_version(self) -> Optional[str]:
        query = select(PAdbVersion).where(PAdbVersion.is_current == True)
        result = await self.db.execute(query)
        version = result.scalars().first()
        if version:
            return version.version_date.strftime('%Y-%m-%d')
        return None
    async def update_version(self, version_date: datetime) -> PAdbVersion:
        await self.db.execute(select(PAdbVersion).where(PAdbVersion.is_current == True).update({PAdbVersion.is_current: False}))
        version = PAdbVersion(version_date=version_date, is_current=True)
        self.db.add(version)
        await self.db.flush()
        return version
    async def get_attributes_for_part(self, part_terminology_id: int) -> List[Dict[str, Any]]:
        query = select(PartAttributeAssignment, PartAttribute, MetaData).join(PartAttribute, PartAttributeAssignment.pa_id == PartAttribute.pa_id).join(MetaData, PartAttributeAssignment.meta_id == MetaData.meta_id).where(PartAttributeAssignment.part_terminology_id == part_terminology_id)
        result = await self.db.execute(query)
        attributes = []
        for assignment, attribute, metadata in result:
            valid_values = await self.valid_value_repo.get_for_attribute_assignment(assignment.papt_id)
            uom_codes = await self.uom_repo.get_for_attribute_assignment(assignment.papt_id)
            attributes.append({'assignment': assignment, 'attribute': attribute, 'metadata': metadata, 'valid_values': valid_values, 'uom_codes': uom_codes})
        return attributes
class PartAttributeRepository(BaseRepository[PartAttribute, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=PartAttribute, db=db)
    async def get_by_pa_id(self, pa_id: int) -> Optional[PartAttribute]:
        query = select(PartAttribute).where(PartAttribute.pa_id == pa_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def search(self, search_term: str, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(PartAttribute).where(PartAttribute.pa_name.ilike(f'%{search_term}%')).order_by(PartAttribute.pa_name)
        return await self.paginate(query, page, page_size)
class MetaDataRepository(BaseRepository[MetaData, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=MetaData, db=db)
    async def get_by_meta_id(self, meta_id: int) -> Optional[MetaData]:
        query = select(MetaData).where(MetaData.meta_id == meta_id)
        result = await self.db.execute(query)
        return result.scalars().first()
class ValidValueRepository(BaseRepository[ValidValue, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=ValidValue, db=db)
    async def get_by_valid_value_id(self, valid_value_id: int) -> Optional[ValidValue]:
        query = select(ValidValue).where(ValidValue.valid_value_id == valid_value_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_for_attribute_assignment(self, papt_id: int) -> List[ValidValue]:
        query = select(ValidValue).join(ValidValueAssignment, ValidValue.valid_value_id == ValidValueAssignment.valid_value_id).where(ValidValueAssignment.papt_id == papt_id).order_by(ValidValue.valid_value)
        result = await self.db.execute(query)
        return list(result.scalars().all())
class MetaUOMCodeRepository(BaseRepository[MetaUOMCode, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=MetaUOMCode, db=db)
    async def get_by_meta_uom_id(self, meta_uom_id: int) -> Optional[MetaUOMCode]:
        query = select(MetaUOMCode).where(MetaUOMCode.meta_uom_id == meta_uom_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_for_attribute_assignment(self, papt_id: int) -> List[MetaUOMCode]:
        query = select(MetaUOMCode).join(MetaUomCodeAssignment, MetaUOMCode.meta_uom_id == MetaUomCodeAssignment.meta_uom_id).where(MetaUomCodeAssignment.papt_id == papt_id).order_by(MetaUOMCode.uom_code)
        result = await self.db.execute(query)
        return list(result.scalars().all())