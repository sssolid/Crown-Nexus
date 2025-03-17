# /backend/app/services/logging_service.py
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

# Type variables
F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")

class LoggingService:
    """Service for centralized logging functionality.
    
    This service provides standardized logging across the application,
    with support for structured logging, correlation IDs, and context tracking.
    """
    
    def __init__(self) -> None:
        """Initialize the logging service."""
        self._logger = logging.getLogger("app.services.logging_service")
        self._context_data = threading.local()
        
    async def initialize(self) -> None:
        """Initialize service resources."""
        self._logger.debug("Initializing logging service")
        
        # Set up logging configuration
        self.configure_logging()
        
    async def shutdown(self) -> None:
        """Release service resources."""
        self._logger.debug("Shutting down logging service")
        
    def configure_logging(self) -> None:
        """Configure logging with appropriate handlers and formatters."""
        # Configure standard library logging
        self.configure_std_logging()
        
        # Configure structlog
        self.configure_structlog()
        
    def configure_std_logging(self) -> None:
        """Configure standard library logging.
        
        Sets up log handlers based on environment and configuration settings.
        """
        log_level = getattr(logging, settings.LOG_LEVEL.value)
        
        # Clear existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            
        # Configure root logger
        root_logger.setLevel(log_level)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        # Create formatter
        if settings.ENVIRONMENT == Environment.DEVELOPMENT:
            # In development, use a more readable format
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        else:
            # In production, use JSON format
            formatter = jsonlogger.JsonFormatter(
                '%(asctime)s %(name)s %(levelname)s %(message)s'
            )
            
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # Add file handler in production
        if settings.ENVIRONMENT == Environment.PRODUCTION:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(
                log_dir / f"{settings.PROJECT_NAME.lower()}.log"
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
        # Set logger levels
        logging.getLogger("uvicorn").setLevel(logging.INFO)
        logging.getLogger("uvicorn.access").setLevel(logging.INFO)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        
    def configure_structlog(self) -> None:
        """Configure structlog with processors and renderers.
        
        Sets up structlog to work alongside standard library logging,
        with consistent formatting and context handling.
        """
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                self.add_context_processor,
                structlog.processors.UnicodeDecoder(),
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        
    def get_logger(self, name: str) -> BoundLogger:
        """Get a structlog logger instance.
        
        Args:
            name: Logger name (typically __name__)
            
        Returns:
            BoundLogger: Structured logger instance
        """
        return structlog.get_logger(name)
        
    def add_context_processor(
        self, 
        logger: WrappedLogger, 
        method_name: str, 
        event_dict: EventDict
    ) -> EventDict:
        """Add context data to log events.
        
        Args:
            logger: Logger instance
            method_name: Method name being called
            event_dict: Event dictionary to modify
            
        Returns:
            EventDict: Modified event dictionary
        """
        # Add request_id if available
        request_id = getattr(self._context_data, "request_id", None)
        if request_id:
            event_dict["request_id"] = request_id
            
        # Add user_id if available
        user_id = getattr(self._context_data, "user_id", None)
        if user_id:
            event_dict["user_id"] = user_id
            
        # Add service name if available
        service = getattr(self._context_data, "service", None)
        if service:
            event_dict["service"] = service
            
        # Add environment
        event_dict["environment"] = settings.ENVIRONMENT.value
            
        return event_dict
        
    def set_context(
        self, 
        request_id: Optional[str] = None, 
        user_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Set context data for the current thread.
        
        Args:
            request_id: Request ID for correlation
            user_id: User ID for tracking
            **kwargs: Additional context data
        """
        if request_id:
            self._context_data.request_id = request_id
        if user_id:
            self._context_data.user_id = user_id
            
        # Set additional context data
        for key, value in kwargs.items():
            setattr(self._context_data, key, value)
            
    def clear_context(self) -> None:
        """Clear context data for the current thread."""
        if hasattr(self._context_data, "request_id"):
            delattr(self._context_data, "request_id")
        if hasattr(self._context_data, "user_id"):
            delattr(self._context_data, "user_id")
            
    @contextmanager
    def request_context(
        self, 
        request_id: Optional[str] = None, 
        user_id: Optional[str] = None
    ) -> Generator[str, None, None]:
        """Context manager for tracking request context in logs.
        
        Args:
            request_id: Request ID (generated if not provided)
            user_id: User ID (optional)
            
        Yields:
            str: Request ID
        """
        # Generate request ID if not provided
        request_id = request_id or str(uuid.uuid4())
        
        # Set context data
        self.set_context(request_id=request_id, user_id=user_id)
        
        try:
            yield request_id
        finally:
            # Clear context data
            self.clear_context()
            
    def log_execution_time(
        self, 
        logger: Optional[BoundLogger] = None, 
        level: str = "debug"
    ) -> Callable[[F], F]:
        """Decorator to log function execution time.
        
        Args:
            logger: Logger to use
            level: Log level to use
            
        Returns:
            Callable: Decorated function
        """
        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Use provided logger or get new one
                log = logger or self.get_logger(func.__module__)
                
                # Log function start
                start_time = time.time()
                log_method = getattr(log, level)
                log_method(f"Starting {func.__name__}")
                
                try:
                    # Call function
                    result = func(*args, **kwargs)
                    
                    # Log execution time
                    execution_time = time.time() - start_time
                    log_method(
                        f"Completed {func.__name__}",
                        execution_time=f"{execution_time:.4f}s",
                    )
                    
                    return result
                except Exception as e:
                    # Log error and execution time
                    execution_time = time.time() - start_time
                    log.error(
                        f"Error in {func.__name__}: {str(e)}",
                        execution_time=f"{execution_time:.4f}s",
                        exc_info=True,
                    )
                    raise
                    
            return cast(F, wrapper)
        return decorator
        
    async def log_execution_time_async(
        self, 
        logger: Optional[BoundLogger] = None, 
        level: str = "debug"
    ) -> Callable[[F], F]:
        """Decorator to log async function execution time.
        
        Args:
            logger: Logger to use
            level: Log level to use
            
        Returns:
            Callable: Decorated async function
        """
        def decorator(func: F) -> F:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Use provided logger or get new one
                log = logger or self.get_logger(func.__module__)
                
                # Log function start
                start_time = time.time()
                log_method = getattr(log, level)
                log_method(f"Starting {func.__name__}")
                
                try:
                    # Call function
                    result = await func(*args, **kwargs)
                    
                    # Log execution time
                    execution_time = time.time() - start_time
                    log_method(
                        f"Completed {func.__name__}",
                        execution_time=f"{execution_time:.4f}s",
                    )
                    
                    return result
                except Exception as e:
                    # Log error and execution time
                    execution_time = time.time() - start_time
                    log.error(
                        f"Error in {func.__name__}: {str(e)}",
                        execution_time=f"{execution_time:.4f}s",
                        exc_info=True,
                    )
                    raise
                    
            return cast(F, wrapper)
        return decorator
