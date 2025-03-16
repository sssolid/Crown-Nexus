# app/services/__init__.py
from __future__ import annotations

import logging
from typing import Any, Dict, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger

logger = get_logger("app.services")


class ServiceRegistry:
    """Registry for service instances.
    
    This class provides a central registry for service instances,
    allowing for dependency injection and simplified access to services.
    """
    
    _instance = None
    _services: Dict[str, Any] = {}
    
    def __new__(cls, *args, **kwargs):
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super(ServiceRegistry, cls).__new__(cls)
            cls._instance._services = {}
        return cls._instance
    
    @classmethod
    def register(cls, service_class: Type[Any], name: Optional[str] = None) -> None:
        """Register a service class.
        
        Args:
            service_class: Service class to register
            name: Optional name for the service (defaults to class name)
        """
        if name is None:
            name = service_class.__name__
            
        logger.debug(f"Registering service: {name}")
        cls._services[name] = service_class
    
    @classmethod
    def get(cls, name: str, db: AsyncSession) -> Any:
        """Get a service instance.
        
        Args:
            name: Service name
            db: Database session
            
        Returns:
            Any: Service instance
            
        Raises:
            ValueError: If service not found
        """
        if name not in cls._services:
            raise ValueError(f"Service not found: {name}")
            
        service_class = cls._services[name]
        return service_class(db)
    
    @classmethod
    def get_all(cls, db: AsyncSession) -> Dict[str, Any]:
        """Get all service instances.
        
        Args:
            db: Database session
            
        Returns:
            Dict[str, Any]: Service instances
        """
        return {name: cls.get(name, db) for name in cls._services}


# Create singleton instance
service_registry = ServiceRegistry()


# Import services to register them
from app.services.user_service import UserService
from app.services.product_service import ProductService
# Import other services...

# Register services
service_registry.register(UserService)
service_registry.register(ProductService)
# Register other services...