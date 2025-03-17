# /backend/app/core/service_registry.py
from __future__ import annotations

import inspect
from typing import Any, Dict, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency_manager import dependency_manager
from app.core.logging import get_logger
from app.services.error_handling_service import ErrorHandlingService
from app.services.logging_service import LoggingService
from app.services.metrics_service import MetricsService
from app.services.validation_service import ValidationService

logger = get_logger("app.core.service_registry")

def register_services() -> None:
    """Register all services in the dependency manager.
    
    This function should be called during application startup to register
    all services in the dependency manager.
    """
    logger.info("Registering services")
    
    # Register core services
    dependency_manager.register_factory(
        "logging_service", 
        lambda: LoggingService()
    )
    
    dependency_manager.register_factory(
        "error_handling_service", 
        lambda: ErrorHandlingService()
    )
    
    dependency_manager.register_factory(
        "validation_service", 
        lambda: ValidationService()
    )
    
    dependency_manager.register_factory(
        "metrics_service", 
        lambda: MetricsService()
    )
    
    # Register other services
    # These would typically require a database session
    
    logger.info("Services registered successfully")

def get_service(service_name: str, db: Optional[AsyncSession] = None) -> Any:
    """Get a service instance by name.
    
    Args:
        service_name: Name of the service
        db: Optional database session
        
    Returns:
        Any: Service instance
    """
    kwargs = {}
    if db:
        kwargs["db"] = db
        
    return dependency_manager.get(service_name, **kwargs)

async def initialize_services() -> None:
    """Initialize all registered services.
    
    This function should be called during application startup to initialize
    all registered services.
    """
    logger.info("Initializing services")
    
    # Initialize core services
    logging_service = dependency_manager.get("logging_service")
    await logging_service.initialize()
    
    error_handling_service = dependency_manager.get("error_handling_service")
    await error_handling_service.initialize()
    
    validation_service = dependency_manager.get("validation_service")
    await validation_service.initialize()
    
    metrics_service = dependency_manager.get("metrics_service")
    await metrics_service.initialize()
    
    # Initialize other services
    
    logger.info("Services initialized successfully")

async def shutdown_services() -> None:
    """Shutdown all registered services.
    
    This function should be called during application shutdown to release
    resources held by services.
    """
    logger.info("Shutting down services")
    
    # Shutdown core services
    logging_service = dependency_manager.get("logging_service")
    await logging_service.shutdown()
    
    error_handling_service = dependency_manager.get("error_handling_service")
    await error_handling_service.shutdown()
    
    validation_service = dependency_manager.get("validation_service")
    await validation_service.shutdown()
    
    metrics_service = dependency_manager.get("metrics_service")
    await metrics_service.shutdown()
    
    # Shutdown other services
    
    logger.info("Services shut down successfully")
