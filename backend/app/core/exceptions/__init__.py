# /backend/app/core/exceptions/__init__.py
from __future__ import annotations

"""Exception system for the application.

This module exports a simplified exception hierarchy for use throughout the
application, providing consistent error handling and reporting.
"""

# Base exceptions and types
from app.core.exceptions.base import (
    AppException,
    ErrorCategory,
    ErrorCode,
    ErrorDetail,
    ErrorResponse,
    ErrorSeverity,
)

# Domain exceptions
from app.core.exceptions.domain import (
    AuthException,
    AuthenticationException,
    BusinessException,
    InvalidStateException,
    OperationNotAllowedException,
    PermissionDeniedException,
    ResourceAlreadyExistsException,
    ResourceException,
    ResourceNotFoundException,
    ValidationException,
)

# System exceptions
from app.core.exceptions.system import (
    ConfigurationException,
    DatabaseException,
    DataIntegrityException,
    NetworkException,
    RateLimitException,
    SecurityException,
    ServiceException,
    SystemException,
    TransactionException,
)

# Exception handlers
from app.core.exceptions.handlers import (
    app_exception_handler,
    generic_exception_handler,
    validation_exception_handler,
)

__all__ = [
    # Base
    "AppException",
    "ErrorCategory",
    "ErrorCode",
    "ErrorDetail",
    "ErrorResponse",
    "ErrorSeverity",
    # Domain
    "AuthException",
    "AuthenticationException",
    "BusinessException",
    "InvalidStateException",
    "OperationNotAllowedException",
    "PermissionDeniedException",
    "ResourceAlreadyExistsException",
    "ResourceException",
    "ResourceNotFoundException",
    "ValidationException",
    # System
    "ConfigurationException",
    "DatabaseException",
    "DataIntegrityException",
    "NetworkException",
    "RateLimitException",
    "SecurityException",
    "ServiceException",
    "SystemException",
    "TransactionException",
    # Handlers
    "app_exception_handler",
    "generic_exception_handler",
    "validation_exception_handler",
]
