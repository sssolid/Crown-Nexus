from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
class CurrencyBase(BaseModel):
    code: str = Field(..., min_length=3, max_length=3, description='ISO 4217 currency code')
    name: str = Field(..., min_length=1, max_length=100, description='Currency name')
    symbol: Optional[str] = Field(None, max_length=10, description='Currency symbol')
    is_active: bool = Field(True, description='Whether the currency is active')
    is_base: bool = Field(False, description='Whether this is the base currency')
class CurrencyCreate(CurrencyBase):
    pass
class CurrencyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description='Currency name')
    symbol: Optional[str] = Field(None, max_length=10, description='Currency symbol')
    is_active: Optional[bool] = Field(None, description='Whether the currency is active')
    is_base: Optional[bool] = Field(None, description='Whether this is the base currency')
class CurrencyRead(CurrencyBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
class ExchangeRateBase(BaseModel):
    source_currency_id: uuid.UUID = Field(..., description='Source currency ID')
    target_currency_id: uuid.UUID = Field(..., description='Target currency ID')
    rate: float = Field(..., gt=0, description='Exchange rate value')
    effective_date: datetime = Field(..., description='When the rate became effective')
    data_source: Optional[str] = Field(None, description='API or source that provided the rate')
class ExchangeRateCreate(ExchangeRateBase):
    pass
class ExchangeRateRead(ExchangeRateBase):
    id: uuid.UUID
    fetched_at: datetime
    created_at: datetime
    source_currency: CurrencyRead
    target_currency: CurrencyRead
    model_config = ConfigDict(from_attributes=True)
class ConversionRequest(BaseModel):
    source_currency: str = Field(..., min_length=3, max_length=3, description='Source currency code')
    target_currency: str = Field(..., min_length=3, max_length=3, description='Target currency code')
    amount: float = Field(..., gt=0, description='Amount to convert')
    @field_validator('source_currency', 'target_currency')
    @classmethod
    def validate_currency_code(cls, v: str) -> str:
        return v.upper()
class ConversionResponse(BaseModel):
    source_currency: str = Field(..., description='Source currency code')
    target_currency: str = Field(..., description='Target currency code')
    source_amount: float = Field(..., description='Original amount')
    converted_amount: float = Field(..., description='Converted amount')
    exchange_rate: float = Field(..., description='Exchange rate used')
    timestamp: datetime = Field(..., description='Conversion timestamp')