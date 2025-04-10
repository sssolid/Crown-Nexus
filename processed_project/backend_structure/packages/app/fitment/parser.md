# Module: app.fitment.parser

**Path:** `app/fitment/parser.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import re
from typing import Dict, List, Tuple
from exceptions import ParsingError
from models import PartApplication, PartFitment, Position, PositionGroup, Vehicle
```

## Classes

| Class | Description |
| --- | --- |
| `FitmentParser` |  |

### Class: `FitmentParser`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `expand_year_range` |  |
| `extract_positions` |  |
| `extract_year_range` |  |
| `find_model_mapping` |  |
| `parse_application` |  |
| `process_application` |  |

##### `__init__`
```python
def __init__(self, model_mappings) -> None:
```

##### `expand_year_range`
```python
def expand_year_range(self, start_year, end_year) -> List[int]:
```

##### `extract_positions`
```python
def extract_positions(self, position_text) -> List[PositionGroup]:
```

##### `extract_year_range`
```python
def extract_year_range(self, year_text) -> Tuple[(int, int)]:
```

##### `find_model_mapping`
```python
def find_model_mapping(self, vehicle_text) -> List[Dict[(str, str)]]:
```

##### `parse_application`
```python
def parse_application(self, application_text) -> PartApplication:
```

##### `process_application`
```python
def process_application(self, part_app) -> List[PartFitment]:
```
