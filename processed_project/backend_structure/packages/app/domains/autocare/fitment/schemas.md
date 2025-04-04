# Module: app.domains.autocare.fitment.schemas

**Path:** `app/domains/autocare/fitment/schemas.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
```

## Classes

| Class | Description |
| --- | --- |
| `FitmentMapping` |  |
| `FitmentMappingCreate` |  |
| `FitmentMappingDetail` |  |
| `FitmentMappingHistory` |  |
| `FitmentMappingHistoryResponse` |  |
| `FitmentMappingSearchResponse` |  |
| `FitmentMappingUpdate` |  |
| `FitmentSearchParameters` |  |
| `ProductInfo` |  |

### Class: `FitmentMapping`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `FitmentMappingCreate`
**Inherits from:** BaseModel

### Class: `FitmentMappingDetail`
**Inherits from:** FitmentMapping

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `FitmentMappingHistory`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `FitmentMappingHistoryResponse`
**Inherits from:** BaseModel

### Class: `FitmentMappingSearchResponse`
**Inherits from:** BaseModel

### Class: `FitmentMappingUpdate`
**Inherits from:** BaseModel

### Class: `FitmentSearchParameters`
**Inherits from:** BaseModel

### Class: `ProductInfo`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |
