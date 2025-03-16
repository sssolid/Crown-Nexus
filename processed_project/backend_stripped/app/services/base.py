from __future__ import annotations
import uuid
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, cast
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import BusinessLogicException, DatabaseException, ValidationException
from app.core.logging import get_logger
from app.core.permissions import Permission, PermissionChecker
from app.db.base_class import Base
from app.db.utils import count_query, transaction, transactional
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.pagination import CursorPaginationParams, OffsetPaginationParams, PaginationResult
from app.services.pagination import PaginationService
from app.utils.errors import ensure_not_none, resource_already_exists, resource_not_found, validation_error
logger = get_logger('app.services.base')
T = TypeVar('T', bound=Base)
C = TypeVar('C', bound=BaseModel)
U = TypeVar('U', bound=BaseModel)
R = TypeVar('R', bound=BaseModel)
class BaseService(Generic[T, C, U, R]):
    def __init__(self, db: AsyncSession, model_class: Type[T], create_schema: Type[C], update_schema: Type[U], response_schema: Type[R]) -> None:
        self.db = db
        self.model = model_class
        self.repository = BaseRepository(model_class, db)
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.response_schema = response_schema
        self.resource_name = model_class.__name__
    @transactional
    async def get(self, id: Any, current_user: User) -> T:
        permission = f'{self.resource_name.lower()}:read'
        PermissionChecker.ensure_object_permission(current_user, {'id': id}, cast(Permission, permission))
        entity = await self.repository.get_by_id(id)
        if not entity:
            raise resource_not_found(self.resource_name, id)
        PermissionChecker.ensure_object_permission(current_user, entity, cast(Permission, permission))
        return entity
    @transactional
    async def get_multi(self, current_user: User, page: int=1, page_size: int=20, filters: Optional[Dict[str, Any]]=None, order_by: Optional[str]=None) -> Dict[str, Any]:
        permission = f'{self.resource_name.lower()}:read'
        PermissionChecker.ensure_object_permission(current_user, {}, cast(Permission, permission))
        result = await self.repository.get_all(page=page, page_size=page_size, filters=filters, order_by=order_by)
        return result
    async def get_paginated(self, current_user: User, params: OffsetPaginationParams, filters: Optional[Dict[str, Any]]=None) -> PaginationResult[R]:
        permission = f'{self.resource_name.lower()}:read'
        PermissionChecker.ensure_object_permission(current_user, {}, cast(Permission, permission))
        query = self.model.active_only()
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        pagination_service = PaginationService(self.db, self.model, self.response_schema)
        return await pagination_service.paginate_with_offset(query=query, params=params, transform_func=self.to_response)
    async def get_paginated_with_cursor(self, current_user: User, params: CursorPaginationParams, filters: Optional[Dict[str, Any]]=None) -> PaginationResult[R]:
        permission = f'{self.resource_name.lower()}:read'
        PermissionChecker.ensure_object_permission(current_user, {}, cast(Permission, permission))
        query = self.model.active_only()
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        pagination_service = PaginationService(self.db, self.model, self.response_schema)
        return await pagination_service.paginate_with_cursor(query=query, params=params, transform_func=self.to_response)
    @transactional
    async def create(self, obj_in: Union[C, Dict[str, Any]], current_user: User) -> T:
        permission = f'{self.resource_name.lower()}:create'
        PermissionChecker.ensure_object_permission(current_user, {}, cast(Permission, permission))
        if isinstance(obj_in, dict):
            data = obj_in
        else:
            data = obj_in.dict(exclude_unset=True)
        await self.validate_create(data, current_user)
        if hasattr(self.model, 'created_by_id'):
            data['created_by_id'] = str(current_user.id)
        if hasattr(self.model, 'updated_by_id'):
            data['updated_by_id'] = str(current_user.id)
        try:
            entity = await self.repository.create(data)
            await self.after_create(entity, current_user)
            return entity
        except Exception as e:
            logger.error(f'Error creating {self.resource_name}: {str(e)}')
            if isinstance(e, (ValidationException, BusinessLogicException)):
                raise
            raise DatabaseException(message=f'Failed to create {self.resource_name}: {str(e)}') from e
    @transactional
    async def update(self, id: Any, obj_in: Union[U, Dict[str, Any]], current_user: User) -> T:
        entity = await self.repository.get_by_id(id)
        if not entity:
            raise resource_not_found(self.resource_name, id)
        permission = f'{self.resource_name.lower()}:update'
        PermissionChecker.ensure_object_permission(current_user, entity, cast(Permission, permission))
        if isinstance(obj_in, dict):
            data = obj_in
        else:
            data = obj_in.dict(exclude_unset=True)
        await self.validate_update(entity, data, current_user)
        if hasattr(self.model, 'updated_by_id'):
            data['updated_by_id'] = str(current_user.id)
        try:
            updated_entity = await self.repository.update(id, data, current_user.id)
            if not updated_entity:
                raise resource_not_found(self.resource_name, id)
            await self.after_update(updated_entity, entity, current_user)
            return updated_entity
        except Exception as e:
            logger.error(f'Error updating {self.resource_name}: {str(e)}')
            if isinstance(e, (ValidationException, BusinessLogicException)):
                raise
            raise DatabaseException(message=f'Failed to update {self.resource_name}: {str(e)}') from e
    @transactional
    async def delete(self, id: Any, current_user: User, hard_delete: bool=False) -> bool:
        entity = await self.repository.get_by_id(id)
        if not entity:
            raise resource_not_found(self.resource_name, id)
        permission = f'{self.resource_name.lower()}:delete'
        PermissionChecker.ensure_object_permission(current_user, entity, cast(Permission, permission))
        await self.validate_delete(entity, current_user)
        try:
            result = await self.repository.delete(id, current_user.id, hard_delete)
            if not result:
                raise resource_not_found(self.resource_name, id)
            await self.after_delete(entity, current_user)
            return result
        except Exception as e:
            logger.error(f'Error deleting {self.resource_name}: {str(e)}')
            if isinstance(e, (ValidationException, BusinessLogicException)):
                raise
            raise DatabaseException(message=f'Failed to delete {self.resource_name}: {str(e)}') from e
    async def to_response(self, entity: T) -> R:
        if hasattr(self.response_schema, 'from_orm'):
            return self.response_schema.from_orm(entity)
        return self.response_schema(**entity.to_dict())
    async def to_response_multi(self, entities: List[T]) -> List[R]:
        return [await self.to_response(entity) for entity in entities]
    async def validate_create(self, data: Dict[str, Any], current_user: User) -> None:
        pass
    async def validate_update(self, entity: T, data: Dict[str, Any], current_user: User) -> None:
        pass
    async def validate_delete(self, entity: T, current_user: User) -> None:
        pass
    async def after_create(self, entity: T, current_user: User) -> None:
        pass
    async def after_update(self, updated_entity: T, original_entity: T, current_user: User) -> None:
        pass
    async def after_delete(self, entity: T, current_user: User) -> None:
        pass