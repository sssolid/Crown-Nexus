# app/data_import/processors/__init__.py
from __future__ import annotations

"""
Data processors for data import.

This package provides processors for transforming and validating
raw data from external sources into structured formats for import.
"""

from app.data_import.processors.base import Processor
from app.data_import.processors.product_processor import (
    ProductProcessor,
    ProductMappingConfig,
)
from app.data_import.processors.as400_processor import (
    AS400BaseProcessor,
    AS400ProcessorConfig,
    ProductAS400Processor,
    PricingAS400Processor,
    InventoryAS400Processor,
)

__all__ = [
    "Processor",
    "ProductProcessor",
    "ProductMappingConfig",
    "AS400BaseProcessor",
    "AS400ProcessorConfig",
    "ProductAS400Processor",
    "PricingAS400Processor",
    "InventoryAS400Processor",
]
