# Module: app.db.session

**Path:** `app/db/session.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import contextlib
from typing import AsyncGenerator, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
```

## Global Variables
```python
engine = engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,
    future=True,
    pool_pre_ping=True,  # Check connection validity before using from pool
)
async_session_maker = async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
)
```

## Functions

| Function | Description |
| --- | --- |
| `get_db` |  |
| `get_db_context` |  |

### `get_db`
```python
async def get_db() -> AsyncGenerator[(AsyncSession, None)]:
```

### `get_db_context`
```python
@contextlib.asynccontextmanager
async def get_db_context() -> AsyncGenerator[(AsyncSession, None)]:
```
