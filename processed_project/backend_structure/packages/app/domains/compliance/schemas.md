# Module: app.domains.compliance.schemas

**Path:** `app/domains/compliance/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import date, datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.compliance.models import ChemicalType, ExposureScenario, ApprovalStatus, TransportRestriction
```

## Classes

| Class | Description |
| --- | --- |
| `HazardousMaterial` |  |
| `HazardousMaterialBase` |  |
| `HazardousMaterialCreate` |  |
| `HazardousMaterialInDB` |  |
| `HazardousMaterialUpdate` |  |
| `ProductChemical` |  |
| `ProductChemicalBase` |  |
| `ProductChemicalCreate` |  |
| `ProductChemicalInDB` |  |
| `ProductChemicalUpdate` |  |
| `ProductDOTApproval` |  |
| `ProductDOTApprovalBase` |  |
| `ProductDOTApprovalCreate` |  |
| `ProductDOTApprovalInDB` |  |
| `ProductDOTApprovalUpdate` |  |
| `Prop65Chemical` |  |
| `Prop65ChemicalBase` |  |
| `Prop65ChemicalCreate` |  |
| `Prop65ChemicalInDB` |  |
| `Prop65ChemicalUpdate` |  |
| `Warning` |  |
| `WarningBase` |  |
| `WarningCreate` |  |
| `WarningInDB` |  |
| `WarningUpdate` |  |

### Class: `HazardousMaterial`
**Inherits from:** HazardousMaterialInDB

### Class: `HazardousMaterialBase`
**Inherits from:** BaseModel

### Class: `HazardousMaterialCreate`
**Inherits from:** HazardousMaterialBase

### Class: `HazardousMaterialInDB`
**Inherits from:** HazardousMaterialBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `HazardousMaterialUpdate`
**Inherits from:** BaseModel

### Class: `ProductChemical`
**Inherits from:** ProductChemicalInDB

### Class: `ProductChemicalBase`
**Inherits from:** BaseModel

### Class: `ProductChemicalCreate`
**Inherits from:** ProductChemicalBase

### Class: `ProductChemicalInDB`
**Inherits from:** ProductChemicalBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ProductChemicalUpdate`
**Inherits from:** BaseModel

### Class: `ProductDOTApproval`
**Inherits from:** ProductDOTApprovalInDB

### Class: `ProductDOTApprovalBase`
**Inherits from:** BaseModel

### Class: `ProductDOTApprovalCreate`
**Inherits from:** ProductDOTApprovalBase

### Class: `ProductDOTApprovalInDB`
**Inherits from:** ProductDOTApprovalBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ProductDOTApprovalUpdate`
**Inherits from:** BaseModel

### Class: `Prop65Chemical`
**Inherits from:** Prop65ChemicalInDB

### Class: `Prop65ChemicalBase`
**Inherits from:** BaseModel

### Class: `Prop65ChemicalCreate`
**Inherits from:** Prop65ChemicalBase

### Class: `Prop65ChemicalInDB`
**Inherits from:** Prop65ChemicalBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Prop65ChemicalUpdate`
**Inherits from:** BaseModel

### Class: `Warning`
**Inherits from:** WarningInDB

### Class: `WarningBase`
**Inherits from:** BaseModel

### Class: `WarningCreate`
**Inherits from:** WarningBase

### Class: `WarningInDB`
**Inherits from:** WarningBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `WarningUpdate`
**Inherits from:** BaseModel
