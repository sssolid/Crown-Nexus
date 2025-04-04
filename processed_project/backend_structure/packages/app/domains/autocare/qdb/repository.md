# Module: app.domains.autocare.qdb.repository

**Path:** `app/domains/autocare/qdb/repository.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.qdb.models import QualifierType, Qualifier, Language, QualifierTranslation, GroupNumber, QualifierGroup, QdbVersion
```

## Classes

| Class | Description |
| --- | --- |
| `GroupNumberRepository` |  |
| `LanguageRepository` |  |
| `QdbRepository` |  |
| `QualifierRepository` |  |
| `QualifierTypeRepository` |  |

### Class: `GroupNumberRepository`
**Inherits from:** BaseRepository[(GroupNumber, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_groups` `async` |  |
| `get_by_group_number_id` `async` |  |
| `get_qualifiers_by_group` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_groups`
```python
async def get_all_groups(self) -> List[GroupNumber]:
```

##### `get_by_group_number_id`
```python
async def get_by_group_number_id(self, group_number_id) -> Optional[GroupNumber]:
```

##### `get_qualifiers_by_group`
```python
async def get_qualifiers_by_group(self, group_number_id, page, page_size) -> Dict[(str, Any)]:
```

### Class: `LanguageRepository`
**Inherits from:** BaseRepository[(Language, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_languages` `async` |  |
| `get_by_language_id` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_languages`
```python
async def get_all_languages(self) -> List[Language]:
```

##### `get_by_language_id`
```python
async def get_by_language_id(self, language_id) -> Optional[Language]:
```

### Class: `QdbRepository`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_version` `async` |  |
| `search_qualifiers` `async` |  |
| `update_version` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_version`
```python
async def get_version(self) -> Optional[str]:
```

##### `search_qualifiers`
```python
async def search_qualifiers(self, search_term, qualifier_type_id, language_id, page, page_size) -> Dict[(str, Any)]:
```

##### `update_version`
```python
async def update_version(self, version_date) -> QdbVersion:
```

### Class: `QualifierRepository`
**Inherits from:** BaseRepository[(Qualifier, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_qualifier_id` `async` |  |
| `get_groups` `async` |  |
| `get_translations` `async` |  |
| `search` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_qualifier_id`
```python
async def get_by_qualifier_id(self, qualifier_id) -> Optional[Qualifier]:
```

##### `get_groups`
```python
async def get_groups(self, qualifier_id) -> List[Dict[(str, Any)]]:
```

##### `get_translations`
```python
async def get_translations(self, qualifier_id, language_id) -> List[QualifierTranslation]:
```

##### `search`
```python
async def search(self, search_term, qualifier_type_id, language_id, page, page_size) -> Dict[(str, Any)]:
```

### Class: `QualifierTypeRepository`
**Inherits from:** BaseRepository[(QualifierType, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_types` `async` |  |
| `get_by_qualifier_type_id` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_types`
```python
async def get_all_types(self) -> List[QualifierType]:
```

##### `get_by_qualifier_type_id`
```python
async def get_by_qualifier_type_id(self, qualifier_type_id) -> Optional[QualifierType]:
```
