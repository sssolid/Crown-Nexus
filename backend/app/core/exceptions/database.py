from __future__ import annotations
from typing import Any, Dict, Optional

from app.core.exceptions.base import AppException, ErrorCode, ErrorSeverity, ErrorCategory

class DatabaseException(AppException):
    """Exception raised for database errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.DATABASE_ERROR,
        details: Any = None,
        status_code: int = 500,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the database exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.DATABASE,
            original_exception=original_exception
        )

class DataIntegrityException(DatabaseException):
    """Exception raised for data integrity errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.DATA_INTEGRITY_ERROR,
        details: Any = None,
        status_code: int = 409,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the data integrity exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            original_exception=original_exception
        )

class TransactionException(DatabaseException):
    """Exception raised for transaction errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.TRANSACTION_FAILED,
        details: Any = None,
        status_code: int = 500,
        original_exception: Optional[Exception] = None
    ) -> None:
        """Initialize the transaction exception."""
        super().__init__(
            message=message,
            code=code,
            details=details,
            status_code=status_code,
            original_exception=original_exception
        )
