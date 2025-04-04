# Module: app.data_import.commands.import_products

**Path:** `app/data_import/commands/import_products.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import json
import sys
import time
from typing import Dict, List, Optional, Any
import typer
from app.logging import get_logger
from app.core.config.integrations.filemaker import get_filemaker_connector_config
from app.core.config.integrations.as400 import get_as400_connector_config
from app.data_import.connectors.file_connector import FileConnector, FileConnectionConfig
from app.data_import.connectors.filemaker_connector import FileMakerConnector, FileMakerConnectionConfig
from app.data_import.connectors.as400_connector import AS400Connector, AS400ConnectionConfig
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.pipeline.product_pipeline import ProductPipeline
from app.data_import import create_processor, EntityType, SourceType
from app.data_import.field_definitions import generate_query_for_entity
from app.db.session import get_db_context
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.commands.import_products")
app = app = typer.Typer()
```

## Functions

| Function | Description |
| --- | --- |
| `import_products` |  |

### `import_products`
```python
@app.command()
def import_products(source_type, entity_type, config_file, custom_query, dry_run, output_file, file_path, file_type, limit, fields) -> None:
```
