from __future__ import annotations
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.services.search import SearchService, get_search_service
from app.services.vehicle import VehicleDataService, get_vehicle_service
router = APIRouter()
@router.get('/')
async def global_search(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], search_service: Annotated[SearchService, Depends(get_search_service)], q: str=Query(..., description='Search query'), entity_types: Optional[List[str]]=Query(None, description='Entity types to search (products, fitments, categories)'), page: int=Query(1, ge=1, description='Page number'), page_size: int=Query(20, ge=1, le=100, description='Items per page')) -> Any:
    valid_types = {'products', 'fitments', 'categories'}
    if entity_types:
        entity_types = [et for et in entity_types if et in valid_types]
    results = await search_service.global_search(search_term=q, entity_types=entity_types, page=page, page_size=page_size)
    return results
@router.get('/products')
async def search_products(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], search_service: Annotated[SearchService, Depends(get_search_service)], q: Optional[str]=Query(None, description='Search query'), category_id: Optional[str]=Query(None, description='Category ID'), is_active: Optional[bool]=Query(None, description='Active status'), page: int=Query(1, ge=1, description='Page number'), page_size: int=Query(20, ge=1, le=100, description='Items per page'), use_elasticsearch: bool=Query(True, description='Use Elasticsearch if available')) -> Any:
    attributes = {}
    results = await search_service.search_products(search_term=q, category_id=category_id, attributes=attributes or None, is_active=is_active, page=page, page_size=page_size, use_elasticsearch=use_elasticsearch)
    return results
@router.get('/fitments')
async def search_fitments(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], search_service: Annotated[SearchService, Depends(get_search_service)], q: Optional[str]=Query(None, description='Search query'), year: Optional[int]=Query(None, description='Vehicle year'), make: Optional[str]=Query(None, description='Vehicle make'), model: Optional[str]=Query(None, description='Vehicle model'), engine: Optional[str]=Query(None, description='Vehicle engine'), transmission: Optional[str]=Query(None, description='Vehicle transmission'), page: int=Query(1, ge=1, description='Page number'), page_size: int=Query(20, ge=1, le=100, description='Items per page')) -> Any:
    results = await search_service.search_fitments(search_term=q, year=year, make=make, model=model, engine=engine, transmission=transmission, page=page, page_size=page_size)
    return results
@router.get('/vehicle-data/years')
async def get_vehicle_years(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)]) -> List[int]:
    return await vehicle_service.get_years()
@router.get('/vehicle-data/makes')
async def get_vehicle_makes(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)], year: Optional[int]=Query(None, description='Filter by year')) -> List[str]:
    return await vehicle_service.get_makes(year)
@router.get('/vehicle-data/models')
async def get_vehicle_models(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)], make: Optional[str]=Query(None, description='Filter by make'), year: Optional[int]=Query(None, description='Filter by year')) -> List[str]:
    return await vehicle_service.get_models(make, year)
@router.get('/vehicle-data/engines')
async def get_vehicle_engines(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)], make: Optional[str]=Query(None, description='Filter by make'), model: Optional[str]=Query(None, description='Filter by model'), year: Optional[int]=Query(None, description='Filter by year')) -> List[str]:
    return await vehicle_service.get_engines(make, model, year)
@router.get('/vehicle-data/transmissions')
async def get_vehicle_transmissions(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)], make: Optional[str]=Query(None, description='Filter by make'), model: Optional[str]=Query(None, description='Filter by model'), year: Optional[int]=Query(None, description='Filter by year'), engine: Optional[str]=Query(None, description='Filter by engine')) -> List[str]:
    return await vehicle_service.get_transmissions(make, model, year, engine)
@router.post('/vehicle-data/validate-fitment')
async def validate_vehicle_fitment(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)], year: int, make: str, model: str, engine: Optional[str]=None, transmission: Optional[str]=None) -> dict:
    is_valid = await vehicle_service.validate_fitment(year, make, model, engine, transmission)
    return {'valid': is_valid}
@router.get('/vehicle-data/decode-vin/{vin}')
async def decode_vin(vin: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)]) -> Any:
    result = await vehicle_service.decode_vin(vin)
    if result is None:
        return {'error': 'Invalid VIN'}
    return result