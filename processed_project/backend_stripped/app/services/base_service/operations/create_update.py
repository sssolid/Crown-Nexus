from __future__ import annotations
'Create and update operations for the base service.\n\nThis module provides functionality for creating and updating entities,\nwith support for validation, permission checking, and hooks.\n'
from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ErrorCode, PermissionDeniedException, ResourceNotFoundException
from app.logging import get_logger
from app.core.permissions import Permission, PermissionChecker
from app.db.base_class import Base
from app.db.utils import transactional
logger = get_logger('app.services.base_service.operations.create_update')
T = TypeVar('T', bound=Base)
C = TypeVar('C', bound=BaseModel)
U = TypeVar('U', bound=BaseModel)
ID = TypeVar('ID')
class CreateUpdateOperations(Generic[T, C, U, ID]):
    @transactional
    async def create(self, db: AsyncSession, repository: Any, data: Dict[str, Any], user_id: Optional[str]=None, required_permission: Optional[Permission]=None, validate_func: Optional[callable]=None, before_func: Optional[callable]=None, after_func: Optional[callable]=None, get_user_func: Optional[callable]=None) -> T:
        logger.debug(f'Creating entity with data: {data}')
        if user_id and required_permission and get_user_func:
            user = await get_user_func(user_id)
            if not PermissionChecker.has_permission(user, required_permission):
                logger.warning(f'Permission denied for user {user_id} to create entity')
                raise PermissionDeniedException(f"You don't have permission to create this entity", code=ErrorCode.PERMISSION_DENIED, details={'required_permission': required_permission}, status_code=403)
        if validate_func:
            await validate_func(data, user_id)
        if before_func:
            await before_func(data, user_id)
        try:
            entity = await repository.create(data)
            if after_func:
                await after_func(entity, user_id)
            logger.info(f"Created entity with ID: {getattr(entity, 'id', None)}")
            return entity
        except Exception as e:
            logger.error(f'Error creating entity: {str(e)}')
            raise
    async def create_with_schema(self, db: AsyncSession, repository: Any, schema: C, user_id: Optional[str]=None, required_permission: Optional[Permission]=None, validate_func: Optional[callable]=None, before_func: Optional[callable]=None, after_func: Optional[callable]=None, get_user_func: Optional[callable]=None) -> T:
        return await self.create(db=db, repository=repository, data=schema.model_dump(), user_id=user_id, required_permission=required_permission, validate_func=validate_func, before_func=before_func, after_func=after_func, get_user_func=get_user_func)
    @transactional
    async def update(self, db: AsyncSession, repository: Any, id: ID, data: Dict[str, Any], user_id: Optional[str]=None, required_permission: Optional[Permission]=None, validate_func: Optional[callable]=None, before_func: Optional[callable]=None, after_func: Optional[callable]=None, get_user_func: Optional[callable]=None) -> T:
        logger.debug(f'Updating entity with ID: {id}, data: {data}')
        entity = await repository.get_by_id(id)
        if not entity:
            logger.warning(f'Entity with ID {id} not found')
            raise ResourceNotFoundException(f'Entity not found', code=ErrorCode.RESOURCE_NOT_FOUND, details={'id': str(id)}, status_code=404)
        if user_id and required_permission and get_user_func:
            user = await get_user_func(user_id)
            if not PermissionChecker.has_permission(user, required_permission):
                logger.warning(f'Permission denied for user {user_id} to update entity')
                raise PermissionDeniedException(f"You don't have permission to update this entity", code=ErrorCode.PERMISSION_DENIED, details={'required_permission': required_permission}, status_code=403)
        if validate_func:
            await validate_func(entity, data, user_id)
        original_entity = entity
        if before_func:
            await before_func(entity, data, user_id)
        try:
            updated_entity = await repository.update(id, data, user_id)
            if not updated_entity:
                raise ResourceNotFoundException(f'Entity not found', code=ErrorCode.RESOURCE_NOT_FOUND, details={'id': str(id)}, status_code=404)
            if after_func:
                await after_func(updated_entity, original_entity, user_id)
            logger.info(f'Updated entity with ID: {id}')
            return updated_entity
        except Exception as e:
            logger.error(f'Error updating entity: {str(e)}')
            raise
    async def update_with_schema(self, db: AsyncSession, repository: Any, id: ID, schema: U, user_id: Optional[str]=None, required_permission: Optional[Permission]=None, validate_func: Optional[callable]=None, before_func: Optional[callable]=None, after_func: Optional[callable]=None, get_user_func: Optional[callable]=None) -> Optional[T]:
        return await self.update(db=db, repository=repository, id=id, data=schema.model_dump(exclude_unset=True), user_id=user_id, required_permission=required_permission, validate_func=validate_func, before_func=before_func, after_func=after_func, get_user_func=get_user_func)