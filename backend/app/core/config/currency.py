# app/core/config/models.py

from __future__ import annotations

"""
Currency and exchange rate configuration settings.

This module defines settings for currency conversion, exchange rate APIs,
and update frequencies.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class CurrencySettings(BaseSettings):
    """Currency and exchange rate settings."""

    # Exchange rate API configuration
    EXCHANGE_RATE_API_KEY: str = ""
    EXCHANGE_RATE_UPDATE_FREQUENCY: int = 24  # In hours
    STORE_INVERSE_RATES: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )
