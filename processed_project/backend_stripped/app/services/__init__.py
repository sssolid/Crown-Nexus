from __future__ import annotations
import logging
from typing import Any, Dict, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import get_logger
logger = get_logger('app.services')
class ServiceRegistry:
    _instance = None
    _services: Dict[str, Any] = {}
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ServiceRegistry, cls).__new__(cls)
            cls._instance._services = {}
        return cls._instance
    @classmethod
    def register(cls, service_class: Type[Any], name: Optional[str]=None) -> None:
        if name is None:
            name = service_class.__name__
        logger.debug(f'Registering service: {name}')
        cls._services[name] = service_class
    @classmethod
    def get(cls, name: str, db: AsyncSession) -> Any:
        if name not in cls._services:
            raise ValueError(f'Service not found: {name}')
        service_class = cls._services[name]
        return service_class(db)
    @classmethod
    def get_all(cls, db: AsyncSession) -> Dict[str, Any]:
        return {name: cls.get(name, db) for name in cls._services}
service_registry = ServiceRegistry()
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.services.chat import ChatService
service_registry.register(UserService)
service_registry.register(ProductService)
service_registry.register(ChatService)
def get_chat_service(db: AsyncSession) -> ChatService:
    return service_registry.get('ChatService', db)