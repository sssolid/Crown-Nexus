# Module: app.domains.autocare.importers.base_importer

**Path:** `app/domains/autocare/importers/base_importer.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import abc
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Set
from sqlalchemy.ext.asyncio import AsyncSession
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.importers.base_importer")
T = T = TypeVar("T")
```

## Classes

| Class | Description |
| --- | --- |
| `BaseImporter` |  |

### Class: `BaseImporter`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `import_data` `async` |  |
| `validate_source` `async` |  |

##### `import_data`
```python
async def import_data(self) -> Dict[(str, Any)]:
```

##### `validate_source`
```python
async def validate_source(self) -> bool:
```
