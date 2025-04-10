from __future__ import annotations
'\nElasticsearch integration configuration.\n\nThis module defines configuration settings for the Elasticsearch integration,\nincluding connection parameters and security settings.\n'
from typing import Optional
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
class ElasticsearchSettings(BaseSettings):
    ELASTICSEARCH_HOST: str = 'localhost'
    ELASTICSEARCH_PORT: int = 9200
    ELASTICSEARCH_USE_SSL: bool = False
    ELASTICSEARCH_USERNAME: Optional[str] = None
    ELASTICSEARCH_PASSWORD: Optional[SecretStr] = None
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='ignore')
    @property
    def elasticsearch_uri(self) -> str:
        protocol = 'https' if self.ELASTICSEARCH_USE_SSL else 'http'
        auth = ''
        if self.ELASTICSEARCH_USERNAME:
            password = self.ELASTICSEARCH_PASSWORD.get_secret_value() if self.ELASTICSEARCH_PASSWORD else ''
            auth = f'{self.ELASTICSEARCH_USERNAME}:{password}@'
        return f'{protocol}://{auth}{self.ELASTICSEARCH_HOST}:{self.ELASTICSEARCH_PORT}'
elasticsearch_settings = ElasticsearchSettings()