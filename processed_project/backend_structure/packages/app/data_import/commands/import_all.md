# Module: app.data_import.commands.import_all

**Path:** `app/data_import/commands/import_all.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import json
import sys
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import typer
from sqlalchemy import select
from app.core.config.integrations.as400 import get_as400_connector_config
from app.core.config.integrations.filemaker import get_filemaker_connector_config
from app.data_import import create_processor, EntityType, SourceType
from app.data_import.connectors.as400_connector import AS400ConnectionConfig, AS400Connector
from app.data_import.connectors.file_connector import FileConnectionConfig, FileConnector
from app.data_import.connectors.filemaker_connector import FileMakerConnectionConfig, FileMakerConnector
from app.data_import.field_definitions import generate_query_for_entity
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.pipeline.product_pipeline import ProductPipeline
from app.db.session import get_db_context
from app.domains.sync_history.models import SyncEntityType, SyncSource, SyncStatus
from app.domains.sync_history.repository import SyncHistoryRepository
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.commands.import_all")
app = app = typer.Typer()
```

## Functions

| Function | Description |
| --- | --- |
| `configure_logging` |  |
| `import_all` |  |
| `resolve_system_user_id` |  |

### `configure_logging`
```python
def configure_logging(verbosity) -> None:
```

### `import_all`
```python
@app.command()
def import_all(source_type, config_file, dry_run, output_dir, file_path, file_type, limit, verbosity, system_user, notify_users, entity_types) -> None:
```

### `resolve_system_user_id`
```python
def resolve_system_user_id(user_id) -> Optional[uuid.UUID]:
```

## Classes

| Class | Description |
| --- | --- |
| `LoggingVerbosity` |  |

### Class: `LoggingVerbosity`

#### Attributes

| Name | Value |
| --- | --- |
| `QUIET` | `'quiet'` |
| `NORMAL` | `'normal'` |
| `VERBOSE` | `'verbose'` |
| `DEBUG` | `'debug'` |
