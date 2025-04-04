from __future__ import annotations
"\nAudit-specific exceptions for the application.\n\nThis module defines exceptions related to audit operations that integrate\nwith the application's exception system.\n"
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import ErrorCode
from app.core.exceptions.service import BackendError, CoreServiceException, ManagerError
class AuditException(CoreServiceException):
    def __init__(self, message: str, code: ErrorCode=ErrorCode.SERVICE_ERROR, details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, status_code: int=500, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=code, details=details, status_code=status_code, original_exception=original_exception)
class AuditBackendException(BackendError):
    def __init__(self, backend_name: str, operation: str='log_event', message: str='Audit backend operation failed', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        super().__init__(backend_name=backend_name, operation=operation, message=message, details=details, original_exception=original_exception)
class AuditManagerException(ManagerError):
    def __init__(self, operation: str, message: str='Audit manager operation failed', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        super().__init__(manager_name='audit', operation=operation, message=message, details=details, original_exception=original_exception)
class AuditConfigurationException(AuditException):
    def __init__(self, message: str='Invalid audit configuration', details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]=None, original_exception: Optional[Exception]=None) -> None:
        super().__init__(message=message, code=ErrorCode.CONFIGURATION_ERROR, details=details, original_exception=original_exception)