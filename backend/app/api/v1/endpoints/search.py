# backend/app/api/v1/endpoints/search.py
"""
Global search API endpoints.

This module provides endpoints for searching across the application:
- Full-text search across products, fitments, and categories
- Advanced filtering options
- Faceted search results
- Type-ahead suggestions
"""

from __future__ import annotations

from typing import Annotated, Any, List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.services.search import SearchService, get_search_service
from app.services.vehicle import VehicleDataService, get_vehicle_service

router = APIRouter()


@router.get("/")
async def global_search(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    search_service: Annotated[SearchService, Depends(get_search_service)],
    q: str = Query(..., description="Search query"),
    entity_types: Optional[List[str]] = Query(
        None,
        description="Entity types to search (products, fitments, categories)",
    ),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> Any:
    """
    Perform a global search across multiple entity types.

    Args:
        db: Database session
        current_user: Current authenticated user
        search_service: Search service
        q: Search query
        entity_types: Entity types to search
        page: Page number
        page_size: Items per page

    Returns:
        Dict[str, Any]: Search results grouped by entity type
    """
    # Validate entity types
    valid_types = {"products", "fitments", "categories"}
    if entity_types:
        entity_types = [et for et in entity_types if et in valid_types]

    # Perform search
    results = await search_service.global_search(
        search_term=q,
        entity_types=entity_types,
        page=page,
        page_size=page_size,
    )

    return results


@router.get("/products")
async def search_products(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    search_service: Annotated[SearchService, Depends(get_search_service)],
    q: Optional[str] = Query(None, description="Search query"),
    category_id: Optional[str] = Query(None, description="Category ID"),
    is_active: Optional[bool] = Query(None, description="Active status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    use_elasticsearch: bool = Query(True, description="Use Elasticsearch if available"),
) -> Any:
    """
    Search for products with filtering.

    Args:
        db: Database session
        current_user: Current authenticated user
        search_service: Search service
        q: Search query
        category_id: Category ID filter
        is_active: Active status filter
        page: Page number
        page_size: Items per page
        use_elasticsearch: Whether to use Elasticsearch

    Returns:
        Dict[str, Any]: Search results with pagination
    """
    # Extract attributes from query parameters (would be handled better in a real implementation)
    attributes = {}

    # Perform search
    results = await search_service.search_products(
        search_term=q,
        category_id=category_id,
        attributes=attributes or None,
        is_active=is_active,
        page=page,
        page_size=page_size,
        use_elasticsearch=use_elasticsearch,
    )

    return results


@router.get("/fitments")
async def search_fitments(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    search_service: Annotated[SearchService, Depends(get_search_service)],
    q: Optional[str] = Query(None, description="Search query"),
    year: Optional[int] = Query(None, description="Vehicle year"),
    make: Optional[str] = Query(None, description="Vehicle make"),
    model: Optional[str] = Query(None, description="Vehicle model"),
    engine: Optional[str] = Query(None, description="Vehicle engine"),
    transmission: Optional[str] = Query(None, description="Vehicle transmission"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> Any:
    """
    Search for fitments with filtering.

    Args:
        db: Database session
        current_user: Current authenticated user
        search_service: Search service
        q: Search query
        year: Vehicle year filter
        make: Vehicle make filter
        model: Vehicle model filter
        engine: Vehicle engine filter
        transmission: Vehicle transmission filter
        page: Page number
        page_size: Items per page

    Returns:
        Dict[str, Any]: Search results with pagination
    """
    # Perform search
    results = await search_service.search_fitments(
        search_term=q,
        year=year,
        make=make,
        model=model,
        engine=engine,
        transmission=transmission,
        page=page,
        page_size=page_size,
    )

    return results


@router.get("/vehicle-data/years")
async def get_vehicle_years(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)],
) -> List[int]:
    """
    Get all available vehicle years.

    Args:
        db: Database session
        current_user: Current authenticated user
        vehicle_service: Vehicle data service

    Returns:
        List[int]: List of years
    """
    return await vehicle_service.get_years()


@router.get("/vehicle-data/makes")
async def get_vehicle_makes(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)],
    year: Optional[int] = Query(None, description="Filter by year"),
) -> List[str]:
    """
    Get all available vehicle makes.

    Args:
        db: Database session
        current_user: Current authenticated user
        vehicle_service: Vehicle data service
        year: Filter by year

    Returns:
        List[str]: List of makes
    """
    return await vehicle_service.get_makes(year)


@router.get("/vehicle-data/models")
async def get_vehicle_models(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)],
    make: Optional[str] = Query(None, description="Filter by make"),
    year: Optional[int] = Query(None, description="Filter by year"),
) -> List[str]:
    """
    Get all available vehicle models.

    Args:
        db: Database session
        current_user: Current authenticated user
        vehicle_service: Vehicle data service
        make: Filter by make
        year: Filter by year

    Returns:
        List[str]: List of models
    """
    return await vehicle_service.get_models(make, year)


@router.get("/vehicle-data/engines")
async def get_vehicle_engines(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)],
    make: Optional[str] = Query(None, description="Filter by make"),
    model: Optional[str] = Query(None, description="Filter by model"),
    year: Optional[int] = Query(None, description="Filter by year"),
) -> List[str]:
    """
    Get all available vehicle engines.

    Args:
        db: Database session
        current_user: Current authenticated user
        vehicle_service: Vehicle data service
        make: Filter by make
        model: Filter by model
        year: Filter by year

    Returns:
        List[str]: List of engines
    """
    return await vehicle_service.get_engines(make, model, year)


@router.get("/vehicle-data/transmissions")
async def get_vehicle_transmissions(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)],
    make: Optional[str] = Query(None, description="Filter by make"),
    model: Optional[str] = Query(None, description="Filter by model"),
    year: Optional[int] = Query(None, description="Filter by year"),
    engine: Optional[str] = Query(None, description="Filter by engine"),
) -> List[str]:
    """
    Get all available vehicle transmissions.

    Args:
        db: Database session
        current_user: Current authenticated user
        vehicle_service: Vehicle data service
        make: Filter by make
        model: Filter by model
        year: Filter by year
        engine: Filter by engine

    Returns:
        List[str]: List of transmissions
    """
    return await vehicle_service.get_transmissions(make, model, year, engine)


@router.post("/vehicle-data/validate-fitment")
async def validate_vehicle_fitment(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)],
    year: int,
    make: str,
    model: str,
    engine: Optional[str] = None,
    transmission: Optional[str] = None,
) -> dict:
    """
    Validate if a fitment combination exists.

    Args:
        db: Database session
        current_user: Current authenticated user
        vehicle_service: Vehicle data service
        year: Vehicle year
        make: Vehicle make
        model: Vehicle model
        engine: Vehicle engine
        transmission: Vehicle transmission

    Returns:
        dict: Validation result
    """
    is_valid = await vehicle_service.validate_fitment(
        year, make, model, engine, transmission
    )

    return {"valid": is_valid}


@router.get("/vehicle-data/decode-vin/{vin}")
async def decode_vin(
    vin: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    vehicle_service: Annotated[VehicleDataService, Depends(get_vehicle_service)],
) -> Any:
    """
    Decode a Vehicle Identification Number (VIN).

    Args:
        vin: Vehicle Identification Number
        db: Database session
        current_user: Current authenticated user
        vehicle_service: Vehicle data service

    Returns:
        Dict[str, Any]: Decoded vehicle data
    """
    result = await vehicle_service.decode_vin(vin)

    if result is None:
        return {"error": "Invalid VIN"}

    return result
