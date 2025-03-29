# Module: app.core.cache.keys

**Path:** `app/core/cache/keys.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import hashlib
import inspect
import json
import re
from typing import Any, Callable, Dict, List, Optional, Tuple
```

## Functions

| Function | Description |
| --- | --- |
| `generate_cache_key` |  |
| `generate_list_key` |  |
| `generate_model_key` |  |
| `generate_query_key` |  |
| `parse_pattern` |  |

### `generate_cache_key`
```python
def generate_cache_key(prefix, func, args, kwargs, skip_args, skip_kwargs) -> str:
```

### `generate_list_key`
```python
def generate_list_key(prefix, model_name, filters) -> str:
```

### `generate_model_key`
```python
def generate_model_key(prefix, model_name, model_id, field) -> str:
```

### `generate_query_key`
```python
def generate_query_key(prefix, query_name, params) -> str:
```

### `parse_pattern`
```python
def parse_pattern(pattern) -> re.Pattern:
```
