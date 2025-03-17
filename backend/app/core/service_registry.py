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

    # Initialize services that don't require DB
    logging_service = dependency_manager.get("logging_service")
    await logging_service.initialize()

    error_handling_service = dependency_manager.get("error_handling_service")
    await error_handling_service.initialize()

    validation_service = dependency_manager.get("validation_service")
    await validation_service.initialize()

    metrics_service = dependency_manager.get("metrics_service")
    await metrics_service.initialize()

    cache_service = dependency_manager.get("cache_service")
    await cache_service.initialize()

    security_service = dependency_manager.get("security_service")
    await security_service.initialize()

    audit_service = dependency_manager.get("audit_service")
    await audit_service.initialize()

    # Services like media_service may need initialization without DB
    media_service = dependency_manager.get("media_service")
    await media_service.initialize()

    logger.info("Services initialized successfully")


async def shutdown_services() -> None:
    """Properly shut down all registered services."""
    logger.info("Shutting down services")

    logging_service = dependency_manager.get("logging_service")
    await logging_service.shutdown()

    error_handling_service = dependency_manager.get("error_handling_service")
    await error_handling_service.shutdown()

    validation_service = dependency_manager.get("validation_service")
    await validation_service.shutdown()

    metrics_service = dependency_manager.get("metrics_service")
    await metrics_service.shutdown()

    cache_service = dependency_manager.get("cache_service")
    await cache_service.shutdown()

    security_service = dependency_manager.get("security_service")
    await security_service.shutdown()

    audit_service = dependency_manager.get("audit_service")
    await audit_service.shutdown()

    media_service = dependency_manager.get("media_service")
    await media_service.shutdown()

    logger.info("Services shut down successfully")
