# Module: app.core.celery_app

**Path:** `app/core/celery_app.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import os
from celery import Celery
from celery.schedules import crontab
```

## Global Variables
```python
celery_app = celery_app = Celery("crown_nexus")
```

## Functions

| Function | Description |
| --- | --- |
| `get_celery_app` |  |

### `get_celery_app`
```python
def get_celery_app() -> Celery:
```
