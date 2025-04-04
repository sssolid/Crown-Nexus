# Module: app.domains.media.schemas

**Path:** `app/domains/media/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.media.models import MediaType, MediaVisibility
from app.core.config import settings
```

## Classes

| Class | Description |
| --- | --- |
| `FileUploadError` |  |
| `FileUploadResponse` |  |
| `Media` |  |
| `MediaBase` |  |
| `MediaCreate` |  |
| `MediaInDB` |  |
| `MediaListResponse` |  |
| `MediaUpdate` |  |

### Class: `FileUploadError`
**Inherits from:** BaseModel

### Class: `FileUploadResponse`
**Inherits from:** BaseModel

### Class: `Media`
**Inherits from:** MediaInDB

#### Methods

| Method | Description |
| --- | --- |
| `model_post_init` |  |

##### `model_post_init`
```python
def model_post_init(self, __context) -> None:
```

### Class: `MediaBase`
**Inherits from:** BaseModel

### Class: `MediaCreate`
**Inherits from:** BaseModel

### Class: `MediaInDB`
**Inherits from:** MediaBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `MediaListResponse`
**Inherits from:** BaseModel

### Class: `MediaUpdate`
**Inherits from:** BaseModel
