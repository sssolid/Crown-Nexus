from __future__ import annotations
import logging
import os
from functools import lru_cache
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
class FitmentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='FITMENT_', case_sensitive=False, extra='ignore')
    vcdb_path: str = Field(..., description='Path to the VCDB database file')
    pcdb_path: str = Field(..., description='Path to the PCDB database file')
    db_url: Optional[str] = Field(None, description='SQLAlchemy URL for the database')
    model_mappings_path: Optional[str] = Field(None, description='Path to the model mappings Excel file')
    log_level: str = Field('INFO', description='Logging level')
    cache_size: int = Field(100, description='Maximum size for LRU caches')
    @validator('vcdb_path', 'pcdb_path')
    def validate_file_path(cls, v: str) -> str:
        if not os.path.isfile(v):
            raise ValueError(f'File not found: {v}')
        return v
    @validator('model_mappings_path')
    def validate_optional_file_path(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not os.path.isfile(v)):
            raise ValueError(f'File not found: {v}')
        return v
@lru_cache(maxsize=1)
def get_settings() -> FitmentSettings:
    return FitmentSettings()
def configure_logging() -> None:
    settings = get_settings()
    logging.basicConfig(level=getattr(logging, settings.log_level.upper()), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')