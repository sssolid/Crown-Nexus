# Module: app.data_import.processors

**Path:** `app/data_import/processors/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.data_import.processors.base import Processor
from app.data_import.processors.product_processor import ProductProcessor, ProductMappingConfig
from app.data_import.processors.as400_processor import AS400BaseProcessor, AS400ProcessorConfig, ProductAS400Processor, PricingAS400Processor, InventoryAS400Processor
```

## Global Variables
```python
__all__ = __all__ = [
    "Processor",
    "ProductProcessor",
    "ProductMappingConfig",
    "AS400BaseProcessor",
    "AS400ProcessorConfig",
    "ProductAS400Processor",
    "PricingAS400Processor",
    "InventoryAS400Processor",
]
```
