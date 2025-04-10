# Module: app.db.alembic_command

**Path:** `app/db/alembic_command.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from alembic import command
from alembic.config import Config
from alembic.operations import Operations
from alembic.script import ScriptDirectory
```

## Global Variables
```python
command_name =     command_name = sys.argv[1]
revision_arg =         revision_arg = sys.argv[2] if len(sys.argv) > 2 else "-1"
message =         message = sys.argv[2] if len(sys.argv) > 2 else "auto-generated"
```

## Functions

| Function | Description |
| --- | --- |
| `downgrade` |  |
| `fix_self_referential_tables` |  |
| `get_alembic_config` |  |
| `post_process_migration_file` |  |
| `revision` |  |
| `upgrade` |  |

### `downgrade`
```python
def downgrade(config_path, revision) -> None:
```

### `fix_self_referential_tables`
```python
def fix_self_referential_tables(content) -> str:
```

### `get_alembic_config`
```python
def get_alembic_config(config_path) -> Config:
```

### `post_process_migration_file`
```python
def post_process_migration_file(alembic_cfg) -> None:
```

### `revision`
```python
def revision(config_path, message, autogenerate) -> None:
```

### `upgrade`
```python
def upgrade(config_path, revision) -> None:
```
