# /backend/app/services/validation_service.py
from __future__ import annotations

import re
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Type, Union, cast

from pydantic import BaseModel, Field, ValidationError, root_validator, validator

from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

logger = get_logger("app.services.validation_service")

class ValidationService:
    """Service for validating data.
    
    This service provides standardized validation across the application,
    with support for common validation patterns.
    """
    
    def __init__(self) -> None:
        """Initialize the validation service."""
        self.logger = logger
        self.validators: Dict[str, callable] = {
            "email": self.validate_email,
            "phone": self.validate_phone,
            "date": self.validate_date,
            "length": self.validate_length,
            "range": self.validate_range,
            "regex": self.validate_regex,
            "required": self.validate_required,
            "unique": self.validate_unique,
        }
        
    async def initialize(self) -> None:
        """Initialize service resources."""
        self.logger.debug("Initializing validation service")
        
    async def shutdown(self) -> None:
        """Release service resources."""
        self.logger.debug("Shutting down validation service")
        
    def validate_data(
        self, 
        data: Dict[str, Any], 
        schema_class: Type[BaseModel]
    ) -> BaseModel:
        """Validate data against a Pydantic schema.
        
        Args:
            data: Data to validate
            schema_class: Pydantic schema class
            
        Returns:
            BaseModel: Validated schema
            
        Raises:
            ValidationException: If validation fails
        """
        try:
            schema = schema_class(**data)
            return schema
        except ValidationError as e:
            self.logger.warning(f"Validation error: {str(e)}")
            
            # Format error for API response
            errors = []
            for error in e.errors():
                errors.append({
                    "loc": list(error["loc"]),
                    "msg": error["msg"],
                    "type": error["type"],
                })
                
            raise ValidationException(
                "Validation error",
                code="validation_error",
                details={"errors": errors},
                status_code=400,
            )
            
    def validate_email(self, email: str) -> bool:
        """Validate an email address.
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
        
    def validate_phone(self, phone: str) -> bool:
        """Validate a phone number.
        
        Args:
            phone: Phone number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Remove common formatting
        cleaned = re.sub(r"[\s\-\(\).]", "", phone)
        # Check for valid length and digits
        return bool(re.match(r"^\+?[0-9]{10,15}$", cleaned))
        
    def validate_date(
        self, 
        value: Union[str, date, datetime], 
        min_date: Optional[Union[str, date, datetime]] = None,
        max_date: Optional[Union[str, date, datetime]] = None,
        format_str: Optional[str] = None,
    ) -> bool:
        """Validate a date.
        
        Args:
            value: Date to validate
            min_date: Minimum allowed date
            max_date: Maximum allowed date
            format_str: Date format string for string dates
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Convert to date object if string
        if isinstance(value, str):
            if not format_str:
                format_str = "%Y-%m-%d"
            try:
                value = datetime.strptime(value, format_str).date()
            except ValueError:
                return False
                
        # Convert to date object if datetime
        if isinstance(value, datetime):
            value = value.date()
            
        # Convert min and max dates if provided
        if min_date and isinstance(min_date, str):
            if not format_str:
                format_str = "%Y-%m-%d"
            try:
                min_date = datetime.strptime(min_date, format_str).date()
            except ValueError:
                return False
                
        if max_date and isinstance(max_date, str):
            if not format_str:
                format_str = "%Y-%m-%d"
            try:
                max_date = datetime.strptime(max_date, format_str).date()
            except ValueError:
                return False
                
        # Convert min_date from datetime to date if needed
        if min_date and isinstance(min_date, datetime):
            min_date = min_date.date()
            
        # Convert max_date from datetime to date if needed
        if max_date and isinstance(max_date, datetime):
            max_date = max_date.date()
            
        # Check min and max constraints
        if min_date and value < min_date:
            return False
        if max_date and value > max_date:
            return False
            
        return True
        
    def validate_length(
        self, 
        value: str, 
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
    ) -> bool:
        """Validate string length.
        
        Args:
            value: String to validate
            min_length: Minimum allowed length
            max_length: Maximum allowed length
            
        Returns:
            bool: True if valid, False otherwise
        """
        if min_length is not None and len(value) < min_length:
            return False
        if max_length is not None and len(value) > max_length:
            return False
        return True
        
    def validate_range(
        self, 
        value: Union[int, float], 
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
    ) -> bool:
        """Validate a numeric value within a range.
        
        Args:
            value: Numeric value to validate
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            
        Returns:
            bool: True if valid, False otherwise
        """
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True
        
    def validate_regex(self, value: str, pattern: str) -> bool:
        """Validate a string against a regex pattern.
        
        Args:
            value: String to validate
            pattern: Regex pattern
            
        Returns:
            bool: True if valid, False otherwise
        """
        return bool(re.match(pattern, value))
        
    def validate_required(self, value: Any) -> bool:
        """Validate that a value is not None or empty.
        
        Args:
            value: Value to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, (list, dict, set)) and not value:
            return False
        return True
        
    async def validate_unique(
        self, 
        field: str, 
        value: Any, 
        model: Any, 
        db: Any,
        exclude_id: Optional[str] = None,
    ) -> bool:
        """Validate that a field value is unique.
        
        Args:
            field: Field name
            value: Field value
            model: SQLAlchemy model
            db: Database session
            exclude_id: ID to exclude from the check
            
        Returns:
            bool: True if valid, False otherwise
        """
        from sqlalchemy import select
        
        # Build query
        query = select(model).filter(getattr(model, field) == value)
        
        # Exclude current entity if ID provided
        if exclude_id:
            query = query.filter(model.id != exclude_id)
            
        # Execute query
        result = await db.execute(query)
        
        # Check if any results
        return result.first() is None
