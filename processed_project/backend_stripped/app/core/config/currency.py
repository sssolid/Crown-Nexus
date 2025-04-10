from __future__ import annotations
'\nCurrency and exchange rate configuration settings.\n\nThis module defines settings for currency conversion, exchange rate APIs,\nand update frequencies.\n'
from pydantic_settings import BaseSettings, SettingsConfigDict
class CurrencySettings(BaseSettings):
    EXCHANGE_RATE_API_KEY: str = ''
    EXCHANGE_RATE_UPDATE_FREQUENCY: int = 24
    STORE_INVERSE_RATES: bool = True
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='ignore')