from __future__ import annotations
import json
import logging
import sys
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Generator, List, Optional, TypeVar, cast
import structlog
from pythonjsonlogger import jsonlogger
from structlog.stdlib import BoundLogger
from structlog.types import EventDict, Processor, WrappedLogger
from app.core.config import Environment, LogLevel, settings
from app.services.interfaces import ServiceInterface
F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')
class LoggingService:
    def __init__(self) -> None:
        self._logger = logging.getLogger('app.services.logging_service')
        self._context_data = threading.local()
    async def initialize(self) -> None:
        self._logger.debug('Initializing logging service')
        self.configure_logging()
    async def shutdown(self) -> None:
        self._logger.debug('Shutting down logging service')
    def configure_logging(self) -> None:
        self.configure_std_logging()
        self.configure_structlog()
    def configure_std_logging(self) -> None:
        log_level = getattr(logging, settings.LOG_LEVEL.value)
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        root_logger.setLevel(log_level)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        if settings.ENVIRONMENT == Environment.DEVELOPMENT:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        else:
            formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        if settings.ENVIRONMENT == Environment.PRODUCTION:
            log_dir = Path('logs')
            log_dir.mkdir(exist_ok=True)
            file_handler = logging.FileHandler(log_dir / f'{settings.PROJECT_NAME.lower()}.log')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        logging.getLogger('uvicorn').setLevel(logging.INFO)
        logging.getLogger('uvicorn.access').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    def configure_structlog(self) -> None:
        structlog.configure(processors=[structlog.stdlib.filter_by_level, structlog.stdlib.add_logger_name, structlog.stdlib.add_log_level, structlog.stdlib.PositionalArgumentsFormatter(), structlog.processors.TimeStamper(fmt='iso'), structlog.processors.StackInfoRenderer(), structlog.processors.format_exc_info, self.add_context_processor, structlog.processors.UnicodeDecoder(), structlog.stdlib.ProcessorFormatter.wrap_for_formatter], context_class=dict, logger_factory=structlog.stdlib.LoggerFactory(), wrapper_class=structlog.stdlib.BoundLogger, cache_logger_on_first_use=True)
    def get_logger(self, name: str) -> BoundLogger:
        return structlog.get_logger(name)
    def add_context_processor(self, logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
        request_id = getattr(self._context_data, 'request_id', None)
        if request_id:
            event_dict['request_id'] = request_id
        user_id = getattr(self._context_data, 'user_id', None)
        if user_id:
            event_dict['user_id'] = user_id
        service = getattr(self._context_data, 'service', None)
        if service:
            event_dict['service'] = service
        event_dict['environment'] = settings.ENVIRONMENT.value
        return event_dict
    def set_context(self, request_id: Optional[str]=None, user_id: Optional[str]=None, **kwargs: Any) -> None:
        if request_id:
            self._context_data.request_id = request_id
        if user_id:
            self._context_data.user_id = user_id
        for key, value in kwargs.items():
            setattr(self._context_data, key, value)
    def clear_context(self) -> None:
        if hasattr(self._context_data, 'request_id'):
            delattr(self._context_data, 'request_id')
        if hasattr(self._context_data, 'user_id'):
            delattr(self._context_data, 'user_id')
    @contextmanager
    def request_context(self, request_id: Optional[str]=None, user_id: Optional[str]=None) -> Generator[str, None, None]:
        request_id = request_id or str(uuid.uuid4())
        self.set_context(request_id=request_id, user_id=user_id)
        try:
            yield request_id
        finally:
            self.clear_context()
    def log_execution_time(self, logger: Optional[BoundLogger]=None, level: str='debug') -> Callable[[F], F]:
        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                log = logger or self.get_logger(func.__module__)
                start_time = time.time()
                log_method = getattr(log, level)
                log_method(f'Starting {func.__name__}')
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    log_method(f'Completed {func.__name__}', execution_time=f'{execution_time:.4f}s')
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    log.error(f'Error in {func.__name__}: {str(e)}', execution_time=f'{execution_time:.4f}s', exc_info=True)
                    raise
            return cast(F, wrapper)
        return decorator
    async def log_execution_time_async(self, logger: Optional[BoundLogger]=None, level: str='debug') -> Callable[[F], F]:
        def decorator(func: F) -> F:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                log = logger or self.get_logger(func.__module__)
                start_time = time.time()
                log_method = getattr(log, level)
                log_method(f'Starting {func.__name__}')
                try:
                    result = await func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    log_method(f'Completed {func.__name__}', execution_time=f'{execution_time:.4f}s')
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    log.error(f'Error in {func.__name__}: {str(e)}', execution_time=f'{execution_time:.4f}s', exc_info=True)
                    raise
            return cast(F, wrapper)
        return decorator