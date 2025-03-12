"""
API endpoints for fitment functionality.

This module provides the FastAPI endpoints for the fitment module.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.schemas.model_mapping import ModelMapping as ModelMappingSchema
from app.schemas.model_mapping import ModelMappingCreate, ModelMappingList, ModelMappingUpdate

from .exceptions import (
    ConfigurationError,
    DatabaseError,
    FitmentError,
    MappingError,
    ParsingError,
    ValidationError
)
from .mapper import FitmentMappingEngine
from .models import ValidationStatus


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/fitment", tags=["fitment"])


# API Models for request/response
class ProcessFitmentRequest(BaseModel):
    """Request body for processing fitment applications."""

    application_texts: List[str] = Field(..., min_items=1)
    part_terminology_id: int = Field(...)
    product_id: Optional[str] = None


class FitmentValidationResponse(BaseModel):
    """Response model for fitment validation results."""

    status: str
    message: str
    original_text: str
    suggestions: List[str] = Field(default_factory=list)
    fitment: Optional[Dict[str, Any]] = None


class ProcessFitmentResponse(BaseModel):
    """Response body for processing fitment applications."""

    results: Dict[str, List[FitmentValidationResponse]]
    valid_count: int
    warning_count: int
    error_count: int


class UploadModelMappingsResponse(BaseModel):
    """Response for model mappings upload."""

    message: str
    mapping_count: int


class ModelMappingRequest(BaseModel):
    """Request for creating or updating a model mapping."""

    pattern: str
    mapping: str
    priority: int = 0
    active: bool = True


class ModelMappingResponse(BaseModel):
    """Response for a model mapping."""

    id: int
    pattern: str
    mapping: str
    priority: int
    active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ModelMappingsListResponse(BaseModel):
    """Response for listing model mappings."""

    items: List[ModelMappingResponse]
    total: int


# Dependency for getting the mapping engine
def get_mapping_engine():
    """
    Get an instance of the mapping engine.

    This is a FastAPI dependency for endpoints that need the mapping engine.
    """
    from .dependencies import get_fitment_mapping_engine

    try:
        return get_fitment_mapping_engine()
    except Exception as e:
        logger.error(f"Failed to get mapping engine: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fitment mapping engine not available"
        ) from e


@router.post("/process", response_model=ProcessFitmentResponse)
async def process_fitment(
    request: ProcessFitmentRequest = Body(...),
    mapping_engine: FitmentMappingEngine = Depends(get_mapping_engine)
):
    """
    Process fitment application texts.

    Args:
        request: Request body with application texts and part terminology ID
        mapping_engine: Mapping engine instance

    Returns:
        Processing results

    Raises:
        HTTPException: If processing fails
    """
    try:
        # Process the applications
        results = mapping_engine.batch_process_applications(
            request.application_texts,
            request.part_terminology_id
        )

        # Count results by status
        valid_count = 0
        warning_count = 0
        error_count = 0

        serialized_results = {}

        for app_text, validation_results in results.items():
            serialized = mapping_engine.serialize_validation_results(validation_results)
            serialized_results[app_text] = serialized

            # Count by status
            for result in validation_results:
                if result.status == ValidationStatus.VALID:
                    valid_count += 1
                elif result.status == ValidationStatus.WARNING:
                    warning_count += 1
                elif result.status == ValidationStatus.ERROR:
                    error_count += 1

        # Save results if product_id provided
        if request.product_id:
            # Flatten all validation results
            all_results = []
            for app_results in results.values():
                all_results.extend(app_results)

            await mapping_engine.save_mapping_results(request.product_id, all_results)

        return {
            "results": serialized_results,
            "valid_count": valid_count,
            "warning_count": warning_count,
            "error_count": error_count
        }
    except FitmentError as e:
        logger.error(f"Fitment error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "details": e.details}
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e


@router.post("/upload-model-mappings", response_model=UploadModelMappingsResponse)
async def upload_model_mappings(
    file: UploadFile = File(...),
    mapping_engine: FitmentMappingEngine = Depends(get_mapping_engine)
):
    """
    Upload model mappings JSON file.

    Args:
        file: JSON file with model mappings
        mapping_engine: Mapping engine instance

    Returns:
        Upload result

    Raises:
        HTTPException: If upload fails
    """
    try:
        # Verify file type
        if not file.filename or not file.filename.endswith(".json"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Please upload a JSON file (.json)"
            )

        # Read the file content
        content = await file.read()

        try:
            # Parse JSON
            json_data = json.loads(content.decode('utf-8'))

            # Import mappings to database
            mapping_count = await mapping_engine.db_service.import_mappings_from_json(json_data)

            # Refresh mappings in the engine
            await mapping_engine.refresh_mappings()

            return {
                "message": "Model mappings uploaded and configured successfully",
                "mapping_count": mapping_count
            }
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid JSON format: {str(e)}"
            )

    except FitmentError as e:
        logger.error(f"Fitment error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "details": e.details}
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e


@router.get("/model-mappings", response_model=ModelMappingList)
async def list_model_mappings(
    mapping_engine: FitmentMappingEngine = Depends(get_mapping_engine),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0, le=1000),
    pattern: Optional[str] = None
):
    """
    List model mappings from database.

    Args:
        mapping_engine: Mapping engine instance
        skip: Number of items to skip (for pagination)
        limit: Maximum number of items to return (for pagination)
        pattern: Optional pattern to filter by

    Returns:
        List of model mappings with pagination information

    Raises:
        HTTPException: If retrieval fails
    """
    try:
        async with mapping_engine.db_service.get_session() as session:
            from app.models.model_mapping import ModelMapping
            from sqlalchemy import or_, select, func
            import logging

            # Log pagination parameters for debugging
            logger = logging.getLogger(__name__)
            logger.info(f"Model mappings request - skip: {skip}, limit: {limit}, pattern: {pattern}")

            # Build query
            query = select(ModelMapping)

            # Add pattern filter if provided
            if pattern:
                query = query.where(ModelMapping.pattern.ilike(f"%{pattern}%"))

            # Count total before pagination
            count_query = select(func.count()).select_from(query.subquery())
            total = await session.scalar(count_query) or 0
            logger.info(f"Total mappings before pagination: {total}")

            # Add pagination and ordering
            query = query.order_by(ModelMapping.pattern, ModelMapping.priority.desc())
            query = query.offset(skip).limit(limit)

            # Execute query
            result = await session.execute(query)
            items = result.scalars().all()
            logger.info(f"Returning {len(items)} items")

            return {
                "items": items,
                "total": total
            }
    except Exception as e:
        logger.error(f"Error listing model mappings: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list model mappings: {str(e)}"
        ) from e


@router.post("/model-mappings", response_model=ModelMappingSchema, status_code=status.HTTP_201_CREATED)
async def create_model_mapping(
    mapping_data: ModelMappingCreate,
    mapping_engine: FitmentMappingEngine = Depends(get_mapping_engine)
):
    """
    Create a new model mapping.

    Args:
        mapping_data: Mapping data
        mapping_engine: Mapping engine instance

    Returns:
        Created mapping

    Raises:
        HTTPException: If creation fails
    """
    try:
        # Create mapping in database
        mapping_id = await mapping_engine.db_service.add_model_mapping(
            mapping_data.pattern,
            mapping_data.mapping,
            mapping_data.priority
        )

        # Refresh mappings in the engine
        await mapping_engine.refresh_mappings()

        # Return the created mapping
        async with mapping_engine.db_service.get_session() as session:
            from app.models.model_mapping import ModelMapping

            mapping = await session.get(ModelMapping, mapping_id)
            if not mapping:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Mapping not found after creation"
                )

            return mapping
    except HTTPException:
        raise
    except FitmentError as e:
        logger.error(f"Fitment error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "details": e.details}
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e


@router.put("/model-mappings/{mapping_id}", response_model=ModelMappingSchema)
async def update_model_mapping(
    mapping_id: int,
    mapping_data: ModelMappingUpdate,
    mapping_engine: FitmentMappingEngine = Depends(get_mapping_engine)
):
    """
    Update an existing model mapping.

    Args:
        mapping_id: ID of the mapping to update
        mapping_data: Updated mapping data
        mapping_engine: Mapping engine instance

    Returns:
        Updated mapping

    Raises:
        HTTPException: If update fails
    """
    try:
        # Update fields that are not None
        update_data = mapping_data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        # Update mapping in database
        success = await mapping_engine.db_service.update_model_mapping(
            mapping_id,
            **update_data
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mapping not found"
            )

        # Refresh mappings in the engine
        await mapping_engine.refresh_mappings()

        # Return the updated mapping
        async with mapping_engine.db_service.get_session() as session:
            from app.models.model_mapping import ModelMapping

            mapping = await session.get(ModelMapping, mapping_id)
            if not mapping:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Mapping not found after update"
                )

            return mapping
    except HTTPException:
        raise
    except FitmentError as e:
        logger.error(f"Fitment error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "details": e.details}
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e


@router.delete("/model-mappings/{mapping_id}", status_code=status.HTTP_200_OK)
async def delete_model_mapping(
    mapping_id: int,
    mapping_engine: FitmentMappingEngine = Depends(get_mapping_engine)
):
    """
    Delete a model mapping.

    Args:
        mapping_id: ID of the mapping to delete
        mapping_engine: Mapping engine instance

    Returns:
        Success message

    Raises:
        HTTPException: If deletion fails
    """
    try:
        # Delete mapping from database
        success = await mapping_engine.db_service.delete_model_mapping(mapping_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mapping not found"
            )

        # Refresh mappings in the engine
        await mapping_engine.refresh_mappings()

        return {"message": "Mapping deleted successfully"}
    except HTTPException:
        raise
    except FitmentError as e:
        logger.error(f"Fitment error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "details": e.details}
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e


@router.post("/refresh-mappings", status_code=status.HTTP_200_OK)
async def refresh_mappings(
    mapping_engine: FitmentMappingEngine = Depends(get_mapping_engine)
):
    """
    Refresh model mappings from the database.

    This allows for updating mappings without restarting the server.

    Args:
        mapping_engine: Mapping engine instance

    Returns:
        Success message

    Raises:
        HTTPException: If refresh fails
    """
    try:
        # Refresh mappings in the engine
        await mapping_engine.refresh_mappings()

        return {"message": "Mappings refreshed successfully"}
    except FitmentError as e:
        logger.error(f"Fitment error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "details": e.details}
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e


@router.get("/pcdb-positions/{terminology_id}", response_model=List[Dict[str, Any]])
async def get_pcdb_positions(
    terminology_id: int = Path(...),
    mapping_engine: FitmentMappingEngine = Depends(get_mapping_engine)
):
    """
    Get PCDB positions for a part terminology.

    Args:
        terminology_id: Part terminology ID
        mapping_engine: Mapping engine instance

    Returns:
        List of PCDB positions

    Raises:
        HTTPException: If retrieval fails
    """
    try:
        positions = mapping_engine.get_pcdb_positions(terminology_id)

        # Convert to dictionaries
        serialized = []
        for pos in positions:
            serialized.append({
                "id": pos.id,
                "name": pos.name,
                "front_rear": pos.front_rear,
                "left_right": pos.left_right,
                "upper_lower": pos.upper_lower,
                "inner_outer": pos.inner_outer
            })

        return serialized
    except FitmentError as e:
        logger.error(f"Fitment error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "details": e.details}
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e


@router.post("/parse-application", response_model=Dict[str, Any])
async def parse_application(
    application_text: str = Body(..., embed=True),
    mapping_engine: FitmentMappingEngine = Depends(get_mapping_engine)
):
    """
    Parse a part application text.

    Args:
        application_text: Raw part application text
        mapping_engine: Mapping engine instance

    Returns:
        Parsed application components

    Raises:
        HTTPException: If parsing fails
    """
    try:
        if not mapping_engine.parser:
            raise ConfigurationError("Mapping engine not configured")

        part_app = mapping_engine.parser.parse_application(application_text)

        return {
            "raw_text": part_app.raw_text,
            "year_range": part_app.year_range,
            "vehicle_text": part_app.vehicle_text,
            "position_text": part_app.position_text,
            "additional_notes": part_app.additional_notes
        }
    except FitmentError as e:
        logger.error(f"Fitment error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": str(e), "details": e.details}
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e
