# Module: app.data_import

**Path:** `app/data_import/__init__.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from app.db.base import Base
from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS, COMPLEX_FIELD_MAPPINGS, EntityFieldDefinitions, FieldDefinition, FieldType
from app.data_import.processors.processor_factory import create_processor, ProcessorFactory, EntityType, SourceType
```

## Global Variables
```python
__all__ = __all__ = [
    "ENTITY_FIELD_DEFINITIONS",
    "COMPLEX_FIELD_MAPPINGS",
    "EntityFieldDefinitions",
    "FieldDefinition",
    "FieldType",
    "create_processor",
    "ProcessorFactory",
    "EntityType",
    "SourceType",
]
```
