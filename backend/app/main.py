# backend/app/main.py
"""
FastAPI application entry point.

This module defines the FastAPI application instance and configures
middleware, routers, and lifecycle events. It serves as the entry point
for the application when run with an ASGI server like Uvicorn.

The application uses:
- FastAPI for API definition and routing
- CORS middleware for cross-origin requests
- Lifespan events for startup/shutdown operations
- Centralized error handling
- Versioned API routing
"""

from __future__ import annotations

import logging
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Callable, Optional

from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from fastapi.exceptions import RequestValidationError
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    generic_exception_handler,
)
from app.middleware.error_handler import ErrorHandlerMiddleware

from app.api.deps import get_current_user
from app.api.v1.router import api_router
from app.core.config import Environment, settings
from app.core.logging import setup_logging, get_logger, request_context, set_user_id
from app.fitment.api import router as fitment_router
from app.fitment.dependencies import initialize_mapping_engine
from app.models.user import User

# Initialize structured logging
setup_logging()
logger = get_logger("app.main")


class RequestContextMiddleware:
    """
    Middleware that sets up logging request context.
    
    This middleware ensures each request has a unique ID and tracks
    execution time, both stored in the logging context.
    """
    
    def __init__(self, app: FastAPI) -> None:
        """Initialize middleware with the FastAPI app."""
        self.app = app
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and set up logging context.
        
        Args:
            request: The incoming request
            call_next: The next middleware or route handler
            
        Returns:
            Response: The processed response
        """
        # Get or generate request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Add request ID to response headers
        start_time = time.time()
        
        # Use context manager to set up logging context
        with request_context(request_id=request_id):
            try:
                # Store request ID in request state for dependency injection
                request.state.request_id = request_id
                
                # Process the request
                response = await call_next(request)
                
                # Add timing and request ID headers
                process_time = time.time() - start_time
                response.headers["X-Process-Time"] = f"{process_time:.4f}"
                response.headers["X-Request-ID"] = request_id
                
                # Log request completion
                status_code = response.status_code
                log_method = logger.info if status_code < 400 else (
                    logger.warning if status_code < 500 else logger.error
                )
                log_method(
                    "Request completed",
                    method=request.method,
                    path=request.url.path,
                    status_code=status_code,
                    process_time=process_time,
                )
                
                return response
            except Exception as e:
                # Calculate processing time
                process_time = time.time() - start_time
                
                # Log the error with structured context
                logger.exception(
                    "Request failed",
                    method=request.method,
                    path=request.url.path,
                    error=str(e),
                    process_time=process_time,
                )
                
                # Return error response
                return JSONResponse(
                    status_code=500,
                    content={"detail": "Internal server error"},
                    headers={"X-Request-ID": request_id}
                )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI lifespan event handler.

    This context manager handles application startup and shutdown events.
    It's responsible for initializing and cleaning up resources.

    Args:
        app: FastAPI application instance

    Yields:
        None
    """
    # Startup operations
    logger.info(
        "Application starting",
        app_name=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT.value
    )

    # Initialize fitment mapping engine
    logger.info("Initializing fitment mapping engine")
    await initialize_mapping_engine()
    
    # Additional initialization code here
    # You could add:
    # - Redis connection pool initialization
    # - Elasticsearch client setup
    # - Background task scheduler initialization
    # - Database connection pool setup

    # Allow FastAPI to continue startup
    logger.info("Application startup complete")
    yield

    # Shutdown operations
    logger.info("Application shutting down")
    
    # Cleanup code here
    # You could add:
    # - Closing connection pools
    # - Shutting down background task schedulers
    # - Flushing caches
    
    logger.info("Application shutdown complete")


# Create the FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# Add request context middleware (must be first to capture all requests)
app.add_middleware(RequestContextMiddleware)

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Mount static files directory for media (only for local storage)
if settings.MEDIA_STORAGE_TYPE == "local":
    media_path = Path(settings.MEDIA_ROOT).resolve()
    media_path.mkdir(parents=True, exist_ok=True)
    app.mount("/media", StaticFiles(directory=str(media_path)), name="media")
    logger.info("Media directory mounted", path=str(media_path))


# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(fitment_router)


# Dependency to log the current user
async def log_current_user(
    current_user: Optional[User] = Depends(get_current_user)
) -> Optional[User]:
    """
    Log the current user ID in the request context.
    
    Args:
        current_user: Current authenticated user from token
        
    Returns:
        The current user unchanged
    """
    if current_user:
        set_user_id(str(current_user.id))
    return current_user


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.

    This endpoint allows monitoring systems to check if the application
    is running and responding to requests.

    Returns:
        dict: Health status information
    """
    return {
        "status": "ok",
        "version": settings.VERSION,
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT.value,
    }


# Additional routes and middleware can be added here


if __name__ == "__main__":
    # This block allows running the application directly with
    # `python app/main.py` during development
    import uvicorn
    
    host = "0.0.0.0"
    port = 8000
    
    logger.info(
        "Starting development server",
        host=host,
        port=port,
        url=f"http://{host}:{port}"
    )
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level=settings.fitment.FITMENT_LOG_LEVEL.lower(),
    )