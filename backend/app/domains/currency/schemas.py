from __future__ import annotations

"""Currency schema definitions.

This module defines Pydantic schemas for Currency and ExchangeRate objects,
including creation, update, and response models.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CurrencyBase(BaseModel):
    """Base schema for currency data.

    Attributes:
        code: ISO 4217 currency code.
        name: Currency name.
        symbol: Currency symbol.
        is_active: Whether the currency is active.
        is_base: Whether this is the base currency.
    """

    code: str = Field(
        ..., min_length=3, max_length=3, description="ISO 4217 currency code"
    )
    name: str = Field(..., min_length=1, max_length=100, description="Currency name")
    symbol: Optional[str] = Field(None, max_length=10, description="Currency symbol")
    is_active: bool = Field(True, description="Whether the currency is active")
    is_base: bool = Field(False, description="Whether this is the base currency")


class CurrencyCreate(CurrencyBase):
    """Schema for creating a new currency."""

    pass


class CurrencyUpdate(BaseModel):
    """Schema for updating an existing currency.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Currency name"
    )
    symbol: Optional[str] = Field(None, max_length=10, description="Currency symbol")
    is_active: Optional[bool] = Field(
        None, description="Whether the currency is active"
    )
    is_base: Optional[bool] = Field(
        None, description="Whether this is the base currency"
    )


class CurrencyRead(CurrencyBase):
    """Schema for currency data in API responses.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class ExchangeRateBase(BaseModel):
    """Base schema for exchange rate data.

    Attributes:
        source_currency_id: ID of the source currency.
        target_currency_id: ID of the target currency.
        rate: Exchange rate value.
        effective_date: When the rate became effective.
        data_source: API or source that provided the rate.
    """

    source_currency_id: uuid.UUID = Field(..., description="Source currency ID")
    target_currency_id: uuid.UUID = Field(..., description="Target currency ID")
    rate: float = Field(..., gt=0, description="Exchange rate value")
    effective_date: datetime = Field(..., description="When the rate became effective")
    data_source: Optional[str] = Field(
        None, description="API or source that provided the rate"
    )


class ExchangeRateCreate(ExchangeRateBase):
    """Schema for creating a new exchange rate."""

    pass


class ExchangeRateRead(ExchangeRateBase):
    """Schema for exchange rate data in API responses.

    Includes database-specific fields and related currencies.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    fetched_at: datetime = Field(..., description="When the rate was fetched")
    created_at: datetime = Field(..., description="Creation timestamp")
    source_currency: CurrencyRead = Field(..., description="Source currency details")
    target_currency: CurrencyRead = Field(..., description="Target currency details")

    model_config = ConfigDict(from_attributes=True)


class ConversionRequest(BaseModel):
    """Schema for currency conversion request.

    Attributes:
        source_currency: Source currency code.
        target_currency: Target currency code.
        amount: Amount to convert.
    """

    source_currency: str = Field(
        ..., min_length=3, max_length=3, description="Source currency code"
    )
    target_currency: str = Field(
        ..., min_length=3, max_length=3, description="Target currency code"
    )
    amount: float = Field(..., gt=0, description="Amount to convert")

    @field_validator("source_currency", "target_currency")
    @classmethod
    def validate_currency_code(cls, v: str) -> str:
        """Validate and normalize currency codes.

        Args:
            v: The currency code to validate.

        Returns:
            Uppercase version of the currency code.
        """
        return v.upper()


class ConversionResponse(BaseModel):
    """Schema for currency conversion response.

    Attributes:
        source_currency: Source currency code.
        target_currency: Target currency code.
        source_amount: Original amount.
        converted_amount: Converted amount.
        exchange_rate: Exchange rate used.
        timestamp: Conversion timestamp.
    """

    source_currency: str = Field(..., description="Source currency code")
    target_currency: str = Field(..., description="Target currency code")
    source_amount: float = Field(..., description="Original amount")
    converted_amount: float = Field(..., description="Converted amount")
    exchange_rate: float = Field(..., description="Exchange rate used")
    timestamp: datetime = Field(..., description="Conversion timestamp")
