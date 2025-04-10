# backend/app/api/v1/router.py
"""
API router configuration.

This module configures the FastAPI router for v1 of the API,
organizing routes by feature area and applying appropriate tags
for API documentation. It serves as the central point for including
all endpoint routers in the application.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import auth, fitments, media, products, search, users
from app.api.v1.endpoints.autocare import vcdb, padb, pcdb, qdb

# Create the main API router
api_router = APIRouter()

# Include endpoint routers with appropriate prefixes and tags
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

api_router.include_router(products.router, prefix="/products", tags=["Products"])

api_router.include_router(fitments.router, prefix="/fitments", tags=["Fitments"])

api_router.include_router(media.router, prefix="/media", tags=["Media"])

api_router.include_router(users.router, prefix="/users", tags=["Users"])

api_router.include_router(search.router, prefix="/search", tags=["Search"])

api_router.include_router(
    vcdb.router, prefix="/autocare/vcdb", tags=["Vehicle Component Database"]
)
api_router.include_router(
    padb.router, prefix="/autocare/padb", tags=["Part Attribute Database"]
)
api_router.include_router(
    pcdb.router, prefix="/autocare/pcdb", tags=["Product Component Database"]
)
api_router.include_router(
    qdb.router, prefix="/autocare/qdb", tags=["Qualifier Database"]
)
