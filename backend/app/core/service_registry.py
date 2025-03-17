# backend/app/core/service_registry.py
from __future__ import annotations

import inspect
from typing import Any, Dict, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency_manager import dependency_manager
from app.core.logging import get_logger
from app.services.audit_service import AuditService
from app.services.cache_service import CacheService
from app.services.chat import ChatService
from app.services.currency_service import ExchangeRateService
from app.services.error_handling_service import ErrorHandlingService
from app.services.logging_service import LoggingService
from app.services.media_service import MediaService
from app.services.metrics_service import MetricsService
from app.services.product_service import ProductService
from app.services.search import SearchService
from app.services.security_service import SecurityService
from app.services.user_service import UserService
from app.services.validation_service import ValidationService
from app.services.vehicle import VehicleDataService

logger = get_logger("app.core.service_registry")


def register_services() -> None:
    """
    Register all application services with the dependency manager.

    This function makes services available for dependency injection throughout
    the application.
    """
    logger.info("Registering services")

    # Core services
    dependency_manager.register_factory("logging_service", lambda: LoggingService())
    dependency_manager.register_factory("error_handling_service", lambda: ErrorHandlingService())
    dependency_manager.register_factory("validation_service", lambda: ValidationService())
    dependency_manager.register_factory("metrics_service", lambda: MetricsService())
    dependency_manager.register_factory("cache_service", lambda: CacheService())
    dependency_manager.register_factory("security_service", lambda: SecurityService())
    dependency_manager.register_factory("audit_service", lambda: AuditService())

    # Domain services requiring DB
    dependency_manager.register_factory(
        "user_service",
        lambda db: UserService(db) if db else None
    )
    dependency_manager.register_factory(
        "product_service",
        lambda db: ProductService(db) if db else None
    )
    dependency_manager.register_factory(
        "chat_service",
        lambda db: ChatService(db) if db else None
    )
    dependency_manager.register_factory(
        "search_service",
        lambda db: SearchService(db) if db else None
    )
    dependency_manager.register_factory(
        "vehicle_service",
        lambda db: VehicleDataService(db) if db else None
    )
    dependency_manager.register_factory(
        "media_service",
        lambda: MediaService()
    )
    dependency_manager.register_factory(
        "exchange_rate_service",
        lambda db: ExchangeRateService(db) if db else None
    )

    logger.info("Services registered successfully")


def get_service(service_name: str, db: Optional[AsyncSession] = None) -> Any:
    """
    Get a registered service by name.

    Args:
        service_name: Name of the service to retrieve
        db: Optional database session to pass to the service

    Returns:
        The requested service instance
    """
    kwargs = {}
    if db:
        kwargs["db"] = db
    return dependency_manager.get(service_name, **kwargs)


async def initialize_services() -> None:
    """Initialize all registered services."""
    logger.info("Initializing services")

    # Initialize services in the correct order
    services_order = [
        "logging_service",
        "error_handling_service",
        "validation_service",
        "metrics_service",
        "cache_service",
        "security_service",
        "audit_service",
        "media_service",
        "user_service",
        "chat_service",
        "search_service",
        "product_service",
        "vehicle_service",
        "exchange_rate_service",
    ]

    for service_name in services_order:
        try:
            service = dependency_manager.get(service_name)
            await service.initialize()
            logger.info(f"Initialized {service_name}")
        except Exception as e:
            logger.error(f"Error initializing {service_name}: {str(e)}", exc_info=e)

    logger.info("Services initialized successfully")


async def shutdown_services() -> None:
    """Shut down all registered services."""
    logger.info("Shutting down services")

    # Shutdown services in reverse order
    services_order = [
        "exchange_rate_service",
        "vehicle_service",
        "product_service",
        "search_service",
        "chat_service",
        "user_service",
        "media_service",
        "audit_service",
        "security_service",
        "cache_service",
        "metrics_service",
        "validation_service",
        "error_handling_service",
        "logging_service",
        "exchange_rate_service",
    ]

    for service_name in services_order:
        try:
            service = dependency_manager.get(service_name)
            await service.shutdown()
            logger.info(f"Shut down {service_name}")
        except Exception as e:
            logger.error(f"Error shutting down {service_name}: {str(e)}", exc_info=e)

    logger.info("Services shut down successfully")
