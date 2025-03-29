# Module: app.core.exceptions

**Path:** `app/core/exceptions/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorDetail, ErrorResponse, ErrorSeverity
from app.core.exceptions.domain import AuthException, AuthenticationException, BusinessException, InvalidStateException, OperationNotAllowedException, PermissionDeniedException, ResourceAlreadyExistsException, ResourceException, ResourceNotFoundException, ValidationException
from app.core.exceptions.system import ConfigurationException, DatabaseException, DataIntegrityException, NetworkException, RateLimitException, SecurityException, ServiceException, SystemException, TransactionException
from app.core.exceptions.handlers import app_exception_handler, generic_exception_handler, validation_exception_handler
```

## Global Variables
```python
__all__ = __all__ = [
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
```
