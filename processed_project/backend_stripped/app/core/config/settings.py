from __future__ import annotations
'\nCombined application settings.\n\nThis module integrates all modular settings into a single application settings\nclass, providing a unified interface for configuration.\n'
from functools import lru_cache
from typing import Any, Dict
from pydantic import model_validator
from pydantic_settings import SettingsConfigDict
from app.core.config.base import BaseAppSettings
from app.core.config.celery import CelerySettings
from app.core.config.currency import CurrencySettings
from app.core.config.database import DatabaseSettings
from app.core.config.fitment import FitmentSettings
from app.core.config.media import MediaSettings
from app.core.config.security import SecuritySettings
class Settings(BaseAppSettings, DatabaseSettings, SecuritySettings, MediaSettings, FitmentSettings, CurrencySettings, CelerySettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='ignore')
    @model_validator(mode='after')
    def setup_celery_urls(self) -> 'Settings':
        if not self.CELERY_BROKER_URL:
            self.CELERY_BROKER_URL = self.redis_uri
        if not self.CELERY_RESULT_BACKEND:
            self.CELERY_RESULT_BACKEND = self.redis_uri
        return self
    def model_dump(self, **kwargs: Any) -> Dict[str, Any]:
        settings_dict = super().model_dump(**kwargs)
        settings_dict['redis_uri'] = self.redis_uri
        settings_dict['media_base_url'] = self.media_base_url
        return settings_dict
    @property
    def as400(self) -> 'AS400Settings':
        from app.core.config.integrations.as400 import as400_settings
        return as400_settings
    @property
    def elasticsearch(self) -> 'ElasticsearchSettings':
        from app.core.config.integrations.elasticsearch import elasticsearch_settings
        return elasticsearch_settings
@lru_cache
def get_settings() -> Settings:
    return Settings()
settings = get_settings()