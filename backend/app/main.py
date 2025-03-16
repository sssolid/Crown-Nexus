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
import logging.config
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Callable, Dict, Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import Environment, settings, LogLevel
from app.fitment.api import router as fitment_router
from app.fitment.dependencies import initialize_mapping_engine

# Configure structured logging
def configure_logging() -> None:
    """Configure application logging based on settings."""
    log_level = settings.fitment.FITMENT_LOG_LEVEL
    
    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "fmt": "%(levelname)s %(asctime)s %(name)s %(process)d %(message)s %(pathname)s %(lineno)d %(funcName)s",
            },
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        },
        "loggers": {
            "app": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": ["console"],
                "level": logging.INFO if settings.ENVIRONMENT == Environment.DEVELOPMENT else logging.WARNING,
                "propagate": False,
            },
            "fitment": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": log_level,
        },
    }
    
    logging.config.dictConfig(logging_config)


# Initialize logging
configure_logging()
logger = logging.getLogger("app.main")


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
    logger.info(f"Starting up {settings.PROJECT_NAME} v{settings.VERSION} in {settings.ENVIRONMENT.value} environment")

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
    yield

    # Shutdown operations
    logger.info(f"Shutting down {settings.PROJECT_NAME}")
    
    # Cleanup code here
    # You could add:
    # - Closing connection pools
    # - Shutting down background task schedulers
    # - Flushing caches


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


# Add middleware for request timing and error handling
@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable) -> Response:
    """
    Middleware to add processing time to response headers.

    This middleware measures how long each request takes to process
    and adds the timing information to the response headers.

    Args:
        request: The incoming request
        call_next: The next middleware or route handler

    Returns:
        Response: The processed response
    """
    start_time = time.time()
    request_id = request.headers.get("X-Request-ID", "unknown")
    
    logger.debug(f"Request started: {request.method} {request.url.path} [ID: {request_id}]")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        
        # Log completed request
        status_code = response.status_code
        log_level = logging.INFO if status_code < 400 else logging.WARNING if status_code < 500 else logging.ERROR
        logger.log(
            log_level, 
            f"Request completed: {request.method} {request.url.path} - Status: {status_code} - Time: {process_time:.4f}s [ID: {request_id}]"
        )
        
        return response
    except Exception as e:
        # Calculate process time even for errors
        process_time = time.time() - start_time
        
        # Log the error with request details
        logger.exception(
            f"Request failed: {request.method} {request.url.path} - Error: {str(e)} - Time: {process_time:.4f}s [ID: {request_id}]"
        )
        
        # Return an error response
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )


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
    logger.info(f"Mounted media directory at {media_path}")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(fitment_router)


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


if __name__ == "__main__":
    # This block allows running the application directly with
    # `python app/main.py` during development
    import uvicorn
    
    host = "0.0.0.0"
    port = 8000
    
    logger.info(f"Starting development server at http://{host}:{port}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level=settings.fitment.FITMENT_LOG_LEVEL.lower(),
    )