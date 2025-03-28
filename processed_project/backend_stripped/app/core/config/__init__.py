from __future__ import annotations
'\nConfiguration package for the application.\n\nThis module exports the main settings interfaces and common types used\nthroughout the application.\n'
from app.core.config.base import Environment, LogLevel
from app.core.config.settings import Settings, get_settings, settings
__all__ = ['Settings', 'Environment', 'LogLevel', 'get_settings', 'settings', 'AS400Settings', 'ElasticsearchSettings', 'as400_settings', 'elasticsearch_settings', 'get_as400_connector_config']
def __getattr__(name: str) -> object:
    if name == 'AS400Settings':
        from app.core.config.integrations.as400 import AS400Settings
        return AS400Settings
    elif name == 'as400_settings':
        from app.core.config.integrations.as400 import as400_settings
        return as400_settings
    elif name == 'get_as400_connector_config':
        from app.core.config.integrations.as400 import get_as400_connector_config
        return get_as400_connector_config
    elif name == 'ElasticsearchSettings':
        from app.core.config.integrations.elasticsearch import ElasticsearchSettings
        return ElasticsearchSettings
    elif name == 'elasticsearch_settings':
        from app.core.config.integrations.elasticsearch import elasticsearch_settings
        return elasticsearch_settings
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')