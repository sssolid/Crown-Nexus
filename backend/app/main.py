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
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import Environment, settings
from app.fitment.api import router as fitment_router
from app.fitment.dependencies import initialize_mapping_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


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
    logger.info("Starting up application")

    # Initialize connection pools, caches, etc.
    # Here you would typically:
    # - Initialize Redis connection
    # - Initialize Elasticsearch client
    # - Set up background tasks

    await initialize_mapping_engine()

    # Allow FastAPI to continue startup
    yield

    # Shutdown operations
    logger.info("Shutting down application")

    # Clean up resources
    # Here you would typically:
    # - Close connections
    # - Cancel background tasks
    # - Flush caches


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


# Add middleware for request timing
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
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        return response
    except Exception as e:
        # Log the error
        logger.exception(f"Request failed: {str(e)}")
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

# Mount static files directory for media (only in development)
if settings.ENVIRONMENT == Environment.DEVELOPMENT:
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
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    # This block allows running the application directly with
    # `python app/main.py` during development
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
