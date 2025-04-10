from __future__ import annotations
"Permission service implementation.\n\nThis module provides a unified service interface for permission-related functions\nthroughout the application, integrating with the application's dependency management,\nmetrics, caching, and error handling systems.\n"
import time
from typing import Any, Dict, List, Optional, Set, Union, cast, TYPE_CHECKING
from app.core.dependency_manager import get_service, register_service
from app.core.error import handle_exception
from app.core.exceptions import AuthenticationException, PermissionDeniedException
from app.core.permissions.checker import PermissionChecker
from app.core.permissions.models import Permission, ROLE_PERMISSIONS
from app.core.permissions.utils import get_user_by_id, check_owner_permission
from app.logging import get_logger
if TYPE_CHECKING:
    from app.domains.users.models import User
    from sqlalchemy.ext.asyncio import AsyncSession
logger = get_logger('app.core.permissions.service')
class PermissionService:
    def __init__(self, db: Optional['AsyncSession']=None) -> None:
        self.db = db
        self.logger = get_logger('app.core.permissions.service')
        self.checker = PermissionChecker()
        try:
            self.metrics_service = get_service('metrics_service')
        except Exception as e:
            self.logger.warning(f'Metrics service not available: {str(e)}')
            self.metrics_service = None
        try:
            self.cache_service = get_service('cache_service')
        except Exception as e:
            self.logger.warning(f'Cache service not available: {str(e)}')
            self.cache_service = None
        try:
            self.event_service = get_service('event_service')
        except Exception as e:
            self.logger.warning(f'Event service not available: {str(e)}')
            self.event_service = None
        try:
            self.error_service = get_service('error_service')
        except Exception as e:
            self.logger.warning(f'Error service not available: {str(e)}')
            self.error_service = None
        self.logger.info('Permission service initialized')
    async def initialize(self) -> None:
        self.logger.info('Initializing permission service')
    async def shutdown(self) -> None:
        self.logger.info('Shutting down permission service')
    async def check_permission(self, user: 'User', permission: Permission, resource_id: Optional[str]=None, resource_type: Optional[str]=None) -> bool:
        start_time = time.monotonic()
        has_permission = False
        try:
            if self.cache_service:
                cache_key = f'permission:check:{user.id}:{permission}'
                cached_result = await self.cache_service.get(cache_key)
                if cached_result is not None:
                    has_permission = cached_result
                    self.logger.debug(f'Permission check cache hit: {user.id}, {permission}', user_id=str(user.id), permission=str(permission), result=has_permission)
                    if self.metrics_service:
                        self.metrics_service.increment_counter('permission_check_cache_hits_total', labels={'permission': str(permission), 'granted': str(has_permission)})
                    return has_permission
            has_permission = self.checker.has_permission(user, permission)
            if self.cache_service:
                await self.cache_service.set(f'permission:check:{user.id}:{permission}', has_permission, ttl=300)
            if not has_permission:
                self.logger.warning('Permission denied', user_id=str(user.id), user_role=user.role, permission=str(permission), resource_id=resource_id, resource_type=resource_type)
            return has_permission
        except Exception as e:
            handle_exception(exception=e, user_id=str(getattr(user, 'id', None)), function_name='check_permission')
            return False
        finally:
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram('permission_check_duration_seconds', duration, {'permission': str(permission), 'granted': str(has_permission)})
                self.metrics_service.increment_counter('permission_checks_total', labels={'permission': str(permission), 'granted': str(has_permission)})
    async def check_permissions(self, user: 'User', permissions: List[Permission], require_all: bool=True, resource_id: Optional[str]=None, resource_type: Optional[str]=None) -> bool:
        start_time = time.monotonic()
        result = False
        try:
            if not permissions:
                return True
            if len(permissions) == 1:
                return await self.check_permission(user, permissions[0], resource_id, resource_type)
            permission_results = {}
            for permission in permissions:
                permission_results[str(permission)] = await self.check_permission(user, permission, resource_id, resource_type)
                if require_all and (not permission_results[str(permission)]):
                    result = False
                    break
                elif not require_all and permission_results[str(permission)]:
                    result = True
                    break
            if require_all:
                result = all(permission_results.values())
            else:
                result = any(permission_results.values())
            if not result:
                self.logger.warning('Multiple permissions check failed', user_id=str(user.id), user_role=user.role, permissions=str(permissions), require_all=require_all, results=permission_results, resource_id=resource_id, resource_type=resource_type)
            return result
        except Exception as e:
            handle_exception(exception=e, user_id=str(getattr(user, 'id', None)), function_name='check_permissions')
            return False
        finally:
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram('multiple_permissions_check_duration_seconds', duration, {'permissions_count': str(len(permissions)), 'require_all': str(require_all), 'granted': str(result)})
                self.metrics_service.increment_counter('multiple_permissions_checks_total', labels={'permissions_count': str(len(permissions)), 'require_all': str(require_all), 'granted': str(result)})
    async def check_object_permission(self, user: 'User', obj: Any, permission: Permission, owner_field: str='created_by_id') -> bool:
        start_time = time.monotonic()
        result = False
        try:
            result = self.checker.check_object_permission(user, obj, permission, owner_field)
            if not result:
                obj_id = getattr(obj, 'id', None)
                obj_type = obj.__class__.__name__
                self.logger.warning('Object permission denied', user_id=str(user.id), user_role=user.role, permission=str(permission), object_id=obj_id, object_type=obj_type, owner_field=owner_field)
            return result
        except Exception as e:
            handle_exception(exception=e, user_id=str(getattr(user, 'id', None)), function_name='check_object_permission')
            return False
        finally:
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram('object_permission_check_duration_seconds', duration, {'permission': str(permission), 'granted': str(result), 'object_type': obj.__class__.__name__})
                self.metrics_service.increment_counter('object_permission_checks_total', labels={'permission': str(permission), 'granted': str(result), 'object_type': obj.__class__.__name__})
    async def ensure_permission(self, user: 'User', permission: Permission, resource_type: str, resource_id: Optional[str]=None) -> None:
        has_permission = await self.check_permission(user, permission, resource_id, resource_type)
        if not has_permission:
            action = str(permission).split(':')[-1]
            if self.event_service:
                await self.event_service.publish(event_name='permission.denied', payload={'user_id': str(user.id), 'permission': str(permission), 'resource_type': resource_type, 'resource_id': resource_id, 'action': action})
            if self.error_service:
                raise self.error_service.permission_denied(action=action, resource_type=resource_type, permission=str(permission))
            else:
                raise PermissionDeniedException(message=f'Permission denied to {action} {resource_type}', action=action, resource_type=resource_type, permission=str(permission))
    async def ensure_object_permission(self, user: 'User', obj: Any, permission: Permission, owner_field: str='created_by_id') -> None:
        has_permission = await self.check_object_permission(user, obj, permission, owner_field)
        if not has_permission:
            action = str(permission).split(':')[-1]
            resource = str(permission).split(':')[0]
            obj_id = getattr(obj, 'id', None)
            obj_type = obj.__class__.__name__
            if self.event_service:
                await self.event_service.publish(event_name='permission.object_denied', payload={'user_id': str(user.id), 'permission': str(permission), 'object_type': obj_type, 'object_id': obj_id, 'action': action, 'resource': resource})
            if self.error_service:
                raise self.error_service.permission_denied(action=action, resource_type=resource, permission=str(permission))
            else:
                raise PermissionDeniedException(message=f'Permission denied to {action} this {resource}', action=action, resource_type=resource, permission=str(permission))
    async def get_user_permissions(self, user_id: str) -> Set[Permission]:
        if not self.db:
            raise ValueError('Database session required to get user permissions')
        start_time = time.monotonic()
        try:
            if self.cache_service:
                cache_key = f'permissions:user:{user_id}'
                cached_permissions = await self.cache_service.get(cache_key)
                if cached_permissions is not None:
                    self.logger.debug(f'User permissions cache hit: {user_id}', user_id=user_id, permissions_count=len(cached_permissions))
                    if self.metrics_service:
                        self.metrics_service.increment_counter('user_permissions_cache_hits_total')
                    return {Permission(p) for p in cached_permissions if p in Permission._value2member_map_}
            user = await get_user_by_id(self.db, user_id)
            role_permissions = ROLE_PERMISSIONS.get(user.role, set())
            user_permissions = getattr(user, 'permissions', [])
            if isinstance(role_permissions, set):
                all_permissions = role_permissions.copy()
            else:
                all_permissions = set(role_permissions)
            if user_permissions:
                all_permissions.update(user_permissions)
            if self.cache_service:
                await self.cache_service.set(f'permissions:user:{user_id}', [p.value for p in all_permissions], ttl=300)
            return all_permissions
        except AuthenticationException:
            raise
        except Exception as e:
            handle_exception(exception=e, user_id=user_id, function_name='get_user_permissions')
            raise
        finally:
            if self.metrics_service:
                duration = time.monotonic() - start_time
                self.metrics_service.observe_histogram('get_user_permissions_duration_seconds', duration)
    async def invalidate_permissions_cache(self, user_id: str) -> None:
        if not self.cache_service:
            return
        try:
            cache_key = f'permissions:user:{user_id}'
            await self.cache_service.delete(cache_key)
            await self.cache_service.invalidate_pattern(f'permission:check:{user_id}:*')
            self.logger.debug(f'Invalidated permissions cache for user: {user_id}', user_id=user_id)
        except Exception as e:
            self.logger.warning(f'Failed to invalidate permissions cache: {str(e)}', user_id=user_id, exc_info=True)
_permission_service: Optional[PermissionService] = None
@register_service
def get_permission_service(db: Optional['AsyncSession']=None) -> PermissionService:
    global _permission_service
    if _permission_service is None:
        _permission_service = PermissionService(db)
    elif db is not None:
        _permission_service.db = db
    return _permission_service