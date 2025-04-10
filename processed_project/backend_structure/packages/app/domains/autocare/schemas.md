# Module: app.domains.autocare.schemas

**Path:** `app/domains/autocare/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator
```

## Classes

| Class | Description |
| --- | --- |
| `AutocareExportParams` |  |
| `AutocareImportParams` |  |
| `DataType` |  |
| `FileFormat` |  |
| `FitmentSearchParams` |  |
| `ImportMode` |  |
| `PaginatedResponse` |  |

### Class: `AutocareExportParams`
**Inherits from:** BaseModel

### Class: `AutocareImportParams`
**Inherits from:** BaseModel

### Class: `DataType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `VEHICLES` | `'vehicles'` |
| `PARTS` | `'parts'` |
| `FITMENTS` | `'fitments'` |
| `ALL` | `'all'` |

### Class: `FileFormat`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `ACES_XML` | `'aces_xml'` |
| `PIES_XML` | `'pies_xml'` |
| `CSV` | `'csv'` |
| `EXCEL` | `'excel'` |
| `JSON` | `'json'` |

### Class: `FitmentSearchParams`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_search_criteria` |  |

##### `validate_search_criteria`
```python
@model_validator(mode='after')
def validate_search_criteria(self) -> 'FitmentSearchParams':
```

### Class: `ImportMode`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `REPLACE` | `'replace'` |
| `MERGE` | `'merge'` |
| `UPDATE` | `'update'` |
| `INSERT` | `'insert'` |

### Class: `PaginatedResponse`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |
