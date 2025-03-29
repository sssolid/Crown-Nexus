from __future__ import annotations
import os
from app.core.config import Environment, get_settings
def test_settings_from_env() -> None:
    os.environ['PROJECT_NAME'] = 'test_project'
    os.environ['ENVIRONMENT'] = 'development'
    os.environ['API_V1_STR'] = '/api/v1'
    settings = get_settings()
    assert settings.PROJECT_NAME == 'test_project'
    assert settings.ENVIRONMENT == Environment.DEVELOPMENT
    assert settings.API_V1_STR == '/api/v1'
def test_environment_enum() -> None:
    assert Environment.DEVELOPMENT.value == 'development'
    assert Environment.STAGING.value == 'staging'
    assert Environment.PRODUCTION.value == 'production'
def test_cors_origins_parsing() -> None:
    os.environ['BACKEND_CORS_ORIGINS'] = 'http://localhost,http://example.com'
    settings = get_settings()
    assert 'http://localhost' in settings.BACKEND_CORS_ORIGINS
    assert 'http://example.com' in settings.BACKEND_CORS_ORIGINS
    os.environ['BACKEND_CORS_ORIGINS'] = '["http://other.com", "https://test.com"]'
    settings = get_settings()
    assert 'http://other.com' in settings.BACKEND_CORS_ORIGINS
    assert 'https://test.com' in settings.BACKEND_CORS_ORIGINS