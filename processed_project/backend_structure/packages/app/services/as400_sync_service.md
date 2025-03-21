# Module: app.services.as400_sync_service

**Path:** `app/services/as400_sync_service.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import time
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Type, cast
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config.integrations.as400 import AS400Settings, as400_settings, get_as400_connector_config
from app.core.exceptions import AppException, ConfigurationException
from app.core.logging import get_logger
from app.data_import.connectors.as400_connector import AS400Connector, AS400ConnectionConfig
from app.data_import.pipeline.as400_pipeline import AS400Pipeline, ParallelAS400Pipeline
from app.db.session import async_session_maker, get_db_context
from app.models.audit import AuditLog
from app.models.product import Product, ProductMeasurement, ProductStock
from app.models.reference import Warehouse
from app.schemas.product import ProductCreate, ProductMeasurementCreate, ProductStock as ProductStockSchema
from app.data_import.processors.as400_processor import AS400ProcessorConfig, ProductAS400Processor, PricingAS400Processor, InventoryAS400Processor
from app.data_import.importers.as400_importers import ProductAS400Importer, ProductMeasurementImporter, ProductStockImporter, ProductPricingImporter
```

## Global Variables
```python
logger = logger = get_logger("app.services.as400_sync_service")
as400_sync_service = as400_sync_service = AS400SyncService.get_instance()
```

## Classes

| Class | Description |
| --- | --- |
| `AS400SyncService` |  |
| `SyncEntityType` |  |
| `SyncLog` |  |
| `SyncStatus` |  |

### Class: `AS400SyncService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_instance` |  |
| `get_sync_status` `async` |  |
| `initialize` `async` |  |
| `run_sync` `async` |  |
| `schedule_sync` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `get_instance`
```python
@classmethod
def get_instance(cls) -> AS400SyncService:
```

##### `get_sync_status`
```python
async def get_sync_status(self, entity_type) -> Dict[(str, Any)]:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `run_sync`
```python
async def run_sync(self, entity_type, force) -> Dict[(str, Any)]:
```

##### `schedule_sync`
```python
async def schedule_sync(self, entity_type, delay_seconds) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

### Class: `SyncEntityType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `PRODUCT` | `'product'` |
| `MEASUREMENT` | `'measurement'` |
| `STOCK` | `'stock'` |
| `PRICING` | `'pricing'` |
| `MANUFACTURER` | `'manufacturer'` |
| `CUSTOMER` | `'customer'` |
| `ORDER` | `'order'` |

### Class: `SyncLog`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `complete` |  |

##### `__init__`
```python
def __init__(self, entity_type, status, records_processed, records_created, records_updated, records_failed, started_at, completed_at, error_message) -> None:
```

##### `complete`
```python
def complete(self, status, records_processed, records_created, records_updated, records_failed, error_message) -> None:
```

### Class: `SyncStatus`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `PENDING` | `'pending'` |
| `RUNNING` | `'running'` |
| `COMPLETED` | `'completed'` |
| `FAILED` | `'failed'` |
| `CANCELLED` | `'cancelled'` |
