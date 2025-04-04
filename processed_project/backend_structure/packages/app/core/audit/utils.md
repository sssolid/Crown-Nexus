# Module: app.core.audit.utils

**Path:** `app/core/audit/utils.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.core.audit.base import AuditEventType, AuditLogLevel
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.audit.utils")
```

## Functions

| Function | Description |
| --- | --- |
| `anonymize_data` |  |
| `format_audit_event` |  |
| `get_event_level_mapping` |  |
| `get_sensitive_fields` |  |

### `anonymize_data`
```python
def anonymize_data(data, sensitive_fields) -> Dict[(str, Any)]:
```

### `format_audit_event`
```python
def format_audit_event(event) -> str:
```

### `get_event_level_mapping`
```python
def get_event_level_mapping() -> Dict[(str, str)]:
```

### `get_sensitive_fields`
```python
def get_sensitive_fields() -> List[str]:
```
