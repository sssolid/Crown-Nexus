# Module: app.core.permissions.models

**Path:** `app/core/permissions/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import enum
from typing import Dict, Set, TYPE_CHECKING
from app.domains.users.models import UserRole
```

## Classes

| Class | Description |
| --- | --- |
| `Permission` |  |
| `UserRole` |  |

### Class: `Permission`
**Inherits from:** str, enum.Enum

#### Attributes

| Name | Value |
| --- | --- |
| `USER_CREATE` | `'user:create'` |
| `USER_READ` | `'user:read'` |
| `USER_UPDATE` | `'user:update'` |
| `USER_DELETE` | `'user:delete'` |
| `USER_ADMIN` | `'user:admin'` |
| `PRODUCT_CREATE` | `'product:create'` |
| `PRODUCT_READ` | `'product:read'` |
| `PRODUCT_UPDATE` | `'product:update'` |
| `PRODUCT_DELETE` | `'product:delete'` |
| `PRODUCT_ADMIN` | `'product:admin'` |
| `MEDIA_CREATE` | `'media:create'` |
| `MEDIA_READ` | `'media:read'` |
| `MEDIA_UPDATE` | `'media:update'` |
| `MEDIA_DELETE` | `'media:delete'` |
| `MEDIA_ADMIN` | `'media:admin'` |
| `FITMENT_CREATE` | `'fitment:create'` |
| `FITMENT_READ` | `'fitment:read'` |
| `FITMENT_UPDATE` | `'fitment:update'` |
| `FITMENT_DELETE` | `'fitment:delete'` |
| `FITMENT_ADMIN` | `'fitment:admin'` |
| `COMPANY_CREATE` | `'company:create'` |
| `COMPANY_READ` | `'company:read'` |
| `COMPANY_UPDATE` | `'company:update'` |
| `COMPANY_DELETE` | `'company:delete'` |
| `COMPANY_ADMIN` | `'company:admin'` |
| `SYSTEM_ADMIN` | `'system:admin'` |

### Class: `UserRole`
**Inherits from:** str, enum.Enum

#### Attributes

| Name | Value |
| --- | --- |
| `ADMIN` | `'admin'` |
| `MANAGER` | `'manager'` |
| `CLIENT` | `'client'` |
| `DISTRIBUTOR` | `'distributor'` |
| `READ_ONLY` | `'read_only'` |
