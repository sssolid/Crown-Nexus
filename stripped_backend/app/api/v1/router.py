from __future__ import annotations
from fastapi import APIRouter
from app.api.v1.endpoints import auth, fitments, media, products, search, users
api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['Authentication'])
api_router.include_router(products.router, prefix='/products', tags=['Products'])
api_router.include_router(fitments.router, prefix='/fitments', tags=['Fitments'])
api_router.include_router(media.router, prefix='/media', tags=['Media'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(search.router, prefix='/search', tags=['Search'])