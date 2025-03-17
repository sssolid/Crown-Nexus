from __future__ import annotations
import logging
import logging.config
import sys
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast, Union
import structlog
from pythonjsonlogger import jsonlogger
from structlog.stdlib import BoundLogger
from structlog.types import EventDict, Processor, WrappedLogger
from app.core.config import Environment, LogLevel, settings
F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')
_request_context = threading.local()
class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        request_id = getattr(_request_context, 'request_id', None)
        record.request_id = request_id or 'no_request_id'
        return True
class UserIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        user_id = getattr(_request_context, 'user_id', None)
        record.user_id = user_id or 'anonymous'
        return True
def add_request_id_processor(logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
    request_id = getattr(_request_context, 'request_id', None)
    if request_id:
        event_dict['request_id'] = request_id
    return event_dict
def add_user_id_processor(logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
    user_id = getattr(_request_context, 'user_id', None)
    if user_id:
        event_dict['user_id'] = user_id
    return event_dict
def add_timestamp_processor(logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
    event_dict['timestamp'] = datetime.utcnow().isoformat() + 'Z'
    return event_dict
def add_service_info_processor(logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
    event_dict['service'] = settings.PROJECT_NAME
    event_dict['version'] = settings.VERSION
    event_dict['environment'] = settings.ENVIRONMENT.value
    return event_dict
def configure_std_logging() -> None:
    log_level_name = getattr(settings.logging, 'LOG_LEVEL', LogLevel.INFO).value
    log_level = getattr(logging, log_level_name, logging.INFO)
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    config: Dict[str, Any] = {'version': 1, 'disable_existing_loggers': False, 'formatters': {'standard': {'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d [%(request_id)s] [%(user_id)s] - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}, 'json': {'()': jsonlogger.JsonFormatter, 'fmt': '%(timestamp)s %(level)s %(name)s %(request_id)s %(user_id)s %(message)s %(pathname)s %(lineno)d %(funcName)s %(process)d %(thread)d', 'rename_fields': {'levelname': 'level', 'asctime': 'timestamp'}}}, 'filters': {'request_id': {'()': RequestIdFilter}, 'user_id': {'()': UserIdFilter}}, 'handlers': {'console': {'level': log_level, 'class': 'logging.StreamHandler', 'formatter': 'standard' if settings.ENVIRONMENT != Environment.PRODUCTION else 'json', 'filters': ['request_id', 'user_id'], 'stream': sys.stdout}}, 'loggers': {'app': {'handlers': ['console'], 'level': log_level, 'propagate': False}, 'uvicorn': {'handlers': ['console'], 'level': log_level, 'propagate': False}, 'fitment': {'handlers': ['console'], 'level': getattr(logging, settings.fitment.FITMENT_LOG_LEVEL, logging.INFO), 'propagate': False}, 'sqlalchemy.engine': {'handlers': ['console'], 'level': logging.INFO if settings.ENVIRONMENT == Environment.DEVELOPMENT else logging.WARNING, 'propagate': False}}, 'root': {'handlers': ['console'], 'level': log_level}}
    if settings.ENVIRONMENT != Environment.DEVELOPMENT:
        config['handlers']['file'] = {'level': log_level, 'class': 'logging.handlers.RotatingFileHandler', 'filename': str(log_dir / 'app.log'), 'maxBytes': 10485760, 'backupCount': 10, 'formatter': 'json', 'filters': ['request_id', 'user_id']}
        config['handlers']['error_file'] = {'level': logging.ERROR, 'class': 'logging.handlers.RotatingFileHandler', 'filename': str(log_dir / 'error.log'), 'maxBytes': 10485760, 'backupCount': 10, 'formatter': 'json', 'filters': ['request_id', 'user_id']}
        for logger_name in config['loggers']:
            config['loggers'][logger_name]['handlers'].extend(['file', 'error_file'])
        config['root']['handlers'].extend(['file', 'error_file'])
    logging.config.dictConfig(config)
def configure_structlog() -> None:
    shared_processors: List[Processor] = [structlog.stdlib.add_logger_name, structlog.stdlib.add_log_level, structlog.processors.TimeStamper(fmt='iso'), structlog.processors.StackInfoRenderer(), structlog.processors.format_exc_info, add_request_id_processor, add_user_id_processor, add_service_info_processor]
    if settings.ENVIRONMENT == Environment.DEVELOPMENT:
        structlog.configure(processors=shared_processors + [structlog.dev.ConsoleRenderer(colors=True)], logger_factory=structlog.stdlib.LoggerFactory(), cache_logger_on_first_use=True)
    else:
        structlog.configure(processors=shared_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter], logger_factory=structlog.stdlib.LoggerFactory(), cache_logger_on_first_use=True)
def setup_logging() -> None:
    configure_std_logging()
    configure_structlog()
    logger = get_logger('app.core.logging')
    logger.info(f'Logging initialized', environment=settings.ENVIRONMENT.value, log_level=settings.logging.LOG_LEVEL.value)
def get_logger(name: str) -> BoundLogger:
    return cast(BoundLogger, structlog.get_logger(name))
@contextmanager
def request_context(request_id: Optional[str]=None, user_id: Optional[str]=None):
    _request_id = request_id or str(uuid.uuid4())
    old_request_id = getattr(_request_context, 'request_id', None)
    old_user_id = getattr(_request_context, 'user_id', None)
    _request_context.request_id = _request_id
    if user_id:
        _request_context.user_id = user_id
    try:
        yield _request_id
    finally:
        if old_request_id:
            _request_context.request_id = old_request_id
        else:
            delattr(_request_context, 'request_id')
        if user_id:
            if old_user_id:
                _request_context.user_id = old_user_id
            else:
                delattr(_request_context, 'user_id')
def set_user_id(user_id: str) -> None:
    _request_context.user_id = user_id
def clear_user_id() -> None:
    if hasattr(_request_context, 'user_id'):
        delattr(_request_context, 'user_id')
def log_execution_time(logger: Optional[BoundLogger]=None, level: str='info'):
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log = logger or get_logger(func.__module__)
            log_method = getattr(log, level)
            start_time = datetime.now()
            log_method(f'{func.__name__} started')
            try:
                result = func(*args, **kwargs)
                execution_time = (datetime.now() - start_time).total_seconds()
                log_method(f'{func.__name__} completed', execution_time=execution_time)
                return result
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                log.exception(f'{func.__name__} failed', error=str(e), execution_time=execution_time)
                raise
        return cast(F, wrapper)
    return decorator
def log_execution_time_async(logger: Optional[BoundLogger]=None, level: str='info'):
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            log = logger or get_logger(func.__module__)
            log_method = getattr(log, level)
            start_time = datetime.now()
            log_method(f'{func.__name__} started')
            try:
                result = await func(*args, **kwargs)
                execution_time = (datetime.now() - start_time).total_seconds()
                log_method(f'{func.__name__} completed', execution_time=execution_time)
                return result
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                log.exception(f'{func.__name__} failed', error=str(e), execution_time=execution_time)
                raise
        return cast(F, wrapper)
    return decorator