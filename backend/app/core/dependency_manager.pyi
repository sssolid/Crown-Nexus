# app/core/dependency_manager.pyi
from typing import Any, Awaitable, Callable, Literal, Optional, overload
from sqlalchemy.ext.asyncio import AsyncSession

# Import all service classes
from app.core.error.service import ErrorService
from app.core.validation import ValidationService
from app.core.metrics.service import MetricsService
from app.core.pagination.service import PaginationService
from app.core.rate_limiting import RateLimitingService
from app.core.cache.service import CacheService
from app.domains.audit.service import AuditService
from app.services.search import SearchService
from app.domains.media.service import MediaService

# Define overloads for each service
@overload
def get_service(
    service_name: Literal["error_service"], db: Optional[AsyncSession] = None
) -> ErrorService: ...
@overload
def get_service(
    service_name: Literal["validation_service"], db: Optional[AsyncSession] = None
) -> ValidationService: ...
@overload
def get_service(
    service_name: Literal["metrics_service"], db: Optional[AsyncSession] = None
) -> MetricsService: ...
@overload
def get_service(
    service_name: Literal["pagination_service"], db: Optional[AsyncSession] = None
) -> PaginationService: ...
@overload
def get_service(
    service_name: Literal["rate_limiting_service"], db: Optional[AsyncSession] = None
) -> RateLimitingService: ...
@overload
def get_service(
    service_name: Literal["cache_service"], db: Optional[AsyncSession] = None
) -> CacheService: ...
@overload
def get_service(
    service_name: Literal["audit_service"], db: Optional[AsyncSession] = None
) -> AuditService: ...
@overload
def get_service(
    service_name: Literal["search_service"], db: Optional[AsyncSession] = None
) -> SearchService: ...
@overload
def get_service(
    service_name: Literal["media_service"], db: Optional[AsyncSession] = None
) -> MediaService: ...

# Fallback for other services
@overload
def get_service(service_name: str, db: Optional[AsyncSession] = None) -> Any: ...

# Include other important functions from dependency_manager.py
def get_dependency(name: str, **kwargs: Any) -> Any: ...
def register_service(provider: Any, name: Optional[str] = None) -> Any: ...
def register_async_service(
    async_provider: Any, name: Optional[str] = None
) -> Callable[..., Awaitable[T]]: ...
async def initialize_services() -> None: ...
async def shutdown_services() -> None: ...
def register_services() -> None: ...
def inject_dependency(dependency_name: str) -> Any: ...
def with_dependencies(**dependencies: str) -> Any: ...
