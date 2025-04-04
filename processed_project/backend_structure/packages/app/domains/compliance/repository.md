# Module: app.domains.compliance.repository

**Path:** `app/domains/compliance/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.compliance.models import Prop65Chemical, Warning, ProductChemical, ProductDOTApproval, HazardousMaterial, ApprovalStatus, ChemicalType, ExposureScenario
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

## Classes

| Class | Description |
| --- | --- |
| `HazardousMaterialRepository` |  |
| `ProductChemicalRepository` |  |
| `ProductDOTApprovalRepository` |  |
| `Prop65ChemicalRepository` |  |
| `WarningRepository` |  |

### Class: `HazardousMaterialRepository`
**Inherits from:** BaseRepository[(HazardousMaterial, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_product` `async` |  |
| `find_by_un_number` `async` |  |
| `get_by_hazard_class` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, hazmat_id) -> HazardousMaterial:
```

##### `find_by_product`
```python
async def find_by_product(self, product_id) -> Optional[HazardousMaterial]:
```

##### `find_by_un_number`
```python
async def find_by_un_number(self, un_number) -> List[HazardousMaterial]:
```

##### `get_by_hazard_class`
```python
async def get_by_hazard_class(self, hazard_class) -> List[HazardousMaterial]:
```

### Class: `ProductChemicalRepository`
**Inherits from:** BaseRepository[(ProductChemical, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_product_and_chemical` `async` |  |
| `get_by_exposure_scenario` `async` |  |
| `get_by_product` `async` |  |
| `get_products_with_warnings` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, association_id) -> ProductChemical:
```

##### `find_by_product_and_chemical`
```python
async def find_by_product_and_chemical(self, product_id, chemical_id) -> Optional[ProductChemical]:
```

##### `get_by_exposure_scenario`
```python
async def get_by_exposure_scenario(self, scenario) -> List[ProductChemical]:
```

##### `get_by_product`
```python
async def get_by_product(self, product_id) -> List[ProductChemical]:
```

##### `get_products_with_warnings`
```python
async def get_products_with_warnings(self) -> List[uuid.UUID]:
```

### Class: `ProductDOTApprovalRepository`
**Inherits from:** BaseRepository[(ProductDOTApproval, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_approval_number` `async` |  |
| `find_by_product` `async` |  |
| `get_by_status` `async` |  |
| `get_expiring_soon` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, approval_id) -> ProductDOTApproval:
```

##### `find_by_approval_number`
```python
async def find_by_approval_number(self, approval_number) -> Optional[ProductDOTApproval]:
```

##### `find_by_product`
```python
async def find_by_product(self, product_id) -> Optional[ProductDOTApproval]:
```

##### `get_by_status`
```python
async def get_by_status(self, status) -> List[ProductDOTApproval]:
```

##### `get_expiring_soon`
```python
async def get_expiring_soon(self, days) -> List[ProductDOTApproval]:
```

### Class: `Prop65ChemicalRepository`
**Inherits from:** BaseRepository[(Prop65Chemical, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_cas_number` `async` |  |
| `find_by_name` `async` |  |
| `get_by_type` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, chemical_id) -> Prop65Chemical:
```

##### `find_by_cas_number`
```python
async def find_by_cas_number(self, cas_number) -> Optional[Prop65Chemical]:
```

##### `find_by_name`
```python
async def find_by_name(self, name) -> List[Prop65Chemical]:
```

##### `get_by_type`
```python
async def get_by_type(self, chemical_type) -> List[Prop65Chemical]:
```

### Class: `WarningRepository`
**Inherits from:** BaseRepository[(Warning, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `get_by_chemical` `async` |  |
| `get_by_product` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, warning_id) -> Warning:
```

##### `get_by_chemical`
```python
async def get_by_chemical(self, chemical_id) -> List[Warning]:
```

##### `get_by_product`
```python
async def get_by_product(self, product_id) -> List[Warning]:
```
