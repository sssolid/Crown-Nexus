from __future__ import annotations
'Import schemas for data import.\n\nThis package contains schemas specifically designed for the data import process,\nthat allow working with string identifiers instead of UUIDs or other domain-specific types.\n'
from app.data_import.schemas.pricing import ProductPricingImport
__all__ = ['ProductPricingImport']