# /backend/app/main.py to use the service registry
from __future__ import annotations

from app.db import base

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Optional

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.deps import get_current_user
from app.core.cache.manager import initialize_cache
from app.core.config import Environment, settings
from app.core.dependency_manager import (
    register_services,
    initialize_services,
    shutdown_services,
)
from app.core.error import (
    initialize as initialize_error_system,
    shutdown as shutdown_error_system,
)
from app.core.events import EventBackendType, init_event_backend, init_domain_events
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.core.logging import get_logger, set_user_id
from app.core.metrics import (
    initialize as initialize_metrics_system,
    shutdown as shutdown_metrics_system,
)
from app.core.pagination import (
    initialize as initialize_pagination_system,
    shutdown as shutdown_pagination_system,
)
from app.core.rate_limiting import (
    initialize as initialize_ratelimiting_system,
    shutdown as shutdown_ratelimiting_system,
    RateLimitRule,
    RateLimitStrategy,
)
from app.core.startup.as400_sync import initialize_as400_sync, shutdown_as400_sync
from app.core.validation import (
    initialize as initialize_validation_system,
    shutdown as shutdown_validation_system,
)
from app.domains.users.models import User
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.metrics import MetricsMiddleware
from app.middleware.rate_limiting import RateLimitMiddleware
from app.middleware.request_context import RequestContextMiddleware
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.middleware.security import SecurityHeadersMiddleware, SecureRequestMiddleware

# Logger
logger = get_logger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """FastAPI lifespan event handler.

    This context manager handles application startup and shutdown events.
    It's responsible for initializing and cleaning up resources.

    Args:
        app: FastAPI application instance

    Yields:
        None
    """
    # Initialize event system
    event_backend = EventBackendType.CELERY
    init_event_backend(event_backend)

    # Initialize domain event handlers
    init_domain_events()

    # Register services
    register_services()

    # Initialize error system
    await initialize_error_system()

    # Initialize validation system()
    await initialize_validation_system()

    # Initialize metrics system
    await initialize_metrics_system()

    # Initialize pagination system
    await initialize_pagination_system()

    # Initialize rate limiting system
    await initialize_ratelimiting_system()

    # Initialize cache backends
    await initialize_cache()

    # Initialize services
    await initialize_services()

    # Initialize AS400 sync
    await initialize_as400_sync()

    logger.info(f"Application started in {settings.ENVIRONMENT.value} environment")

    # Include API router
    from app.api.v1.router import api_router

    app.include_router(api_router, prefix=settings.API_V1_STR)

    yield

    # Shutdown AS400 sync
    await shutdown_as400_sync()

    # Shutdown services
    await shutdown_services()

    # Shutdown rate limiting system
    await shutdown_ratelimiting_system()

    # Shutdown pagination system
    await shutdown_pagination_system()

    # Shutdown metrics system
    await shutdown_metrics_system()

    # Shutdown validation system
    await shutdown_validation_system()

    # Shutdown error handling service
    await shutdown_error_system()

    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)


# CORS configuration
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add middleware
app.add_middleware(RequestContextMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(ResponseFormatterMiddleware)

# Add security middleware
app.add_middleware(
    SecurityHeadersMiddleware,
    content_security_policy=settings.CONTENT_SECURITY_POLICY,
    permissions_policy=settings.PERMISSIONS_POLICY,
)

# Add secure request validation
app.add_middleware(SecureRequestMiddleware, block_suspicious_requests=True)

# Add rate limiting middleware
if settings.ENVIRONMENT != Environment.DEVELOPMENT or settings.RATE_LIMIT_ENABLED:
    app.add_middleware(
        RateLimitMiddleware,
        rules=[
            RateLimitRule(
                requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
                window_seconds=60,
                strategy=RateLimitStrategy.IP,
                exclude_paths=["/api/v1/health", "/static/"],
            ),
            # Stricter limits for auth endpoints
            RateLimitRule(
                requests_per_window=10,
                window_seconds=60,
                strategy=RateLimitStrategy.IP,
                path_pattern="/api/v1/auth/",
            ),
        ],
        use_redis=settings.RATE_LIMIT_STORAGE == "redis",
        enable_headers=True,
        block_exceeding_requests=True,
    )

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Static files for media
media_path = Path(settings.MEDIA_ROOT).resolve()
app.mount("/media", StaticFiles(directory=media_path), name="media")


# Log current user
async def log_current_user(
    current_user: User = Depends(get_current_user),
) -> Optional[User]:
    """Log the current user ID in the request context.

    Args:
        current_user: Current authenticated user from token

    Returns:
        The current user unchanged
    """
    if current_user:
        set_user_id(str(current_user.id))
    return current_user


# Health check endpoint
@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint.

    This endpoint allows monitoring systems to check if the application is running
    and responding to requests.

    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT.value,
        "version": settings.VERSION,
    }


# Main entry point for running the application directly
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=settings.ENVIRONMENT == Environment.DEVELOPMENT,
    )
