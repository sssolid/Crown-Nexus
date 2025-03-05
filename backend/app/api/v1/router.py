from __future__ import annotations

from fastapi import APIRouter

# Import endpoint routers
# from app.api.v1.endpoints import products, fitments, users, auth

api_router = APIRouter()

# Include endpoint routers
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(products.router, prefix="/products", tags=["products"])
# api_router.include_router(fitments.router, prefix="/fitments", tags=["fitments"])
