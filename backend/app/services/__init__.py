# app/services/__init__.py
"""Service layer for the application.

This module provides a registry for services and factory functions to create service instances.
Services are responsible for encapsulating business logic and providing a clean API
for the rest of the application to use.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger

logger = get_logger('app.services')


class ServiceRegistry:
    """Registry for application services.
    
    This class implements the Singleton pattern to provide a central registry
    for all services in the application. Services can be registered and retrieved
    by name.
    """
    
    _instance = None
    _services: Dict[str, Any] = {}

    def __new__(cls, *args, **kwargs):
        """Create a singleton instance of the ServiceRegistry.
        
        Returns:
            ServiceRegistry: The singleton instance
        """
        if cls._instance is None:
            cls._instance = super(ServiceRegistry, cls).__new__(cls)
            cls._instance._services = {}
        return cls._instance

    @classmethod
    def register(cls, service_class: Type[Any], name: Optional[str] = None) -> None:
        """Register a service class.
        
        Args:
            service_class: The service class to register
            name: Optional name for the service. If not provided, the class name is used.
        """
        if name is None:
            name = service_class.__name__
        logger.debug(f'Registering service: {name}')
        cls._services[name] = service_class

    @classmethod
    def get(cls, name: str, db: AsyncSession) -> Any:
        """Get a service instance by name.
        
        Args:
            name: Name of the service to retrieve
            db: Database session to pass to the service constructor
            
        Returns:
            An instance of the requested service
            
        Raises:
            ValueError: If the service name is not found in the registry
        """
        if name not in cls._services:
            raise ValueError(f'Service not found: {name}')
        service_class = cls._services[name]
        return service_class(db)

    @classmethod
    def get_all(cls, db: AsyncSession) -> Dict[str, Any]:
        """Get instances of all registered services.
        
        Args:
            db: Database session to pass to the service constructors
            
        Returns:
            Dictionary mapping service names to service instances
        """
        return {name: cls.get(name, db) for name in cls._services}


service_registry = ServiceRegistry()

# Import and register services
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.services.chat import ChatService

service_registry.register(UserService)
service_registry.register(ProductService)
service_registry.register(ChatService)


# Factory functions
def get_chat_service(db: AsyncSession) -> ChatService:
    """Get a ChatService instance.
    
    This factory function provides a clean way to get a ChatService instance
    without directly depending on the ChatService implementation.
    
    Args:
        db: Database session to pass to the ChatService constructor
        
    Returns:
        ChatService: A new ChatService instance
        
    Raises:
        ValueError: If the ChatService is not registered in the ServiceRegistry
    """
    return service_registry.get("ChatService", db)