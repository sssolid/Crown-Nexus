# Module: app.domains.autocare.commands.import_autocare

**Path:** `app/domains/autocare/commands/import_autocare.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import logging
import asyncio
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, cast
import typer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_context
from app.domains.autocare.importers.flexible_importer import SourceFormat, detect_source_format
from app.domains.autocare.importers.vcdb_importer import VCdbImporter
from app.domains.autocare.importers.pcdb_importer import PCdbImporter
from app.domains.autocare.importers.padb_importer import PAdbImporter
from app.domains.autocare.importers.qdb_importer import QdbImporter
from app.domains.sync_history.models import SyncEntityType, SyncSource, SyncStatus
from app.domains.sync_history.repository import SyncHistoryRepository
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.commands.import_autocare")
app = app = typer.Typer(help="Import AutoCare standard data into the application database.")
```

## Functions

| Function | Description |
| --- | --- |
| `display_import_result` |  |
| `get_database_source_dir` |  |
| `import_autocare` |  |
| `import_database` |  |
| `run_import` |  |

### `display_import_result`
```python
def display_import_result(db_name, result) -> None:
```

### `get_database_source_dir`
```python
def get_database_source_dir(source_dir, database) -> Path:
```

### `import_autocare`
```python
@app.command(name='import')
def import_autocare(database, source_dir, format, batch_size, dry_run, track_in_history, verbose) -> None:
```

### `import_database`
```python
async def import_database(db, database, source_dir, source_format, batch_size, dry_run, track_in_history, verbose) -> Dict:
```

### `run_import`
```python
async def run_import(database, source_dir, source_format, batch_size, dry_run, track_in_history, verbose) -> Union[(Dict, Dict[(str, Dict)])]:
```

## Classes

| Class | Description |
| --- | --- |
| `AutoCareDatabase` |  |

### Class: `AutoCareDatabase`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `VCDB` | `'vcdb'` |
| `PCDB` | `'pcdb'` |
| `PADB` | `'padb'` |
| `QDB` | `'qdb'` |
| `ALL` | `'all'` |
