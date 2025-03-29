from __future__ import annotations
'Autocare domain exceptions.\n\nThis module defines exceptions specific to the autocare domain and its subdomains.\nThese exceptions handle various error cases when working with VCdb, PCdb, PAdb, Qdb,\nACES, and PIES data.\n'
from app.core.exceptions import BusinessException, ResourceNotFoundException
class AutocareException(BusinessException):
    def __init__(self, message: str, details: dict=None) -> None:
        super().__init__(message=message, details=details)
class InvalidVehicleDataException(AutocareException):
    def __init__(self, message: str='Invalid vehicle data', details: dict=None) -> None:
        super().__init__(message=message, details=details)
class InvalidPartDataException(AutocareException):
    def __init__(self, message: str='Invalid part data', details: dict=None) -> None:
        super().__init__(message=message, details=details)
class MappingNotFoundException(ResourceNotFoundException):
    def __init__(self, resource_id: str, details: dict=None) -> None:
        super().__init__(resource_type='FitmentMapping', resource_id=resource_id, message=f'Fitment mapping with ID {resource_id} not found', details=details)
class ImportException(AutocareException):
    def __init__(self, message: str='Failed to import data', details: dict=None) -> None:
        super().__init__(message=message, details=details)
class ExportException(AutocareException):
    def __init__(self, message: str='Failed to export data', details: dict=None) -> None:
        super().__init__(message=message, details=details)
class VCdbException(AutocareException):
    def __init__(self, message: str='VCdb operation failed', details: dict=None) -> None:
        super().__init__(message=message, details=details)
class PCdbException(AutocareException):
    def __init__(self, message: str='PCdb operation failed', details: dict=None) -> None:
        super().__init__(message=message, details=details)
class PAdbException(AutocareException):
    def __init__(self, message: str='PAdb operation failed', details: dict=None) -> None:
        super().__init__(message=message, details=details)
class QdbException(AutocareException):
    def __init__(self, message: str='Qdb operation failed', details: dict=None) -> None:
        super().__init__(message=message, details=details)