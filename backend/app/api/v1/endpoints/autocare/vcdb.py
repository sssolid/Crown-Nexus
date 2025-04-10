# processed_project/backend_stripped/app/api/v1/endpoints/vcdb.py
from __future__ import annotations

"""VCDB API endpoints for accessing Vehicle Component Database.

This module provides HTTP endpoints for interacting with VCDB data,
including vehicles, makes, models, and related vehicle components.
"""

from typing import Annotated, Any, Dict, List, Optional, Tuple, Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db, get_pagination
from app.api.responses import paginated_response, success_response
from app.domains.autocare.vcdb.service import VCdbService
from app.domains.users.models import User

router = APIRouter()


@router.get("/version")
async def get_version(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> str:
    """Get the current VCDB version.

    Args:
        db: Database session

    Returns:
        Current VCDB version as string
    """
    service = VCdbService(db)
    version = await service.get_version()
    return version


@router.get("/stats")
async def get_vcdb_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get VCdb statistics.

    Args:
        db: Database session

    Returns:
        VCdb statistics
    """
    service = VCdbService(db)
    stats = await service.get_stats()
    return stats


@router.get("/years")
async def get_years(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get all years.

    Args:
        db: Database session

    Returns:
        List of years
    """
    service = VCdbService(db)
    years = await service.get_years()
    return years


@router.get("/years/range")
async def get_year_range(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Tuple[int, int]:
    """Get the range of available years.

    Args:
        db: Database session

    Returns:
        Tuple of (min_year, max_year)
    """
    service = VCdbService(db)
    year_range = await service.get_year_range()
    return year_range


@router.get("/makes")
async def get_makes(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get all makes.

    Args:
        db: Database session

    Returns:
        List of makes
    """
    service = VCdbService(db)
    makes = await service.get_makes()
    return makes


@router.get("/years/{year}/makes")
async def get_makes_by_year(
    year: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get makes by year.

    Args:
        year: Year to filter by
        db: Database session

    Returns:
        List of makes for the given year
    """
    service = VCdbService(db)
    makes = await service.get_makes_by_year(year)
    return makes


@router.get("/makes/search")
async def search_makes(
    db: Annotated[AsyncSession, Depends(get_db)],
    search_term: str = Query(..., description="Search term for makes"),
) -> List[Dict[str, Any]]:
    """Search makes by name.

    Args:
        search_term: Text to search for
        db: Database session

    Returns:
        List of matching makes
    """
    service = VCdbService(db)
    makes = await service.search_makes(search_term)
    return makes


@router.get("/makes/{make_id}")
async def get_make_by_id(
    make_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get make by ID.

    Args:
        make_id: ID of the make
        db: Database session

    Returns:
        Make details
    """
    service = VCdbService(db)
    make = await service.get_make_by_id(make_id)
    return make


@router.get("/years/{year}/makes/{make_id}/models")
async def get_models_by_year_make(
    year: int,
    make_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get models by year and make.

    Args:
        year: Year to filter by
        make_id: Make ID to filter by
        db: Database session

    Returns:
        List of models for the given year and make
    """
    service = VCdbService(db)
    models = await service.get_models_by_year_make(year, make_id)
    return models


@router.get("/models/search")
async def search_models(
    db: Annotated[AsyncSession, Depends(get_db)],
    search_term: str = Query(..., description="Search term for models"),
) -> List[Dict[str, Any]]:
    """Search models by name.

    Args:
        search_term: Text to search for
        db: Database session

    Returns:
        List of matching models
    """
    service = VCdbService(db)
    models = await service.search_models(search_term)
    return models


@router.get("/models/{model_id}")
async def get_model_by_id(
    model_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get model by ID.

    Args:
        model_id: ID of the model
        db: Database session

    Returns:
        Model details
    """
    service = VCdbService(db)
    model = await service.get_model_by_id(model_id)
    return model


@router.get("/base-vehicles/{base_vehicle_id}/submodels")
async def get_submodels_by_base_vehicle(
    base_vehicle_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get submodels by base vehicle.

    Args:
        base_vehicle_id: Base vehicle ID
        db: Database session

    Returns:
        List of submodels for the given base vehicle
    """
    service = VCdbService(db)
    submodels = await service.get_submodels_by_base_vehicle(base_vehicle_id)
    return submodels


@router.get("/submodels")
async def get_all_submodels(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get all submodels.

    Args:
        db: Database session

    Returns:
        List of all submodels
    """
    service = VCdbService(db)
    submodels = await service.get_all_submodels()
    return submodels


@router.get("/submodels/search")
async def search_submodels(
    db: Annotated[AsyncSession, Depends(get_db)],
    search_term: str = Query(..., description="Search term for submodels"),
) -> List[Dict[str, Any]]:
    """Search submodels by name.

    Args:
        search_term: Text to search for
        db: Database session

    Returns:
        List of matching submodels
    """
    service = VCdbService(db)
    submodels = await service.search_submodels(search_term)
    return submodels


@router.get("/vehicle-types")
async def get_vehicle_types(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get all vehicle types.

    Args:
        db: Database session

    Returns:
        List of vehicle types
    """
    service = VCdbService(db)
    vehicle_types = await service.get_vehicle_types()
    return vehicle_types


@router.get("/vehicle-type-groups/{group_id}/vehicle-types")
async def get_vehicle_types_by_group(
    group_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get vehicle types by group.

    Args:
        group_id: Vehicle type group ID
        db: Database session

    Returns:
        List of vehicle types in the specified group
    """
    service = VCdbService(db)
    vehicle_types = await service.get_vehicle_types_by_group(group_id)
    return vehicle_types


@router.get("/regions")
async def get_regions(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get all regions.

    Args:
        db: Database session

    Returns:
        List of regions
    """
    service = VCdbService(db)
    regions = await service.get_regions()
    return regions


@router.get("/regions/{parent_id}/children")
async def get_regions_by_parent(
    parent_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get regions by parent region.

    Args:
        parent_id: Parent region ID
        db: Database session

    Returns:
        List of child regions
    """
    service = VCdbService(db)
    regions = await service.get_regions_by_parent(parent_id)
    return regions


@router.get("/base-vehicles/{base_vehicle_id}")
async def get_base_vehicle(
    base_vehicle_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get base vehicle by ID.

    Args:
        base_vehicle_id: Base vehicle ID
        db: Database session

    Returns:
        Base vehicle details
    """
    service = VCdbService(db)
    base_vehicle = await service.get_base_vehicle(base_vehicle_id)
    return base_vehicle


@router.get("/base-vehicles/find")
async def find_base_vehicle(
    db: Annotated[AsyncSession, Depends(get_db)],
    year_id: int = Query(..., description="Year ID"),
    make_id: int = Query(..., description="Make ID"),
    model_id: int = Query(..., description="Model ID"),
) -> Optional[Dict[str, Any]]:
    """Find base vehicle by year, make, and model.

    Args:
        year_id: Year ID
        make_id: Make ID
        model_id: Model ID
        db: Database session

    Returns:
        Base vehicle details or None if not found
    """
    service = VCdbService(db)
    base_vehicle = await service.find_base_vehicle(year_id, make_id, model_id)
    return base_vehicle


@router.get("/base-vehicles/search")
async def search_base_vehicles(
    db: Annotated[AsyncSession, Depends(get_db)],
    year: Optional[int] = Query(None, description="Filter by year"),
    make: Optional[str] = Query(None, description="Filter by make name"),
    model: Optional[str] = Query(None, description="Filter by model name"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> Dict[str, Any]:
    """Search base vehicles.

    Args:
        year: Optional filter by year
        make: Optional filter by make name
        model: Optional filter by model name
        page: Page number for pagination
        page_size: Number of items per page
        db: Database session

    Returns:
        Paginated search results
    """
    service = VCdbService(db)
    result = await service.search_base_vehicles(
        year=year, make=make, model=model, page=page, page_size=page_size
    )
    return result


@router.get("/vehicles/search")
async def search_vehicles(
    db: Annotated[AsyncSession, Depends(get_db)],
    year: Optional[int] = Query(None, description="Filter by year"),
    make: Optional[str] = Query(None, description="Filter by make name"),
    model: Optional[str] = Query(None, description="Filter by model name"),
    submodel: Optional[str] = Query(None, description="Filter by submodel name"),
    engine_config: Optional[str] = Query(
        None, description="Filter by engine configuration"
    ),
    transmission_type: Optional[str] = Query(
        None, description="Filter by transmission type"
    ),
    body_type: Optional[str] = Query(None, description="Filter by body type"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> Dict[str, Any]:
    """Search vehicles.

    Args:
        year: Optional filter by year
        make: Optional filter by make name
        model: Optional filter by model name
        submodel: Optional filter by submodel name
        engine_config: Optional filter by engine configuration
        transmission_type: Optional filter by transmission type
        body_type: Optional filter by body type
        page: Page number for pagination
        page_size: Number of items per page
        db: Database session

    Returns:
        Paginated search results
    """
    service = VCdbService(db)
    result = await service.search_vehicles(
        year=year,
        make=make,
        model=model,
        submodel=submodel,
        engine_config=engine_config,
        transmission_type=transmission_type,
        body_type=body_type,
        page=page,
        page_size=page_size,
    )
    return result


@router.get("/vehicles/{vehicle_id}")
async def get_vehicle_by_id(
    vehicle_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get vehicle by ID.

    Args:
        vehicle_id: Vehicle ID
        db: Database session

    Returns:
        Vehicle details
    """
    service = VCdbService(db)
    vehicle = await service.get_vehicle_by_id(vehicle_id)
    return vehicle


@router.get("/vehicles/{vehicle_id}/details")
async def get_vehicle_details(
    vehicle_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get detailed information about a vehicle.

    Args:
        vehicle_id: Vehicle ID
        db: Database session

    Returns:
        Vehicle details
    """
    service = VCdbService(db)
    details = await service.get_vehicle_details(vehicle_id)
    return details


@router.get("/vehicles/{vehicle_id}/configurations")
async def get_vehicle_configurations(
    vehicle_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    use_config2: bool = Query(
        True, description="Use EngineConfig2 model instead of original EngineConfig"
    ),
) -> Dict[str, Any]:
    """Get configurations for a vehicle.

    Args:
        vehicle_id: Vehicle ID
        use_config2: Whether to use the newer EngineConfig2 model (default: True)
        db: Database session

    Returns:
        Vehicle configurations
    """
    service = VCdbService(db)

    if use_config2:
        configurations = await service.get_vehicle_configurations2(vehicle_id)
    else:
        configurations = await service.get_vehicle_configurations(vehicle_id)

    return configurations


@router.get("/engine-configs/{engine_config_id}")
async def get_engine_config(
    engine_config_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get engine configuration by ID.

    Args:
        engine_config_id: Engine configuration ID
        db: Database session

    Returns:
        Engine configuration details
    """
    service = VCdbService(db)
    engine_config = await service.get_engine_config(engine_config_id)
    return engine_config


@router.get("/engine-configs/search")
async def search_engine_configs(
    db: Annotated[AsyncSession, Depends(get_db)],
    engine_base_id: Optional[int] = Query(None, description="Filter by engine base ID"),
    fuel_type_id: Optional[int] = Query(None, description="Filter by fuel type ID"),
    aspiration_id: Optional[int] = Query(None, description="Filter by aspiration ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> Dict[str, Any]:
    """Search engine configurations.

    Args:
        engine_base_id: Optional filter by engine base ID
        fuel_type_id: Optional filter by fuel type ID
        aspiration_id: Optional filter by aspiration ID
        page: Page number for pagination
        page_size: Number of items per page
        db: Database session

    Returns:
        Paginated search results
    """
    service = VCdbService(db)
    result = await service.search_engine_configs(
        engine_base_id=engine_base_id,
        fuel_type_id=fuel_type_id,
        aspiration_id=aspiration_id,
        page=page,
        page_size=page_size,
    )
    return result


@router.get("/transmissions/{transmission_id}")
async def get_transmission(
    transmission_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get transmission by ID.

    Args:
        transmission_id: Transmission ID
        db: Database session

    Returns:
        Transmission details
    """
    service = VCdbService(db)
    transmission = await service.get_transmission(transmission_id)
    return transmission


@router.get("/transmissions/search")
async def search_transmissions(
    db: Annotated[AsyncSession, Depends(get_db)],
    transmission_type_id: Optional[int] = Query(
        None, description="Filter by transmission type ID"
    ),
    transmission_num_speeds_id: Optional[int] = Query(
        None, description="Filter by number of speeds ID"
    ),
    transmission_control_type_id: Optional[int] = Query(
        None, description="Filter by control type ID"
    ),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> Dict[str, Any]:
    """Search transmissions.

    Args:
        transmission_type_id: Optional filter by transmission type ID
        transmission_num_speeds_id: Optional filter by number of speeds ID
        transmission_control_type_id: Optional filter by control type ID
        page: Page number for pagination
        page_size: Number of items per page
        db: Database session

    Returns:
        Paginated search results
    """
    service = VCdbService(db)
    result = await service.search_transmissions(
        transmission_type_id=transmission_type_id,
        transmission_num_speeds_id=transmission_num_speeds_id,
        transmission_control_type_id=transmission_control_type_id,
        page=page,
        page_size=page_size,
    )
    return result


@router.get("/drive-types")
async def get_drive_types(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get all drive types.

    Args:
        db: Database session

    Returns:
        List of drive types
    """
    service = VCdbService(db)
    drive_types = await service.get_drive_types()
    return drive_types


@router.get("/body-style-configs/{body_style_config_id}")
async def get_body_style_config(
    body_style_config_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get body style configuration by ID.

    Args:
        body_style_config_id: Body style configuration ID
        db: Database session

    Returns:
        Body style configuration details
    """
    service = VCdbService(db)
    body_style_config = await service.get_body_style_config(body_style_config_id)
    return body_style_config


@router.get("/brake-configs/{brake_config_id}")
async def get_brake_config(
    brake_config_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get brake configuration by ID.

    Args:
        brake_config_id: Brake configuration ID
        db: Database session

    Returns:
        Brake configuration details
    """
    service = VCdbService(db)
    brake_config = await service.get_brake_config(brake_config_id)
    return brake_config


@router.get("/wheel-bases")
async def get_wheel_bases(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get all wheel bases.

    Args:
        db: Database session

    Returns:
        List of wheel bases
    """
    service = VCdbService(db)
    wheel_bases = await service.get_wheel_bases()
    return wheel_bases
