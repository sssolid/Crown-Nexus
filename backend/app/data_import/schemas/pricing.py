from __future__ import annotations

"""Import schemas for product pricing data.

This module defines schemas specifically for the data import process
that allow working with string identifiers instead of UUIDs.
"""

import uuid
from typing import Optional
from pydantic import BaseModel, Field


class ProductPricingImport(BaseModel):
    """Schema for importing product pricing data.

    This schema uses string identifiers (part number, pricing type name) instead of UUIDs
    to make it easier to import data from external sources.

    Attributes:
        part_number: Product part number (string identifier)
        pricing_type: String identifier for the pricing type (e.g., "Jobber", "Export")
        price: The monetary value of the product
        currency: Three-letter currency code (default: USD)
    """
    part_number: str = Field(..., description='Product part number')
    pricing_type: str = Field(..., description='Pricing type name (e.g., "Jobber", "Export")')
    price: float = Field(..., description='Price value')
    currency: str = Field('USD', description='Currency code')
