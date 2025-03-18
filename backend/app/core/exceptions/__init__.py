from __future__ import annotations

# Re-export all exceptions
from app.core.exceptions.base import (
    AppException,
    ErrorCategory,
    ErrorCode,
    ErrorDetail,
    ErrorResponse,
    ErrorSeverity,
)
from app.core.exceptions.http import (
    BadRequestException,
    PermissionDeniedException,
    AuthenticationException,
    ResourceNotFoundException,
    ResourceAlreadyExistsException,
)
from app.core.exceptions.database import (
    DatabaseException,
    DataIntegrityException,
    TransactionException,
)
from app.core.exceptions.business import (
    BusinessLogicException,
    ValidationException,
    OperationNotAllowedException,
    InvalidStateException,
)
from app.core.exceptions.network import (
    NetworkException,
    TimeoutException,
    ExternalServiceException,
    ServiceUnavailableException,
    RateLimitException,
)
from app.core.exceptions.security import (
    SecurityException,
    ConfigurationException,
)

# Export handler functions
from app.core.exceptions.handlers import (
    app_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    generic_exception_handler,
)

__all__ = [
    # Base
    "AppException", "ErrorCategory", "ErrorCode", "ErrorDetail",
    "ErrorResponse", "ErrorSeverity",

    # HTTP
    "BadRequestException", "PermissionDeniedException", "AuthenticationException",
    "ResourceNotFoundException", "ResourceAlreadyExistsException",

    # Database
    "DatabaseException", "DataIntegrityException", "TransactionException",

    # Business
    "BusinessLogicException", "ValidationException",
    "OperationNotAllowedException", "InvalidStateException",

    # Network
    "NetworkException", "TimeoutException", "ExternalServiceException",
    "ServiceUnavailableException", "RateLimitException",

    # Security
    "SecurityException", "ConfigurationException",

    # Handlers
    "app_exception_handler", "validation_exception_handler",
    "http_exception_handler", "generic_exception_handler",
]
