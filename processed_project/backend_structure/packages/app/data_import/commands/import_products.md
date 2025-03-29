# Module: app.data_import.commands.import_products

**Path:** `app/data_import/commands/import_products.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import json
import sys
from typing import Dict, Optional
import typer
from app.logging import get_logger
from app.data_import.connectors.file_connector import FileConnector, FileConnectionConfig
from app.data_import.connectors.filemaker_connector import FileMakerConnector, FileMakerConnectionConfig
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.pipeline.product_pipeline import ProductPipeline
from app.data_import.processors.product_processor import ProductMappingConfig, ProductProcessor
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
def import_products(source_type, config_file, query, dry_run, output_file, dsn, username, password, database, file_path, mapping_file, file_type, disable_ssl, limit) -> None:
```
