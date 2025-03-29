# Module: app.domains.autocare.exceptions

**Path:** `app/domains/autocare/exceptions.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.exceptions import BusinessException, ResourceNotFoundException
```

## Classes

| Class | Description |
| --- | --- |
| `AutocareException` |  |
| `ExportException` |  |
| `ImportException` |  |
| `InvalidPartDataException` |  |
| `InvalidVehicleDataException` |  |
| `MappingNotFoundException` |  |
| `PAdbException` |  |
| `PCdbException` |  |
| `QdbException` |  |
| `VCdbException` |  |

### Class: `AutocareException`
**Inherits from:** BusinessException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `ExportException`
**Inherits from:** AutocareException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `ImportException`
**Inherits from:** AutocareException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `InvalidPartDataException`
**Inherits from:** AutocareException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `InvalidVehicleDataException`
**Inherits from:** AutocareException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `MappingNotFoundException`
**Inherits from:** ResourceNotFoundException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, resource_id, details) -> None:
```

### Class: `PAdbException`
**Inherits from:** AutocareException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `PCdbException`
**Inherits from:** AutocareException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `QdbException`
**Inherits from:** AutocareException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```

### Class: `VCdbException`
**Inherits from:** AutocareException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, message, details) -> None:
```
