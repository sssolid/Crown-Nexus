from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import auth, fitments, media, products

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(fitments.router, prefix="/fitments", tags=["fitments"])
api_router.include_router(media.router, prefix="/media", tags=["media"])
# Additional routers will be included here as they are created
# api_router.include_router(users.router, prefix="/users", tags=["users"])
