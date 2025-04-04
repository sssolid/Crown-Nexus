# Module: app.domains.products.exceptions

**Path:** `app/domains/products/exceptions.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.exceptions import BusinessException, ResourceNotFoundException
```

## Classes

| Class | Description |
| --- | --- |
| `BrandNotFoundException` |  |
| `DuplicateBrandNameException` |  |
| `DuplicatePartNumberException` |  |
| `ProductInactiveException` |  |
| `ProductNotFoundException` |  |

### Class: `BrandNotFoundException`
**Inherits from:** ResourceNotFoundException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, brand_id) -> None:
```

### Class: `DuplicateBrandNameException`
**Inherits from:** BusinessException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, name) -> None:
```

### Class: `DuplicatePartNumberException`
**Inherits from:** BusinessException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, part_number) -> None:
```

### Class: `ProductInactiveException`
**Inherits from:** BusinessException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, product_id) -> None:
```

### Class: `ProductNotFoundException`
**Inherits from:** ResourceNotFoundException

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, product_id) -> None:
```
