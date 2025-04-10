# Module: app.domains.media.models

**Path:** `app/domains/media/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, Enum as SQLAEnum, ForeignKey, Integer, String, func, text, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.domains.products.models import Product
from app.domains.users.models import User
```

## Classes

| Class | Description |
| --- | --- |
| `Media` |  |
| `MediaType` |  |
| `MediaVisibility` |  |

### Class: `Media`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'media'` |
| `__table_args__` | `    __table_args__ = {"schema": "media"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |
| `extension` `@property` |  |
| `has_thumbnail` `@property` |  |
| `is_image` `@property` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

##### `extension`
```python
@property
def extension(self) -> str:
```

##### `has_thumbnail`
```python
@property
def has_thumbnail(self) -> bool:
```

##### `is_image`
```python
@property
def is_image(self) -> bool:
```

### Class: `MediaType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `IMAGE` | `'image'` |
| `DOCUMENT` | `'document'` |
| `VIDEO` | `'video'` |
| `MSDS` | `'msds'` |
| `DOT_APPROVAL` | `'dot_approval'` |
| `OTHER` | `'other'` |

### Class: `MediaVisibility`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `PUBLIC` | `'public'` |
| `PRIVATE` | `'private'` |
| `RESTRICTED` | `'restricted'` |
