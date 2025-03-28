from __future__ import annotations
'Model mapping repository implementation.\n\nThis module provides data access and persistence operations for ModelMapping entities.\n'
import re
from typing import List, Optional, Dict, Any
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.model_mapping.models import ModelMapping
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
class ModelMappingRepository(BaseRepository[ModelMapping, int]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=ModelMapping, db=db)
    async def find_by_pattern(self, pattern: str) -> List[ModelMapping]:
        query = select(ModelMapping).where(ModelMapping.pattern.ilike(f'%{pattern}%'), ModelMapping.active == True, ModelMapping.is_deleted == False).order_by(desc(ModelMapping.priority), ModelMapping.pattern)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def find_by_make_model(self, make: str, model: str) -> List[ModelMapping]:
        query = select(ModelMapping).where(ModelMapping.active == True, ModelMapping.is_deleted == False, func.split_part(ModelMapping.mapping, '|', 1).ilike(f'%{make}%'), func.split_part(ModelMapping.mapping, '|', 3).ilike(f'%{model}%')).order_by(desc(ModelMapping.priority))
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def match_vehicle_string(self, vehicle_string: str) -> Optional[Dict[str, str]]:
        query = select(ModelMapping).where(ModelMapping.active == True, ModelMapping.is_deleted == False).order_by(desc(ModelMapping.priority))
        result = await self.db.execute(query)
        mappings = list(result.scalars().all())
        for mapping in mappings:
            pattern = mapping.pattern
            if re.search(pattern, vehicle_string, re.IGNORECASE):
                parts = mapping.mapping.split('|')
                return {'make': parts[0] if len(parts) > 0 else '', 'code': parts[1] if len(parts) > 1 else '', 'model': parts[2] if len(parts) > 2 else ''}
        return None
    async def get_by_make(self, make: str) -> List[ModelMapping]:
        query = select(ModelMapping).where(ModelMapping.active == True, ModelMapping.is_deleted == False, func.split_part(ModelMapping.mapping, '|', 1).ilike(f'%{make}%')).order_by(func.split_part(ModelMapping.mapping, '|', 3))
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_active_mappings(self, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(ModelMapping).where(ModelMapping.active == True, ModelMapping.is_deleted == False).order_by(desc(ModelMapping.priority), ModelMapping.pattern)
        return await self.paginate(query, page, page_size)
    async def ensure_exists(self, mapping_id: int) -> ModelMapping:
        mapping = await self.get_by_id(mapping_id)
        if not mapping:
            raise ResourceNotFoundException(resource_type='ModelMapping', resource_id=str(mapping_id))
        return mapping