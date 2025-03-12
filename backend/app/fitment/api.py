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
    Upload model mappings Excel file.

    Args:
        file: Excel file with model mappings
        mapping_engine: Mapping engine instance

    Returns:
        Upload result

    Raises:
        HTTPException: If upload fails
    """
    try:
        # Verify file type
        if not file.filename or not (
            file.filename.endswith(".xlsx") or
            file.filename.endswith(".xls")
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Please upload an Excel file (.xlsx or .xls)"
            )

        # Save file temporarily
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Configure mapping engine with new mappings
            mapping_engine.configure(temp_file_path)

            # Count mappings
            mapping_count = sum(len(mappings) for mappings in mapping_engine.model_mappings.values())

            return {
                "message": "Model mappings uploaded and configured successfully",
                "mapping_count": mapping_count
            }
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)

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
