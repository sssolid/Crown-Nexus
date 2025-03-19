# /app/services/audit/factory.py
from __future__ import annotations

"""Factory for creating audit loggers.

This module provides a factory for creating different audit logger instances
based on configuration settings.
"""

from typing import Dict, List, Optional, Type, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.services.audit.base import AuditLogger
from app.services.audit.loggers import (
    DatabaseAuditLogger,
    FileAuditLogger,
    LoggingAuditLogger,
)

logger = get_logger("app.services.audit.factory")


class AuditLoggerFactory:
    """Factory for creating audit logger instances."""

    # Registry of logger types to their classes
    _loggers: Dict[str, Type[AuditLogger]] = {
        "logging": LoggingAuditLogger,
        "file": FileAuditLogger,
        "database": DatabaseAuditLogger,
    }

    # Cache of already-created loggers
    _logger_instances: Dict[str, AuditLogger] = {}

    @classmethod
    def register_logger(cls, name: str, logger_class: Type[AuditLogger]) -> None:
        """Register a new audit logger type.

        Args:
            name: Logger type name
            logger_class: Logger class

        Raises:
            ValueError: If a logger with the same name is already registered
        """
        if name in cls._loggers:
            raise ValueError(f"Audit logger '{name}' is already registered")

        cls._loggers[name] = logger_class
        logger.debug(f"Registered audit logger type: {name}")

    @classmethod
    def create_logger(
        cls, logger_type: str, db: Optional[AsyncSession] = None, **kwargs: Any
    ) -> AuditLogger:
        """Create an audit logger of the specified type.

        Args:
            logger_type: The type of logger to create
            db: Optional database session for database loggers
            **kwargs: Additional logger configuration

        Returns:
            AuditLogger: The created logger

        Raises:
            ValueError: If the logger type is not supported
        """
        # Generate a cache key
        cache_key = f"{logger_type}:{id(db)}"

        # Check if logger is already cached
        if cache_key in cls._logger_instances:
            return cls._logger_instances[cache_key]

        # Create new logger based on type
        if logger_type not in cls._loggers:
            raise ValueError(
                f"Unsupported audit logger type: {logger_type}. "
                f"Supported types: {', '.join(cls._loggers.keys())}"
            )

        logger_class = cls._loggers[logger_type]

        if logger_type == "database":
            audit_logger = logger_class(db=db)
        elif logger_type == "file":
            file_path = kwargs.get("file_path", settings.security.AUDIT_LOG_FILE)
            audit_logger = logger_class(file_path=file_path)
        else:
            audit_logger = logger_class()

        # Cache the logger
        cls._logger_instances[cache_key] = audit_logger

        logger.debug(f"Created audit logger: {logger_type}")
        return audit_logger

    @classmethod
    def create_default_loggers(
        cls, db: Optional[AsyncSession] = None
    ) -> List[AuditLogger]:
        """Create the default set of audit loggers based on application settings.

        Args:
            db: Optional database session for database loggers

        Returns:
            List of default audit loggers
        """
        loggers: List[AuditLogger] = []

        # Always add logging logger
        loggers.append(cls.create_logger("logging"))

        # Add file logger if configured
        if (
            hasattr(settings.security, "AUDIT_LOG_TO_FILE")
            and settings.security.AUDIT_LOG_TO_FILE
        ):
            loggers.append(cls.create_logger("file"))

        # Add database logger if configured and session provided
        if (
            db
            and hasattr(settings.security, "AUDIT_LOG_TO_DB")
            and settings.security.AUDIT_LOG_TO_DB
        ):
            loggers.append(cls.create_logger("database", db=db))

        return loggers
