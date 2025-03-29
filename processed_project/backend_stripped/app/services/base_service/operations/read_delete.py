from __future__ import annotations
'Read and delete operations for the base service.\n\nThis module provides functionality for reading and deleting entities,\nwith support for permission checking, filtering, and hooks.\n'
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ErrorCode, PermissionDeniedException, ResourceNotFoundException
from app.logging import get_logger
from app.core.permissions import Permission, PermissionChecker
from app.db.base_class import Base
from app.db.utils import transactional
logger = get_logger('app.services.base_service.operations.read_delete')
T = TypeVar('T', bound=Base)
R = TypeVar('R', bound=BaseModel)
ID = TypeVar('ID')
class ReadDeleteOperations(Generic[T, R, ID]):
    @transactional
    async def get(self, db: AsyncSession, repository: Any, id: ID, user_id: Optional[str]=None, required_permission: Optional[Permission]=None, get_user_func: Optional[callable]=None) -> T:
        logger.debug(f'Getting entity with ID: {id}')
        entity = await repository.get_by_id(id)
        if not entity:
            logger.warning(f'Entity with ID {id} not found')
            raise ResourceNotFoundException(f'Entity not found', code=ErrorCode.RESOURCE_NOT_FOUND, details={'id': str(id)}, status_code=404)
        if user_id and required_permission and get_user_func:
            user = await get_user_func(user_id)
            if not PermissionChecker.has_permission(user, required_permission):
                logger.warning(f'Permission denied for user {user_id} to read entity')
                raise PermissionDeniedException(f"You don't have permission to read this entity", code=ErrorCode.PERMISSION_DENIED, details={'required_permission': required_permission}, status_code=403)
        logger.debug(f'Found entity with ID: {id}')
        return entity
    async def get_by_id(self, db: AsyncSession, repository: Any, id: ID, user_id: Optional[str]=None, required_permission: Optional[Permission]=None, get_user_func: Optional[callable]=None) -> Optional[T]:
        try:
            return await self.get(db=db, repository=repository, id=id, user_id=user_id, required_permission=required_permission, get_user_func=get_user_func)
        except ResourceNotFoundException:
            return None
        except PermissionDeniedException:
            return None
    @transactional
    async def get_multi(self, db: AsyncSession, repository: Any, user_id: Optional[str]=None, page: int=1, page_size: int=20, filters: Optional[Dict[str, Any]]=None, order_by: Optional[str]=None, required_permission: Optional[Permission]=None, get_user_func: Optional[callable]=None, apply_filters_func: Optional[callable]=None) -> Dict[str, Any]:
        logger.debug(f'Getting entities with page={page}, page_size={page_size}, filters={filters}')
        if user_id and required_permission and get_user_func:
            user = await get_user_func(user_id)
            if not PermissionChecker.has_permission(user, required_permission):
                logger.warning(f'Permission denied for user {user_id} to list entities')
                raise PermissionDeniedException(f"You don't have permission to list entities", code=ErrorCode.PERMISSION_DENIED, details={'required_permission': required_permission}, status_code=403)
        applied_filters = filters or {}
        if apply_filters_func:
            applied_filters = await apply_filters_func(applied_filters, user_id)
        try:
            result = await repository.get_all(page=page, page_size=page_size, order_by=order_by, filters=applied_filters)
            logger.debug(f"Found {result.get('total', 0)} entities")
            return result
        except Exception as e:
            logger.error(f'Error getting entities: {str(e)}')
            raise
    async def get_all(self, db: AsyncSession, repository: Any, page: int=1, page_size: int=20, filters: Optional[Dict[str, Any]]=None, user_id: Optional[str]=None, required_permission: Optional[Permission]=None, get_user_func: Optional[callable]=None, apply_filters_func: Optional[callable]=None) -> Dict[str, Any]:
        return await self.get_multi(db=db, repository=repository, user_id=user_id, page=page, page_size=page_size, filters=filters, required_permission=required_permission, get_user_func=get_user_func, apply_filters_func=apply_filters_func)
    async def to_response(self, entity: T, response_model: Type[R]) -> R:
        return response_model.from_orm(entity)
    async def to_response_multi(self, entities: List[T], response_model: Type[R]) -> List[R]:
        return [await self.to_response(entity, response_model) for entity in entities]
    @transactional
    async def delete(self, db: AsyncSession, repository: Any, id: ID, user_id: Optional[str]=None, hard_delete: bool=False, required_permission: Optional[Permission]=None, validate_func: Optional[callable]=None, before_func: Optional[callable]=None, after_func: Optional[callable]=None, get_user_func: Optional[callable]=None) -> bool:
        logger.debug(f'Deleting entity with ID: {id}')
        entity = await repository.get_by_id(id)
        if not entity:
            logger.warning(f'Entity with ID {id} not found')
            raise ResourceNotFoundException(f'Entity not found', code=ErrorCode.RESOURCE_NOT_FOUND, details={'id': str(id)}, status_code=404)
        if user_id and required_permission and get_user_func:
            user = await get_user_func(user_id)
            if not PermissionChecker.has_permission(user, required_permission):
                logger.warning(f'Permission denied for user {user_id} to delete entity')
                raise PermissionDeniedException(f"You don't have permission to delete this entity", code=ErrorCode.PERMISSION_DENIED, details={'required_permission': required_permission}, status_code=403)
        if validate_func:
            await validate_func(entity, user_id)
        if before_func:
            await before_func(entity, user_id)
        try:
            result = await repository.delete(id, user_id, hard_delete)
            if after_func:
                await after_func(entity, user_id)
            logger.info(f'Deleted entity with ID: {id}')
            return result
        except Exception as e:
            logger.error(f'Error deleting entity: {str(e)}')
            raise