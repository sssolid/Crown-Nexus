from __future__ import annotations
import json
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, Query, UploadFile, status
from pydantic import BaseModel, Field
from app.logging import get_logger
from app.domains.model_mapping.schemas import ModelMapping as ModelMappingSchema
from app.domains.model_mapping.schemas import ModelMappingCreate, ModelMappingUpdate
from .exceptions import ConfigurationError, FitmentError
from .mapper import FitmentMappingEngine
from .models import ValidationStatus
logger = get_logger('app.fitment.api')
router = APIRouter(prefix='/api/v1/fitment', tags=['fitment'])
class ProcessFitmentRequest(BaseModel):
    application_texts: List[str] = Field(..., min_items=1)
    part_terminology_id: int = Field(...)
    product_id: Optional[str] = None
class FitmentValidationResponse(BaseModel):
    status: str
    message: str
    original_text: str
    suggestions: List[str] = Field(default_factory=list)
    fitment: Optional[Dict[str, Any]] = None
class ProcessFitmentResponse(BaseModel):
    results: Dict[str, List[FitmentValidationResponse]]
    valid_count: int
    warning_count: int
    error_count: int
class UploadModelMappingsResponse(BaseModel):
    message: str
    mapping_count: int
class ModelMappingRequest(BaseModel):
    pattern: str
    mapping: str
    priority: int = 0
    active: bool = True
class ModelMappingResponse(BaseModel):
    id: int
    pattern: str
    mapping: str
    priority: int
    active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
class ModelMappingsListResponse(BaseModel):
    items: List[ModelMappingResponse]
    total: int
def get_mapping_engine():
    from .dependencies import get_fitment_mapping_engine
    try:
        return get_fitment_mapping_engine()
    except Exception as e:
        logger.error(f'Failed to get mapping engine: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Fitment mapping engine not available') from e
