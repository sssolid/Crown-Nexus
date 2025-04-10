# Module: app.fitment.api

**Path:** `app/fitment/api.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, Query, UploadFile, status
from pydantic import BaseModel, Field
from app.logging import get_logger
from app.domains.model_mapping.schemas import ModelMapping as ModelMappingSchema
from app.domains.model_mapping.schemas import ModelMappingCreate, ModelMappingUpdate
from exceptions import ConfigurationError, FitmentError
from mapper import FitmentMappingEngine
from models import ValidationStatus
```

## Global Variables
```python
logger = logger = get_logger("app.fitment.api")
router = router = APIRouter(prefix="/api/v1/fitment", tags=["fitment"])
```

## Functions

| Function | Description |
| --- | --- |
| `create_model_mapping` |  |
| `delete_model_mapping` |  |
| `get_mapping_engine` |  |
| `get_pcdb_positions` |  |
| `list_model_mappings` |  |
| `parse_application` |  |
| `process_fitment` |  |
| `refresh_mappings` |  |
| `update_model_mapping` |  |
| `upload_model_mappings` |  |

### `create_model_mapping`
```python
@router.post('/model-mappings', response_model=ModelMappingSchema, status_code=status.HTTP_201_CREATED)
async def create_model_mapping(mapping_data, mapping_engine):
```

### `delete_model_mapping`
```python
@router.delete('/model-mappings/{mapping_id}', status_code=status.HTTP_200_OK)
async def delete_model_mapping(mapping_id, mapping_engine):
```

### `get_mapping_engine`
```python
def get_mapping_engine():
```

### `get_pcdb_positions`
```python
@router.get('/pcdb-positions/{terminology_id}', response_model=List[Dict[(str, Any)]])
async def get_pcdb_positions(terminology_id, mapping_engine):
```

### `list_model_mappings`
```python
@router.get('/model-mappings', response_model=ModelMappingsListResponse)
async def list_model_mappings(mapping_engine, skip, limit, pattern, sort_by, sort_order):
```

### `parse_application`
```python
@router.post('/parse-application', response_model=Dict[(str, Any)])
async def parse_application(application_text, mapping_engine):
```

### `process_fitment`
```python
@router.post('/process', response_model=ProcessFitmentResponse)
async def process_fitment(request, mapping_engine):
```

### `refresh_mappings`
```python
@router.post('/refresh-mappings', status_code=status.HTTP_200_OK)
async def refresh_mappings(mapping_engine):
```

### `update_model_mapping`
```python
@router.put('/model-mappings/{mapping_id}', response_model=ModelMappingSchema)
async def update_model_mapping(mapping_id, mapping_data, mapping_engine):
```

### `upload_model_mappings`
```python
@router.post('/upload-model-mappings', response_model=UploadModelMappingsResponse)
async def upload_model_mappings(file, mapping_engine):
```

## Classes

| Class | Description |
| --- | --- |
| `FitmentValidationResponse` |  |
| `ModelMappingRequest` |  |
| `ModelMappingResponse` |  |
| `ModelMappingsListResponse` |  |
| `ProcessFitmentRequest` |  |
| `ProcessFitmentResponse` |  |
| `UploadModelMappingsResponse` |  |

### Class: `FitmentValidationResponse`
**Inherits from:** BaseModel

### Class: `ModelMappingRequest`
**Inherits from:** BaseModel

### Class: `ModelMappingResponse`
**Inherits from:** BaseModel

### Class: `ModelMappingsListResponse`
**Inherits from:** BaseModel

### Class: `ProcessFitmentRequest`
**Inherits from:** BaseModel

### Class: `ProcessFitmentResponse`
**Inherits from:** BaseModel

### Class: `UploadModelMappingsResponse`
**Inherits from:** BaseModel
