# Module: app.cli.autocare

**Path:** `app/cli/autocare.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import sys
import typer
from typing import List, Optional
from app.domains.autocare.commands.import_autocare import import_autocare
```

## Global Variables
```python
app = app = typer.Typer(help="Manage AutoCare standard data (VCdb, PCdb, PAdb, Qdb)")
```

## Functions

| Function | Description |
| --- | --- |
| `callback` |  |
| `main` |  |

### `callback`
```python
@app.callback()
def callback(verbose, version) -> None:
```

### `main`
```python
def main() -> None:
```
