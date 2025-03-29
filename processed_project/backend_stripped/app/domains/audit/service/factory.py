from __future__ import annotations
'Factory for creating audit loggers.\n\nThis module provides a factory for creating different audit logger instances\nbased on configuration settings.\n'
from typing import Dict, List, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.logging import get_logger
from app.domains.audit.service.base import AuditLogger
from app.domains.audit.service.loggers import DatabaseAuditLogger, FileAuditLogger, LoggingAuditLogger
logger = get_logger('app.domains.audit.service.factory')
class AuditLoggerFactory:
    _loggers: Dict[str, Type[AuditLogger]] = {'logging': LoggingAuditLogger, 'file': FileAuditLogger, 'database': DatabaseAuditLogger}
    _logger_instances: Dict[str, AuditLogger] = {}
    @classmethod
    def register_logger(cls, name: str, logger_class: Type[AuditLogger]) -> None:
        if name in cls._loggers:
            raise ValueError(f"Audit logger '{name}' is already registered")
        cls._loggers[name] = logger_class
        logger.debug(f'Registered audit logger type: {name}')
    @classmethod
    def create_logger(cls, logger_type: str, db: Optional[AsyncSession]=None, **kwargs: Any) -> AuditLogger:
        cache_key = f'{logger_type}:{id(db)}'
        if cache_key in cls._logger_instances:
            return cls._logger_instances[cache_key]
        if logger_type not in cls._loggers:
            raise ValueError(f"Unsupported audit logger type: {logger_type}. Supported types: {', '.join(cls._loggers.keys())}")
        logger_class = cls._loggers[logger_type]
        if logger_type == 'database':
            audit_logger = logger_class(db=db)
        elif logger_type == 'file':
            file_path = kwargs.get('file_path', settings.AUDIT_LOG_FILE)
            audit_logger = logger_class(file_path=file_path)
        else:
            audit_logger = logger_class()
        cls._logger_instances[cache_key] = audit_logger
        logger.debug(f'Created audit logger: {logger_type}')
        return audit_logger
    @classmethod
    def create_default_loggers(cls, db: Optional[AsyncSession]=None) -> List[AuditLogger]:
        loggers: List[AuditLogger] = []
        loggers.append(cls.create_logger('logging'))
        if hasattr(settings, 'AUDIT_LOG_TO_FILE') and settings.AUDIT_LOG_TO_FILE:
            loggers.append(cls.create_logger('file'))
        if db and hasattr(settings, 'AUDIT_LOG_TO_DB') and settings.AUDIT_LOG_TO_DB:
            loggers.append(cls.create_logger('database', db=db))
        return loggers