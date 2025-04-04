from __future__ import annotations
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DatabaseException
from app.logging import get_logger
from app.db.base_class import Base
from app.db.utils import bulk_create, count_query, create_object, delete_object, get_by_id, get_by_ids, paginate, update_object, upsert
logger = get_logger('app.repositories.base')
T = TypeVar('T', bound=Base)
ID = TypeVar('ID')
class BaseRepository(Generic[T, ID]):
    def __init__(self, model: Type[T], db: AsyncSession) -> None:
        self.model = model
        self.db = db
    async def get_by_id(self, id_value: ID) -> Optional[T]:
        return await get_by_id(self.db, self.model, id_value)
    async def get_by_ids(self, ids: List[ID]) -> List[T]:
        return await get_by_ids(self.db, self.model, ids)
    async def get_all(self, page: int=1, page_size: int=100, order_by: Optional[str]=None, filters: Optional[Dict[str, Any]]=None) -> Dict[str, Any]:
        query = self.model.active_only()
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        if order_by:
            is_desc = order_by.startswith('-')
            field_name = order_by[1:] if is_desc else order_by
            if hasattr(self.model, field_name):
                field = getattr(self.model, field_name)
                query = query.order_by(field.desc() if is_desc else field)
        return await paginate(self.db, query, page, page_size)
    async def count(self, filters: Optional[Dict[str, Any]]=None) -> int:
        query = self.model.active_only()
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        return await count_query(self.db, query)
    async def create(self, data: Dict[str, Any]) -> T:
        return await create_object(self.db, self.model, data)
    async def update(self, id_value: ID, data: Dict[str, Any], user_id: Optional[Any]=None) -> Optional[T]:
        return await update_object(self.db, self.model, id_value, data, user_id)
    async def delete(self, id_value: ID, user_id: Optional[Any]=None, hard_delete: bool=False) -> bool:
        return await delete_object(self.db, self.model, id_value, user_id, hard_delete)
    async def bulk_create(self, items: List[Dict[str, Any]]) -> List[T]:
        return await bulk_create(self.db, self.model, items)
    async def upsert(self, data: Dict[str, Any], unique_fields: List[str]) -> T:
        return await upsert(self.db, self.model, data, unique_fields)
    async def exists(self, filters: Dict[str, Any]) -> bool:
        count = await self.count(filters)
        return count > 0
    async def find_one_by(self, filters: Dict[str, Any]) -> Optional[T]:
        query = self.model.active_only()
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.where(getattr(self.model, field) == value)
        query = query.limit(1)
        try:
            result = await self.db.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.error(f'Error finding {self.model.__name__} by filters: {str(e)}')
            raise DatabaseException(message=f'Failed to find {self.model.__name__} by filters: {str(e)}') from e