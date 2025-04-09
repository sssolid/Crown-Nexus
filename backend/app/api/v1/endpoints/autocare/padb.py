# processed_project/backend_stripped/app/api/v1/endpoints/padb.py
from __future__ import annotations

"""PADB API endpoints for accessing Part Attribute Database.

This module provides HTTP endpoints for interacting with PADB data,
including part attributes, measurement groups, UOM codes, and valid values.
"""

from typing import Annotated, Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db, get_pagination
from app.api.responses import paginated_response, success_response
from app.domains.autocare.padb.service import PAdbService
from app.domains.users.models import User

router = APIRouter()


@router.get("/version")
async def get_version(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> str:
    """Get the current PADB version.

    Args:
        db: Database session

    Returns:
        Current PADB version as string
    """
    service = PAdbService(db)
    version = await service.get_version()
    return version


@router.get("/attributes/search")
async def search_attributes(
    db: Annotated[AsyncSession, Depends(get_db)],
    search_term: Optional[str] = Query(None, description="Search term for attributes"),
    part_terminology_id: Optional[int] = Query(None, description="Filter by part terminology ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> Dict[str, Any]:
    """Search part attributes.

    Args:
        search_term: Text to search for
        part_terminology_id: Optional filter by part terminology ID
        page: Page number for pagination
        page_size: Number of items per page
        db: Database session

    Returns:
        Paginated search results
    """
    service = PAdbService(db)
    result = await service.search_attributes(
        search_term=search_term,
        part_terminology_id=part_terminology_id,
        page=page,
        page_size=page_size,
    )
    return result


@router.get("/attributes/{pa_id}")
async def get_attribute_details(
    pa_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get detailed information about a part attribute.

    Args:
        pa_id: ID of the part attribute
        db: Database session

    Returns:
        Part attribute details
    """
    service = PAdbService(db)
    details = await service.get_attribute_details(pa_id)
    return details


@router.get("/parts/{part_terminology_id}/attributes")
async def get_part_attributes(
    part_terminology_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Dict[str, Any]:
    """Get attributes for a part.

    Args:
        part_terminology_id: ID of the part
        db: Database session

    Returns:
        Part attributes
    """
    service = PAdbService(db)
    attributes = await service.get_part_attributes(part_terminology_id)
    return attributes


@router.get("/measurement-groups")
async def get_measurement_groups(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get all measurement groups.

    Args:
        db: Database session

    Returns:
        List of measurement groups
    """
    service = PAdbService(db)
    groups = await service.get_measurement_groups()
    return groups


@router.get("/measurement-groups/{measurement_group_id}/uom-codes")
async def get_uom_codes_by_measurement_group(
    measurement_group_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get UOM codes by measurement group.

    Args:
        measurement_group_id: ID of the measurement group
        db: Database session

    Returns:
        List of UOM codes
    """
    service = PAdbService(db)
    uom_codes = await service.get_uom_codes_by_measurement_group(measurement_group_id)
    return uom_codes


@router.get("/attribute-assignments/{papt_id}/valid-values")
async def get_valid_values_for_attribute(
    papt_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> List[Dict[str, Any]]:
    """Get valid values for an attribute assignment.

    Args:
        papt_id: ID of the part attribute assignment
        db: Database session

    Returns:
        List of valid values
    """
    service = PAdbService(db)
    valid_values = await service.get_valid_values_for_attribute(papt_id)
    return valid_values
