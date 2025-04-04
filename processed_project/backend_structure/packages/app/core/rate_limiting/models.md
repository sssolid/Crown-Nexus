# Module: app.core.rate_limiting.models

**Path:** `app/core/rate_limiting/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
```

## Classes

| Class | Description |
| --- | --- |
| `RateLimitRule` |  |
| `RateLimitStrategy` |  |

### Class: `RateLimitRule`
**Decorators:**
- `@dataclass`

### Class: `RateLimitStrategy`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `IP` | `'ip'` |
| `USER` | `'user'` |
| `COMBINED` | `'combined'` |
