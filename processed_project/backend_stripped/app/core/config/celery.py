from __future__ import annotations
'\nCelery task queue configuration settings.\n\nThis module defines settings for the Celery task queue including broker\nand backend configurations.\n'
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
class CelerySettings(BaseSettings):
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='ignore')