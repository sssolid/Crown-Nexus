from __future__ import annotations
'Import schemas for product pricing data.\n\nThis module defines schemas specifically for the data import process\nthat allow working with string identifiers instead of UUIDs.\n'
import uuid
from typing import Optional
from pydantic import BaseModel, Field
class ProductPricingImport(BaseModel):
    part_number: str = Field(..., description='Product part number')
    pricing_type: str = Field(..., description='Pricing type name (e.g., "Jobber", "Export")')
    price: float = Field(..., description='Price value')
    currency: str = Field('USD', description='Currency code')