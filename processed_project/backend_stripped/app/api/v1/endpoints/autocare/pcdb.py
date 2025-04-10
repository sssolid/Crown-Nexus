from __future__ import annotations
'PCDB API endpoints for accessing Product Component Database.\n\nThis module provides HTTP endpoints for interacting with PCDB data,\nincluding parts, categories, positions, and related data.\n'
from typing import Annotated, Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db, get_pagination
from app.api.responses import paginated_response, success_response
from app.domains.autocare.pcdb.service import PCdbService
from app.domains.users.models import User
router = APIRouter()
@router.get('/version')
async def get_version(db: Annotated[AsyncSession, Depends(get_db)]) -> str:
    service = PCdbService(db)
    version = await service.get_version()
    return version
@router.get('/stats')
async def get_pcdb_stats(db: Annotated[AsyncSession, Depends(get_db)]) -> Dict[str, Any]:
    service = PCdbService(db)
    stats = await service.get_stats()
    return stats
@router.get('/categories')
async def get_categories(db: Annotated[AsyncSession, Depends(get_db)]) -> List[Dict[str, Any]]:
    service = PCdbService(db)
    categories = await service.get_categories()
    return categories
@router.get('/categories/{category_id}/subcategories')
async def get_subcategories_by_category(category_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> List[Dict[str, Any]]:
    service = PCdbService(db)
    subcategories = await service.get_subcategories_by_category(category_id)
    return subcategories
@router.get('/parts/search')
async def search_parts(db: Annotated[AsyncSession, Depends(get_db)], search_term: Optional[str]=Query(None, description='Search term for parts'), category_id: Optional[int]=Query(None, description='Filter by category ID'), subcategory_id: Optional[int]=Query(None, description='Filter by subcategory ID'), position_id: Optional[int]=Query(None, description='Filter by position ID'), page: int=Query(1, ge=1, description='Page number'), page_size: int=Query(20, ge=1, le=100, description='Items per page')) -> Dict[str, Any]:
    service = PCdbService(db)
    categories = [category_id] if category_id is not None else None
    subcategories = [subcategory_id] if subcategory_id is not None else None
    positions = [position_id] if position_id is not None else None
    result = await service.search_parts(search_term=search_term, categories=categories, subcategories=subcategories, positions=positions, page=page, page_size=page_size)
    return result
@router.get('/parts/{part_terminology_id}')
async def get_part_details(part_terminology_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Dict[str, Any]:
    service = PCdbService(db)
    details = await service.get_part_details(part_terminology_id)
    return details
@router.get('/categories/{category_id}/parts')
async def get_parts_by_category(db: Annotated[AsyncSession, Depends(get_db)], category_id: int, page: int=Query(1, ge=1, description='Page number'), page_size: int=Query(20, ge=1, le=100, description='Items per page')) -> Dict[str, Any]:
    service = PCdbService(db)
    result = await service.get_parts_by_category(category_id=category_id, page=page, page_size=page_size)
    return result
@router.get('/categories/search')
async def search_categories(db: Annotated[AsyncSession, Depends(get_db)], search_term: str=Query(..., description='Search term for categories')) -> List[Dict[str, Any]]:
    service = PCdbService(db)
    categories = await service.search_categories(search_term=search_term)
    return categories
@router.get('/positions')
async def get_positions(db: Annotated[AsyncSession, Depends(get_db)]) -> List[Dict[str, Any]]:
    service = PCdbService(db)
    positions = await service.get_positions()
    return positions
@router.get('/parts/{part_terminology_id}/positions')
async def get_part_positions(part_terminology_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> List[Dict[str, Any]]:
    service = PCdbService(db)
    positions = await service.get_part_positions(part_terminology_id)
    return positions
@router.get('/parts/{part_terminology_id}/supersessions')
async def get_part_supersessions(part_terminology_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Dict[str, List[Dict[str, Any]]]:
    service = PCdbService(db)
    supersessions = await service.get_part_supersessions(part_terminology_id)
    return supersessions