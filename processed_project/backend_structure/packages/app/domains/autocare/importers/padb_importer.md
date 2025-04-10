# Module: app.domains.autocare.importers.padb_importer

**Path:** `app/domains/autocare/importers/padb_importer.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.autocare.importers.flexible_importer import FlexibleImporter, SourceFormat, detect_source_format
from app.domains.autocare.padb.models import PartAttribute, MetaData, MeasurementGroup, MetaUOMCode, PartAttributeAssignment, MetaUomCodeAssignment, ValidValue, ValidValueAssignment, Style, PartAttributeStyle, PartTypeStyle, PAdbVersion
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.importers.padb_importer")
```

## Classes

| Class | Description |
| --- | --- |
| `PAdbImporter` |  |

### Class: `PAdbImporter`
**Inherits from:** FlexibleImporter

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, db, source_path, source_format, batch_size):
```
