from __future__ import annotations
'Base contracts and protocols for service implementations.\n\nThis module defines common protocols and interfaces that all services should\nimplement, providing a standardized contract for CRUD operations and other\ncommon service functionality.\n'
from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel
from app.db.base_class import Base
from app.services.interfaces import CrudServiceInterface
T = TypeVar('T', bound=Base)
C = TypeVar('C', bound=BaseModel)
U = TypeVar('U', bound=BaseModel)
R = TypeVar('R', bound=BaseModel)
ID = TypeVar('ID')
class BaseServiceProtocol(CrudServiceInterface[T, ID, C, U, R], Generic[T, ID, C, U, R]):
    async def validate_create(self, data: Dict[str, Any], user_id: Optional[str]=None) -> None:
        ...
    async def validate_update(self, entity: T, data: Dict[str, Any], user_id: Optional[str]=None) -> None:
        ...
    async def validate_delete(self, entity: T, user_id: Optional[str]=None) -> None:
        ...
    async def before_create(self, data: Dict[str, Any], user_id: Optional[str]=None) -> None:
        ...
    async def after_create(self, entity: T, user_id: Optional[str]=None) -> None:
        ...
    async def before_update(self, entity: T, data: Dict[str, Any], user_id: Optional[str]=None) -> None:
        ...
    async def after_update(self, updated_entity: T, original_entity: T, user_id: Optional[str]=None) -> None:
        ...
    async def before_delete(self, entity: T, user_id: Optional[str]=None) -> None:
        ...
    async def after_delete(self, entity: T, user_id: Optional[str]=None) -> None:
        ...