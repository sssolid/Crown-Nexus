from __future__ import annotations
'\nLogging configuration module.\n\nThis module handles the configuration of the logging system, including\nformatters, filters, and processors for both standard logging and structlog.\n'
import datetime
import logging
import logging.config
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import pythonjsonlogger.jsonlogger as pythonjsonlogger
import structlog
from structlog.stdlib import BoundLogger, LoggerFactory
from structlog.types import EventDict, Processor, WrappedLogger
DEFAULT_LOG_LEVEL = 'INFO'
_logging_initialized = False
import threading
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
    else:
        event_dict['request_id'] = 'no_request_id'
    return event_dict
def add_user_id_processor(logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
    user_id = getattr(_request_context, 'user_id', None)
    if user_id:
        event_dict['user_id'] = user_id
    else:
        event_dict['user_id'] = 'anonymous'
    return event_dict
def add_timestamp_processor(logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
    event_dict['timestamp'] = datetime.datetime.now(datetime.UTC).isoformat() + 'Z'
    return event_dict
def add_service_info_processor(logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
    def get_project_info() -> tuple[str, str, str]:
        try:
            from app.core.config import settings
            return (settings.PROJECT_NAME, settings.VERSION, settings.ENVIRONMENT.value)
        except (ImportError, AttributeError):
            return ('App', '0.0.0', 'development')
    project_name, version, environment = get_project_info()
    event_dict['service'] = project_name
    event_dict['version'] = version
    event_dict['environment'] = environment
    return event_dict
class ConsoleRendererWithLineNumbers(structlog.dev.ConsoleRenderer):
    def __call__(self, logger: logging.Logger, name: str, event_dict: Dict[str, Any]) -> str:
        lineno = event_dict.pop('lineno', None)
        filename = event_dict.pop('filename', None)
        output = super().__call__(logger, name, event_dict)
        if lineno and filename:
            logger_name_end = output.find(']', output.find('[', output.find(']') + 1)) + 1
            if logger_name_end > 0:
                output = f"{output[:logger_name_end]}:{filename.split('/')[-1]}:{lineno}{output[logger_name_end:]}"
        return output
def get_log_level() -> str:
    try:
        from app.core.config import settings
        return getattr(settings, 'LOG_LEVEL', DEFAULT_LOG_LEVEL)
    except (ImportError, AttributeError):
        return DEFAULT_LOG_LEVEL
def get_environment() -> str:
    try:
        from app.core.config import settings
        return settings.ENVIRONMENT.value
    except (ImportError, AttributeError):
        return 'development'
def configure_std_logging() -> None:
    log_level_name = get_log_level()
    if isinstance(log_level_name, str):
        log_level = getattr(logging, log_level_name, logging.INFO)
    else:
        log_level = logging.INFO
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    class StructlogPassthroughFormatter(logging.Formatter):
        def format(self, record):
            if hasattr(record, '_from_structlog') and record._from_structlog:
                return record.getMessage()
            return super().format(record)
    config: Dict[str, Any] = {'version': 1, 'disable_existing_loggers': False, 'formatters': {'standard': {'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d [%(request_id)s] [%(user_id)s] - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}, 'json': {'()': pythonjsonlogger.JsonFormatter, 'fmt': '%(timestamp)s %(level)s %(name)s %(request_id)s %(user_id)s %(message)s %(pathname)s %(lineno)d %(funcName)s %(process)d %(thread)d', 'rename_fields': {'levelname': 'level', 'asctime': 'timestamp'}}, 'structlog': {'()': StructlogPassthroughFormatter}}, 'filters': {'request_id': {'()': RequestIdFilter}, 'user_id': {'()': UserIdFilter}}, 'handlers': {'console': {'level': log_level, 'class': 'logging.StreamHandler', 'formatter': 'structlog' if get_environment() == 'development' else 'json', 'filters': ['request_id', 'user_id'], 'stream': sys.stdout}}, 'loggers': {'app': {'handlers': ['console'], 'level': log_level, 'propagate': False}, 'uvicorn': {'handlers': ['console'], 'level': log_level, 'propagate': False}, 'sqlalchemy.engine': {'handlers': ['console'], 'level': logging.INFO if get_environment() == 'development' else logging.WARNING, 'propagate': False}}, 'root': {'handlers': ['console'], 'level': log_level}}
    if get_environment() != 'development':
        config['handlers']['file'] = {'level': log_level, 'class': 'logging.handlers.RotatingFileHandler', 'filename': str(log_dir / 'app.log'), 'maxBytes': 10485760, 'backupCount': 10, 'formatter': 'json', 'filters': ['request_id', 'user_id']}
        config['handlers']['error_file'] = {'level': logging.ERROR, 'class': 'logging.handlers.RotatingFileHandler', 'filename': str(log_dir / 'error.log'), 'maxBytes': 10485760, 'backupCount': 10, 'formatter': 'json', 'filters': ['request_id', 'user_id']}
        for logger_name in config['loggers']:
            config['loggers'][logger_name]['handlers'].extend(['file', 'error_file'])
        config['root']['handlers'].extend(['file', 'error_file'])
    logging.config.dictConfig(config)
def configure_structlog() -> None:
    shared_processors: List[Processor] = [structlog.stdlib.add_logger_name, structlog.stdlib.add_log_level, structlog.processors.TimeStamper(fmt='iso'), structlog.processors.CallsiteParameterAdder(), structlog.processors.StackInfoRenderer(), structlog.processors.format_exc_info, add_request_id_processor, add_user_id_processor, add_service_info_processor]
    if get_environment() == 'development':
        structlog.configure(processors=shared_processors + [ConsoleRendererWithLineNumbers(colors=True)], logger_factory=structlog.stdlib.LoggerFactory(), wrapper_class=structlog.stdlib.BoundLogger, cache_logger_on_first_use=True)
    else:
        structlog.configure(processors=shared_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter], logger_factory=structlog.stdlib.LoggerFactory(), wrapper_class=structlog.stdlib.BoundLogger, cache_logger_on_first_use=True)
def initialize_logging() -> None:
    global _logging_initialized
    if _logging_initialized:
        return
    configure_std_logging()
    configure_structlog()
    _logging_initialized = True
    logger = get_logger('app.logging')
    logger.info('Logging initialized', environment=get_environment(), log_level=get_log_level())
async def reinitialize_logging() -> None:
    global _logging_initialized
    if not _logging_initialized:
        initialize_logging()
        return
    logger = get_logger('app.logging')
    logger.debug('Logging system already initialized')
async def shutdown_logging() -> None:
    global _logging_initialized
    if not _logging_initialized:
        return
    logger = get_logger('app.logging')
    logger.info('Shutting down logging system')
    logging.shutdown()
    _logging_initialized = False
def get_logger(name: str) -> BoundLogger:
    if not _logging_initialized:
        initialize_logging()
    return structlog.get_logger(name)
initialize_logging()