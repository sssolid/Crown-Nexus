# Module: manage_db

**Path:** `manage_db.py`

[Back to Project Index](../index.md)

## Imports
```python
from __future__ import annotations
import argparse
import logging
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, cast
from sqlalchemy import MetaData, create_engine, inspect, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.schema import Column, CreateTable, ForeignKey, Table
from app.core.config import settings
from app.db.base import Base
```

## Global Variables
```python
logger = logger = logging.getLogger(__name__)
```

## Functions

| Function | Description |
| --- | --- |
| `execute_sql` |  |
| `find_problematic_tables` |  |
| `get_engine` |  |
| `handle_create` |  |
| `handle_downgrade` |  |
| `handle_stamp` |  |
| `handle_upgrade` |  |
| `initialize_alembic` |  |
| `main` |  |
| `reset_database` |  |
| `run_alembic_command` |  |
| `sort_tables_by_dependency` |  |

### `execute_sql`
```python
def execute_sql(sql, description) -> bool:
```

### `find_problematic_tables`
```python
def find_problematic_tables() -> Dict[(str, List[Tuple[(str, str)]])]:
```

### `get_engine`
```python
def get_engine() -> Engine:
```

### `handle_create`
```python
def handle_create(message) -> bool:
```

### `handle_downgrade`
```python
def handle_downgrade(revision) -> bool:
```

### `handle_stamp`
```python
def handle_stamp(revision) -> bool:
```

### `handle_upgrade`
```python
def handle_upgrade(revision) -> bool:
```

### `initialize_alembic`
```python
def initialize_alembic() -> bool:
```

### `main`
```python
def main() -> None:
```

### `reset_database`
```python
def reset_database() -> bool:
```

### `run_alembic_command`
```python
def run_alembic_command(command, *args) -> bool:
```

### `sort_tables_by_dependency`
```python
def sort_tables_by_dependency() -> List[str]:
```
