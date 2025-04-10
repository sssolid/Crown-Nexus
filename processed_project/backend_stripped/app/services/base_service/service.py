from __future__ import annotations
'Main base service implementation.\n\nThis module provides the primary BaseService that implements the CrudServiceInterface\nwith standardized CRUD operations, permission checking, and lifecycle hooks.\n'
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.logging import get_logger
from app.core.permissions import Permission
from app.db.base_class import Base
from app.repositories.base import BaseRepository
from app.schemas.pagination import CursorPaginationParams, OffsetPaginationParams, PaginationResult
from app.services.base_service.contracts import BaseServiceProtocol
from app.services.base_service.operations import CreateUpdateOperations, ReadDeleteOperations
from app.services.base_service.permissions import PermissionHelper
from app.services.pagination.service import PaginationService
logger = get_logger('app.services.base_service.service')
T = TypeVar('T', bound=Base)
C = TypeVar('C', bound=BaseModel)
U = TypeVar('U', bound=BaseModel)
R = TypeVar('R', bound=BaseModel)
ID = TypeVar('ID')
class BaseService(Generic[T, C, U, R, ID], BaseServiceProtocol[T, ID, C, U, R]):
    def __init__(self, db: AsyncSession, model_class: Type[T], create_schema: Type[C], update_schema: Type[U], response_schema: Type[R], repository_class: Type[BaseRepository[T, ID]]=BaseRepository) -> None:
        self.db = db
        self.model = model_class
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.response_schema = response_schema
        self.repository = repository_class(model_class, db)
        self.create_update_ops = CreateUpdateOperations[T, C, U, ID]()
        self.read_delete_ops = ReadDeleteOperations[T, R, ID]()
        self.pagination_service = PaginationService[T, R](db, model_class, response_schema)
        self.logger = logger.bind(service=self.__class__.__name__)
        self.required_create_permission: Optional[Permission] = None
        self.required_read_permission: Optional[Permission] = None
        self.required_update_permission: Optional[Permission] = None
        self.required_delete_permission: Optional[Permission] = None
    async def initialize(self) -> None:
        self.logger.debug('Initializing service')
    async def shutdown(self) -> None:
        self.logger.debug('Shutting down service')
    async def create(self, data: Dict[str, Any], user_id: Optional[str]=None) -> T:
        return await self.create_update_ops.create(db=self.db, repository=self.repository, data=data, user_id=user_id, required_permission=self.required_create_permission, validate_func=self.validate_create, before_func=self.before_create, after_func=self.after_create, get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id))
    async def create_with_schema(self, schema: C, user_id: Optional[str]=None) -> T:
        return await self.create_update_ops.create_with_schema(db=self.db, repository=self.repository, schema=schema, user_id=user_id, required_permission=self.required_create_permission, validate_func=self.validate_create, before_func=self.before_create, after_func=self.after_create, get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id))
    async def delete(self, id: ID, user_id: Optional[str]=None, hard_delete: bool=False) -> bool:
        return await self.read_delete_ops.delete(db=self.db, repository=self.repository, id=id, user_id=user_id, hard_delete=hard_delete, required_permission=self.required_delete_permission, validate_func=self.validate_delete, before_func=self.before_delete, after_func=self.after_delete, get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id))
    async def get(self, id: ID, user_id: Optional[str]=None) -> T:
        return await self.read_delete_ops.get(db=self.db, repository=self.repository, id=id, user_id=user_id, required_permission=self.required_read_permission, get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id))
    async def get_by_id(self, id: ID, user_id: Optional[str]=None) -> Optional[T]:
        return await self.read_delete_ops.get_by_id(db=self.db, repository=self.repository, id=id, user_id=user_id, required_permission=self.required_read_permission, get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id))
    async def get_multi(self, user_id: Optional[str]=None, page: int=1, page_size: int=20, filters: Optional[Dict[str, Any]]=None, order_by: Optional[str]=None) -> Dict[str, Any]:
        return await self.read_delete_ops.get_multi(db=self.db, repository=self.repository, user_id=user_id, page=page, page_size=page_size, filters=filters, order_by=order_by, required_permission=self.required_read_permission, get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id), apply_filters_func=self.apply_filters)
    async def get_all(self, page: int=1, page_size: int=20, filters: Optional[Dict[str, Any]]=None, user_id: Optional[str]=None) -> Dict[str, Any]:
        return await self.get_multi(user_id=user_id, page=page, page_size=page_size, filters=filters)
    async def update(self, id: ID, data: Dict[str, Any], user_id: Optional[str]=None) -> T:
        return await self.create_update_ops.update(db=self.db, repository=self.repository, id=id, data=data, user_id=user_id, required_permission=self.required_update_permission, validate_func=self.validate_update, before_func=self.before_update, after_func=self.after_update, get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id))
    async def update_with_schema(self, id: ID, schema: U, user_id: Optional[str]=None) -> Optional[T]:
        return await self.create_update_ops.update_with_schema(db=self.db, repository=self.repository, id=id, schema=schema, user_id=user_id, required_permission=self.required_update_permission, validate_func=self.validate_update, before_func=self.before_update, after_func=self.after_update, get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id))
    async def get_paginated(self, user_id: Optional[str], params: OffsetPaginationParams, filters: Optional[Dict[str, Any]]=None) -> PaginationResult[R]:
        if user_id and self.required_read_permission:
            user = await PermissionHelper.get_user(self.db, user_id)
            if not hasattr(user, 'has_permission') or not user.has_permission(self.required_read_permission):
                self.logger.warning(f'Permission denied for user {user_id} to list {self.model.__name__}')
                raise PermissionDeniedException(f"You don't have permission to list {self.model.__name__}", code='PERMISSION_DENIED', details={'required_permission': self.required_read_permission}, status_code=403)
        applied_filters = filters or {}
        applied_filters = await self.apply_filters(applied_filters, user_id)
        query = self.repository.build_query(applied_filters)
        return await self.pagination_service.paginate_with_offset(query, params, self.to_response)
    async def get_paginated_with_cursor(self, user_id: Optional[str], params: CursorPaginationParams, filters: Optional[Dict[str, Any]]=None) -> PaginationResult[R]:
        if user_id and self.required_read_permission:
            user = await PermissionHelper.get_user(self.db, user_id)
            if not hasattr(user, 'has_permission') or not user.has_permission(self.required_read_permission):
                self.logger.warning(f'Permission denied for user {user_id} to list {self.model.__name__}')
                raise PermissionDeniedException(f"You don't have permission to list {self.model.__name__}", code='PERMISSION_DENIED', details={'required_permission': self.required_read_permission}, status_code=403)
        applied_filters = filters or {}
        applied_filters = await self.apply_filters(applied_filters, user_id)
        query = self.repository.build_query(applied_filters)
        return await self.pagination_service.paginate_with_cursor(query, params, self.to_response)
    async def to_response(self, entity: T) -> R:
        return await self.read_delete_ops.to_response(entity, self.response_schema)
    async def to_response_multi(self, entities: List[T]) -> List[R]:
        return await self.read_delete_ops.to_response_multi(entities, self.response_schema)
    async def apply_filters(self, filters: Dict[str, Any], user_id: Optional[str]=None) -> Dict[str, Any]:
        return filters
    async def validate_create(self, data: Dict[str, Any], user_id: Optional[str]=None) -> None:
        pass
    async def validate_update(self, entity: T, data: Dict[str, Any], user_id: Optional[str]=None) -> None:
        pass
    async def validate_delete(self, entity: T, user_id: Optional[str]=None) -> None:
        pass
    async def before_create(self, data: Dict[str, Any], user_id: Optional[str]=None) -> None:
        pass
    async def after_create(self, entity: T, user_id: Optional[str]=None) -> None:
        pass
    async def before_update(self, entity: T, data: Dict[str, Any], user_id: Optional[str]=None) -> None:
        pass
    async def after_update(self, updated_entity: T, original_entity: T, user_id: Optional[str]=None) -> None:
        pass
    async def before_delete(self, entity: T, user_id: Optional[str]=None) -> None:
        pass
    async def after_delete(self, entity: T, user_id: Optional[str]=None) -> None:
        pass