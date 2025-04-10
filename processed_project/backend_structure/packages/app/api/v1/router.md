# Module: app.api.v1.router

**Path:** `app/api/v1/router.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from fastapi import APIRouter
from app.api.v1.endpoints import auth, fitments, media, products, search, users
from app.api.v1.endpoints.autocare import vcdb, padb, pcdb, qdb
```

## Global Variables
```python
api_router = api_router = APIRouter()
```
