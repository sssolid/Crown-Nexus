# /backend/app/main.py to use the service registry
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
    generic_exception_handler
)
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.api.deps import get_current_user
from app.api.v1.router import api_router
from app.core.config import Environment, settings
from app.core.logging import get_logger, request_context, set_user_id
from app.core.service_registry import register_services, initialize_services, shutdown_services
from app.core.cache.manager import initialize_cache

from app.fitment.api import router as fitment_router
from app.fitment.dependencies import initialize_mapping_engine
from app.models.user import User

import uvicorn

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
    # Initialize cache backends
    initialize_cache()

    # Register services
    register_services()
    
    # Initialize services
    await initialize_services()
    
    # Initialize fitment mapping engine
    await initialize_mapping_engine()
    
    logger.info(f"Application started in {settings.ENVIRONMENT.value} environment")
    yield
    
    # Shutdown services
    await shutdown_services()
    
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
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(ResponseFormatterMiddleware)

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Include fitment router
app.include_router(
    fitment_router,
    prefix=f"{settings.API_V1_STR}/fitment",
    tags=["fitment"],
)

# Static files for media
media_path = Path(settings.MEDIA_ROOT).resolve()
app.mount("/media", StaticFiles(directory=media_path), name="media")

# Request context middleware
class RequestContextMiddleware:
    """Middleware that sets up logging request context.

    This middleware ensures each request has a unique ID and tracks execution time,
    both stored in the logging context.
    """

    def __init__(self, app: Callable) -> None:
        """Initialize middleware with the FastAPI app."""
        self.app = app

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """Process the request and set up logging context.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            Response: The processed response
        """
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Store request start time
        start_time = time.time()
        
        # Add request ID to request state
        request.state.request_id = request_id
        
        # Use logging context manager
        with request_context(request_id):
            # Log request
            logger.info(
                f"Request: {request.method} {request.url.path}",
                method=request.method,
                path=request.url.path,
                client=request.client.host if request.client else None,
            )
            
            # Process request
            response = await call_next(request)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response: {response.status_code}",
                status_code=response.status_code,
                execution_time=f"{execution_time:.4f}s",
            )
            
            # Add request ID and timing headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Execution-Time"] = f"{execution_time:.4f}s"
            
            return response

# Log current user
async def log_current_user(current_user: User = Depends(get_current_user)) -> Optional[User]:
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
@app.get('/health')
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
    host = '0.0.0.0'
    port = 8000
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=settings.ENVIRONMENT == Environment.DEVELOPMENT,
    )