from __future__ import annotations
'PADB API endpoints for accessing Part Attribute Database.\n\nThis module provides HTTP endpoints for interacting with PADB data,\nincluding part attributes, measurement groups, UOM codes, and valid values.\n'
from typing import Annotated, Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db, get_pagination
from app.api.responses import paginated_response, success_response
from app.domains.autocare.padb.service import PAdbService
from app.domains.users.models import User
router = APIRouter()
@router.get('/version')
async def get_version(db: Annotated[AsyncSession, Depends(get_db)]) -> str:
    service = PAdbService(db)
    version = await service.get_version()
    return version
@router.get('/stats')
async def get_padb_stats(db: Annotated[AsyncSession, Depends(get_db)]) -> Dict[str, Any]:
    service = PAdbService(db)
    stats = await service.get_stats()
    return stats
@router.get('/attributes/search')
async def search_attributes(db: Annotated[AsyncSession, Depends(get_db)], search_term: Optional[str]=Query(None, description='Search term for attributes'), part_terminology_id: Optional[int]=Query(None, description='Filter by part terminology ID'), page: int=Query(1, ge=1, description='Page number'), page_size: int=Query(20, ge=1, le=100, description='Items per page')) -> Dict[str, Any]:
    service = PAdbService(db)
    result = await service.search_attributes(search_term=search_term, part_terminology_id=part_terminology_id, page=page, page_size=page_size)
    return result
@router.get('/attributes/{pa_id}')
async def get_attribute_details(pa_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Dict[str, Any]:
    service = PAdbService(db)
    details = await service.get_attribute_details(pa_id)
    return details
@router.get('/parts/{part_terminology_id}/attributes')
async def get_part_attributes(part_terminology_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Dict[str, Any]:
    service = PAdbService(db)
    attributes = await service.get_part_attributes(part_terminology_id)
    return attributes
@router.get('/measurement-groups')
async def get_measurement_groups(db: Annotated[AsyncSession, Depends(get_db)]) -> List[Dict[str, Any]]:
    service = PAdbService(db)
    groups = await service.get_measurement_groups()
    return groups
@router.get('/measurement-groups/{measurement_group_id}/uom-codes')
async def get_uom_codes_by_measurement_group(measurement_group_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> List[Dict[str, Any]]:
    service = PAdbService(db)
    uom_codes = await service.get_uom_codes_by_measurement_group(measurement_group_id)
    return uom_codes
@router.get('/attribute-assignments/{papt_id}/valid-values')
async def get_valid_values_for_attribute(papt_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> List[Dict[str, Any]]:
    service = PAdbService(db)
    valid_values = await service.get_valid_values_for_attribute(papt_id)
    return valid_values