@router.post('/process', response_model=ProcessFitmentResponse)
async def process_fitment(request: ProcessFitmentRequest=Body(...), mapping_engine: FitmentMappingEngine=Depends(get_mapping_engine)):
    try:
        results = mapping_engine.batch_process_applications(request.application_texts, request.part_terminology_id)
        valid_count = 0
        warning_count = 0
        error_count = 0
        serialized_results = {}
        for app_text, validation_results in results.items():
            serialized = mapping_engine.serialize_validation_results(validation_results)
            serialized_results[app_text] = serialized
            for result in validation_results:
                if result.status == ValidationStatus.VALID:
                    valid_count += 1
                elif result.status == ValidationStatus.WARNING:
                    warning_count += 1
                elif result.status == ValidationStatus.ERROR:
                    error_count += 1
        if request.product_id:
            all_results = []
            for app_results in results.values():
                all_results.extend(app_results)
            await mapping_engine.save_mapping_results(request.product_id, all_results)
        return {'results': serialized_results, 'valid_count': valid_count, 'warning_count': warning_count, 'error_count': error_count}
    except FitmentError as e:
        logger.error(f'Fitment error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': str(e), 'details': e.details}) from e
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'An unexpected error occurred: {str(e)}') from e
@router.post('/upload-model-mappings', response_model=UploadModelMappingsResponse)
async def upload_model_mappings(file: UploadFile=File(...), mapping_engine: FitmentMappingEngine=Depends(get_mapping_engine)):
    try:
        if not file.filename or not file.filename.endswith('.json'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid file format. Please upload a JSON file (.json)')
        content = await file.read()
        try:
            json_data = json.loads(content.decode('utf-8'))
            mapping_count = await mapping_engine.db_service.import_mappings_from_json(json_data)
            await mapping_engine.refresh_mappings()
            return {'message': 'Model mappings uploaded and configured successfully', 'mapping_count': mapping_count}
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Invalid JSON format: {str(e)}')
    except FitmentError as e:
        logger.error(f'Fitment error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': str(e), 'details': e.details}) from e
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'An unexpected error occurred: {str(e)}') from e
@router.get('/model-mappings', response_model=ModelMappingsListResponse)
async def list_model_mappings(mapping_engine: FitmentMappingEngine=Depends(get_mapping_engine), skip: int=Query(0, ge=0), limit: int=Query(100, gt=0, le=1000), pattern: Optional[str]=None, sort_by: Optional[str]=None, sort_order: Optional[str]=None):
    try:
        async with mapping_engine.db_service.get_session() as session:
            from app.domains.model_mapping.models import ModelMapping
            from sqlalchemy import or_, select, func, desc, asc
            query = select(ModelMapping)
            if pattern:
                query = query.where(ModelMapping.pattern.ilike(f'%{pattern}%'))
            count_query = select(func.count()).select_from(query.subquery())
            total = await session.scalar(count_query) or 0
            if sort_by:
                column_map = {'pattern': ModelMapping.pattern, 'mapping': ModelMapping.mapping, 'priority': ModelMapping.priority, 'active': ModelMapping.active, 'created_at': ModelMapping.created_at, 'updated_at': ModelMapping.updated_at}
                sort_field = column_map.get(sort_by, ModelMapping.pattern)
                if sort_order and sort_order.lower() == 'desc':
                    query = query.order_by(desc(sort_field))
                else:
                    query = query.order_by(asc(sort_field))
            else:
                query = query.order_by(ModelMapping.pattern, desc(ModelMapping.priority))
            query = query.offset(skip).limit(limit)
            result = await session.execute(query)
            items = result.scalars().all()
            return {'items': items, 'total': total}
    except Exception as e:
        logger.error(f'Error listing model mappings: {str(e)}', exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Failed to list model mappings: {str(e)}') from e
@router.post('/model-mappings', response_model=ModelMappingSchema, status_code=status.HTTP_201_CREATED)
async def create_model_mapping(mapping_data: ModelMappingCreate, mapping_engine: FitmentMappingEngine=Depends(get_mapping_engine)):
    try:
        mapping_id = await mapping_engine.db_service.add_model_mapping(mapping_data.pattern, mapping_data.mapping, mapping_data.priority)
        await mapping_engine.refresh_mappings()
        async with mapping_engine.db_service.get_session() as session:
            from app.domains.model_mapping.models import ModelMapping
            mapping = await session.get(ModelMapping, mapping_id)
            if not mapping:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mapping not found after creation')
            return mapping
    except HTTPException:
        raise
    except FitmentError as e:
        logger.error(f'Fitment error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': str(e), 'details': e.details}) from e
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'An unexpected error occurred: {str(e)}') from e
@router.put('/model-mappings/{mapping_id}', response_model=ModelMappingSchema)
async def update_model_mapping(mapping_id: int, mapping_data: ModelMappingUpdate, mapping_engine: FitmentMappingEngine=Depends(get_mapping_engine)):
    try:
        update_data = mapping_data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No fields to update')
        success = await mapping_engine.db_service.update_model_mapping(mapping_id, **update_data)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mapping not found')
        await mapping_engine.refresh_mappings()
        async with mapping_engine.db_service.get_session() as session:
            from app.domains.model_mapping.models import ModelMapping
            mapping = await session.get(ModelMapping, mapping_id)
            if not mapping:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mapping not found after update')
            return mapping
    except HTTPException:
        raise
    except FitmentError as e:
        logger.error(f'Fitment error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': str(e), 'details': e.details}) from e
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'An unexpected error occurred: {str(e)}') from e
@router.delete('/model-mappings/{mapping_id}', status_code=status.HTTP_200_OK)
async def delete_model_mapping(mapping_id: int, mapping_engine: FitmentMappingEngine=Depends(get_mapping_engine)):
    try:
        success = await mapping_engine.db_service.delete_model_mapping(mapping_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mapping not found')
        await mapping_engine.refresh_mappings()
        return {'message': 'Mapping deleted successfully'}
    except HTTPException:
        raise
    except FitmentError as e:
        logger.error(f'Fitment error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': str(e), 'details': e.details}) from e
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'An unexpected error occurred: {str(e)}') from e
@router.post('/refresh-mappings', status_code=status.HTTP_200_OK)
async def refresh_mappings(mapping_engine: FitmentMappingEngine=Depends(get_mapping_engine)):
    try:
        await mapping_engine.refresh_mappings()
        return {'message': 'Mappings refreshed successfully'}
    except FitmentError as e:
        logger.error(f'Fitment error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': str(e), 'details': e.details}) from e
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'An unexpected error occurred: {str(e)}') from e
@router.get('/pcdb-positions/{terminology_id}', response_model=List[Dict[str, Any]])
async def get_pcdb_positions(terminology_id: int=Path(...), mapping_engine: FitmentMappingEngine=Depends(get_mapping_engine)):
    try:
        positions = mapping_engine.get_pcdb_positions(terminology_id)
        serialized = []
        for pos in positions:
            serialized.append({'id': pos.id, 'name': pos.name, 'front_rear': pos.front_rear, 'left_right': pos.left_right, 'upper_lower': pos.upper_lower, 'inner_outer': pos.inner_outer})
        return serialized
    except FitmentError as e:
        logger.error(f'Fitment error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': str(e), 'details': e.details}) from e
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'An unexpected error occurred: {str(e)}') from e
@router.post('/parse-application', response_model=Dict[str, Any])
async def parse_application(application_text: str=Body(..., embed=True), mapping_engine: FitmentMappingEngine=Depends(get_mapping_engine)):
    try:
        if not mapping_engine.parser:
            raise ConfigurationError('Mapping engine not configured')
        part_app = mapping_engine.parser.parse_application(application_text)
        return {'raw_text': part_app.raw_text, 'year_range': part_app.year_range, 'vehicle_text': part_app.vehicle_text, 'position_text': part_app.position_text, 'additional_notes': part_app.additional_notes}
    except FitmentError as e:
        logger.error(f'Fitment error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'message': str(e), 'details': e.details}) from e
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'An unexpected error occurred: {str(e)}') from e