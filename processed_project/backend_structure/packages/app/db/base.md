# Module: app.db.base

**Path:** `app/db/base.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from app.db.base_class import Base
import app.domains.sync_history.models
import app.domains.location.models
import app.domains.api_key.models
import app.domains.users.models
import app.domains.company.models
import app.domains.chat.models
import app.domains.currency.models
import app.domains.media.models
import app.domains.compliance.models
import app.domains.model_mapping.models
import app.domains.products.associations
import app.domains.products.models
import app.domains.autocare.fitment.models
import app.domains.autocare.padb.models
import app.domains.autocare.pcdb.models
import app.domains.autocare.qdb.models
import app.domains.autocare.vcdb.models
import app.domains.reference.models
import app.core.audit.models
from sqlalchemy.orm import configure_mappers
import sys
```
