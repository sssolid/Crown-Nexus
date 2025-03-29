# Module: app.fitment.exceptions

**Path:** `app/fitment/exceptions.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Optional
```

## Classes

| Class | Description |
| --- | --- |
| `ConfigurationError` |  |
| `DatabaseError` |  |
| `FitmentError` |  |
| `MappingError` |  |
| `ParsingError` |  |
| `ValidationError` |  |

### Class: `ConfigurationError`
**Inherits from:** FitmentError

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `DatabaseError`
**Inherits from:** FitmentError

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `FitmentError`
**Inherits from:** Exception

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `MappingError`
**Inherits from:** FitmentError

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `ParsingError`
**Inherits from:** FitmentError

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `ValidationError`
**Inherits from:** FitmentError

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```
