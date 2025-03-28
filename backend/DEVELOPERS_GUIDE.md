# Developer's Guide: Logging, Error Handling, Dependency Management, and Validation Systems

This guide provides a practical overview of the logging, error handling, exception, dependency management, and validation systems. Use it as a reference when implementing these components in your code.

## Table of Contents
1. [Logging System](#1-logging-system)
2. [Exception System](#2-exception-system)
3. [Error Handling System](#3-error-handling-system)
4. [Dependency Management System](#4-dependency-management-system)
5. [Validation System](#5-validation-system)
6. [Common Patterns](#6-common-patterns)

## 1. Logging System

The logging system provides structured, context-aware logging throughout the application. It supports both human-readable formatted logs for development and JSON logs for production.

### Key Features
- Structured logging with contextual information
- Request and user ID tracking
- Execution time logging
- Line numbers and file information for easy debugging
- Colorized development logs
- JSON-formatted production logs

### Basic Logging

```python
from app.logging import get_logger

# Create a logger for your module
logger = get_logger("app.your.module")

# Log at different levels
logger.debug("Debug information with context", item_id=123, status="pending")
logger.info("Operation completed successfully")
logger.warning("Something unexpected happened", details="connection timeout")
logger.error("Operation failed", error_code="DB_CONN_ERROR", retry_count=3)
logger.exception("Exception occurred during processing", exc_info=exception)
```

### Request Context Tracking

Request context is automatically managed by middleware, but you can also use it directly:

```python
from app.logging import request_context, set_user_id, clear_user_id

# Create a custom context for a set of operations
with request_context(request_id="manual-operation-123", user_id="admin"):
    logger.info("Performing administrative operation")
    # All logs within this context will include the specified request_id and user_id

# Set just the user ID
set_user_id("user-456")
logger.info("User context operation")  # Will include user_id=user-456

# Clear when done
clear_user_id()
```

### Performance Logging

Use decorators to automatically log execution time:

```python
from app.logging import log_execution_time, log_execution_time_async

# For synchronous functions
@log_execution_time()  # Optional parameters: logger, level
def process_data(data):
    # Processing logic
    return result
    # Will log start/end times and duration automatically

# For asynchronous functions
@log_execution_time_async()
async def fetch_data():
    # Async processing logic
    return result
```

### Configuration

The logging system is configured at application startup automatically. The configuration:
- Sets appropriate formatters for development vs. production
- Routes logs to console and/or files based on environment
- Configures structlog for structured output

In development:
- Colorized, human-readable logs with line numbers
- Contextual information for debugging

In production:
- JSON-formatted logs for machine processing
- Complete context for log aggregation systems

## 2. Exception System

The exception system provides standardized application exceptions with proper error codes, status codes, and response formatting.

### Available Exception Types

#### Resource Exceptions
```python
from app.core.exceptions import ResourceNotFoundException, ResourceAlreadyExistsException

# When a resource isn't found
raise ResourceNotFoundException(
    resource_type="User",
    resource_id="123",
    message="User not found"  # Optional - default message generated if omitted
)

# When a resource already exists
raise ResourceAlreadyExistsException(
    resource_type="User",
    identifier="user@example.com",
    field="email"  # Default is "id"
)
```

#### Authentication and Authorization Exceptions
```python
from app.core.exceptions import AuthenticationException, PermissionDeniedException

# Authentication failures
raise AuthenticationException(
    message="Invalid credentials",
    details={"reason": "expired_token"}
)

# Permission issues
raise PermissionDeniedException(
    action="edit",
    resource_type="Document",
    permission="documents:write"
)
```

#### Business Logic Exceptions
```python
from app.core.exceptions import BusinessException, InvalidStateException, OperationNotAllowedException

# General business rule violation
raise BusinessException(
    message="Cannot complete order",
    details={"reason": "insufficient_inventory"}
)

# Invalid state transitions
raise InvalidStateException(
    message="Cannot cancel approved order",
    current_state="approved",
    expected_state="pending"
)

# Disallowed operations
raise OperationNotAllowedException(
    message="Cannot delete system user",
    operation="delete",
    reason="system_account"
)
```

#### Validation Exceptions
```python
from app.core.exceptions import ValidationException

# Single validation error
raise ValidationException(
    message="Validation failed",
    errors=[
        {
            "loc": ["email"],
            "msg": "Invalid email format",
            "type": "value_error.email"
        }
    ]
)

# Multiple validation errors
raise ValidationException(
    message="Validation failed",
    errors=[
        {
            "loc": ["username"],
            "msg": "Username must be at least 3 characters",
            "type": "value_error.length"
        },
        {
            "loc": ["email"],
            "msg": "Invalid email format",
            "type": "value_error.email"
        }
    ]
)
```

#### System Exceptions
```python
from app.core.exceptions import (
    DatabaseException,
    NetworkException,
    ServiceException,
    ConfigurationException,
    SecurityException,
    RateLimitException
)

# Database errors
raise DatabaseException(
    message="Failed to insert record",
    details={"table": "users"}
)

# External service errors
raise ServiceException(
    message="Payment service unavailable",
    service_name="stripe"
)

# Rate limiting
raise RateLimitException(
    message="Too many requests",
    headers={"Retry-After": "60"}
)
```

## 3. Error Handling System

The error handling system provides utilities for reporting errors to various destinations and creating common exception types.

### Error Reporting

```python
from app.core.error import report_error, handle_exception
from app.core.error.base import ErrorContext

# Manual error reporting with context
async def process_payment(payment_data, user_id):
    try:
        # Payment processing logic
        result = await payment_gateway.process(payment_data)
        if not result.success:
            raise Exception(f"Payment failed: {result.error_message}")
    except Exception as e:
        # Create context with relevant information
        context = ErrorContext(
            function="process_payment",
            args=[],
            kwargs={"payment_data": payment_data},
            user_id=user_id,
            request_id=get_current_request_id()
        )
        # Report to all registered reporters
        await report_error(e, context)
        # Re-raise to be handled upstream
        raise

# Simplified error handling
def update_user_profile(user_id, data):
    try:
        # Update logic
        result = user_service.update(user_id, data)
        return result
    except Exception as e:
        # Automatically extracts context from current function
        handle_exception(e, user_id=user_id)
        raise
```

### Utility Functions

```python
from app.core.error import (
    ensure_not_none,
    resource_not_found,
    resource_already_exists,
    validation_error,
    permission_denied,
    business_logic_error
)

# Check for null values with automatic exception
def get_product(product_id):
    product = ensure_not_none(
        product_repository.get_by_id(product_id),
        resource_type="Product",
        resource_id=product_id
    )
    return product

# Create specific exceptions
def validate_user_creation(data):
    existing_user = user_repository.find_by_email(data["email"])
    if existing_user:
        raise resource_already_exists(
            resource_type="User",
            identifier=data["email"],
            field="email"
        )

    if not valid_email_format(data["email"]):
        raise validation_error(
            field="email",
            message="Invalid email format"
        )
```

### Error Service

```python
from app.core.dependency_manager import get_service

# Get the error service through dependency injection
error_service = get_service("error_service")

# Report an error
async def handle_process_failure(error, context_data):
    context = ErrorContext(
        function="process_data",
        kwargs=context_data,
        user_id=context_data.get("user_id")
    )
    await error_service.report_error(error, context)

# Create specific exceptions through the service
def check_authorization(user_id, resource, action):
    if not user_has_permission(user_id, resource, action):
        raise error_service.permission_denied(
            action=action,
            resource_type=resource.type,
            permission=f"{resource.type}:{action}"
        )
```

## 4. Dependency Management System

The dependency management system handles service registration, initialization, and dependency injection.

### Service Registration

```python
from app.core.dependency_manager import register_service

# Register a service factory function
@register_service
def get_notification_service(db=None):
    """Create and return a notification service instance."""
    return NotificationService(db)

# Register with explicit name
@register_service(name="email_sender")
def get_email_service():
    """Create and return an email service instance."""
    return EmailService(
        smtp_host=settings.SMTP_HOST,
        smtp_port=settings.SMTP_PORT
    )
```

### Getting Services

```python
from app.core.dependency_manager import get_dependency, get_service

# In FastAPI endpoints
@router.post("/users/{user_id}/notify")
async def notify_user(
    user_id: str,
    message: str,
    db: AsyncSession = Depends(get_db)
):
    # Get service with database session
    notification_service = get_service("notification_service", db=db)
    await notification_service.send_notification(user_id, message)
    return {"status": "notification sent"}

# Get by class name
from app.services.user_service import UserService
user_service = get_dependency(UserService.__name__, db=db)
```

### Dependency Injection

```python
from app.core.dependency_manager import inject_dependency, with_dependencies

# Inject a single dependency
@inject_dependency("audit_service")
def log_user_action(user_id, action, audit_service=None):
    """Log a user action using the injected audit service."""
    audit_service.log_action(user_id, action)

# Inject multiple dependencies
@with_dependencies(notifier="notification_service", audit="audit_service")
async def process_order(order_data, user_id, notifier=None, audit=None):
    """Process an order with multiple injected services."""
    # Process order...

    # Use injected services
    await notifier.send_notification(user_id, "Order processed")
    audit.log_action(user_id, "order_processed", order_id=order_data["id"])
```

### In Service Classes

```python
from app.core.dependency_manager import get_service

class UserService:
    def __init__(self, db):
        self.db = db
        # Get dependencies in constructor
        self.audit_service = get_service("audit_service", db=db)
        self.notification_service = get_service("notification_service", db=db)

    async def update_user(self, user_id, data):
        # Business logic
        user = await self.repository.update(user_id, data)

        # Use services
        await self.audit_service.log_user_update(user_id, data)
        await self.notification_service.notify_profile_update(user_id)

        return user
```

## 5. Validation System

The validation system provides comprehensive tools for validating data throughout the application, ensuring data integrity and consistency.

### Key Features
- Validation of various data types (emails, URLs, dates, etc.)
- Pydantic model validation
- Database-specific validations (e.g., uniqueness)
- Composite validation with multiple rules
- Integration with error handling and logging systems
- Extensible validator architecture

### Basic Validations

```python
from app.core.validation import (
    validate_email,
    validate_phone,
    validate_date,
    validate_length,
    validate_range,
    validate_regex,
    validate_required,
    validate_url,
    validate_uuid,
    validate_credit_card,
    validate_ip_address,
    validate_password_strength,
    validate_enum
)

# Simple validation functions return boolean results
is_valid_email = validate_email("user@example.com")
is_valid_phone = validate_phone("+12125551234")
is_valid_url = validate_url("https://example.com")
is_complex_password = validate_password_strength(
    "SecureP@ss123",
    min_length=10,
    require_lowercase=True,
    require_uppercase=True,
    require_digit=True,
    require_special=True
)

# Date validation with range constraints
from datetime import date
is_valid_date = validate_date(
    "2023-05-15",
    min_date=date(2023, 1, 1),
    max_date=date(2023, 12, 31),
    format_str="%Y-%m-%d"
)

# Enum validation
from enum import Enum
class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

is_valid_role = validate_enum("admin", UserRole)
```

### Pydantic Model Validation

```python
from app.core.validation import validate_data, validate_model
from pydantic import BaseModel, Field

# Define a Pydantic model
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(..., min_length=8)
    age: int = Field(..., ge=18)

# Validate input data against the model
try:
    user_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "Secret123",
        "age": 25
    }

    # Returns a validated model instance or raises ValidationException
    user = validate_data(user_data, UserCreate)
    print(f"Valid user: {user.username}, {user.email}")

except ValidationException as e:
    print(f"Validation failed: {e.errors}")
```

### Database Validations

```python
from app.core.validation import validate_unique
from sqlalchemy.ext.asyncio import AsyncSession

# Check if a value is unique in the database
async def create_user(db: AsyncSession, username: str, email: str):
    # Check username uniqueness
    is_username_unique = await validate_unique(
        field="username",
        value=username,
        model=User,
        db=db
    )

    if not is_username_unique:
        raise ValidationException(
            "Validation failed",
            errors=[{
                "loc": ["username"],
                "msg": f"Username '{username}' is already taken",
                "type": "unique_error"
            }]
        )

    # Check email uniqueness
    is_email_unique = await validate_unique(
        field="email",
        value=email,
        model=User,
        db=db
    )

    if not is_email_unique:
        raise ValidationException(
            "Validation failed",
            errors=[{
                "loc": ["email"],
                "msg": f"Email '{email}' is already registered",
                "type": "unique_error"
            }]
        )

    # Proceed with creation
    # ...
```

### Composite Validation

```python
from app.core.validation import validate_composite

# Define validation rules for multiple fields
validation_rules = {
    "username": {
        "required": True,
        "length": {"min_length": 3, "max_length": 50}
    },
    "email": {
        "required": True,
        "email": True
    },
    "password": {
        "required": True,
        "password": {
            "min_length": 8,
            "require_uppercase": True,
            "require_digit": True
        }
    },
    "age": {
        "required": True,
        "range": {"min_value": 18}
    }
}

# Validate data against the rules
user_data = {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "Secret123",
    "age": 25
}

is_valid, errors = validate_composite(user_data, validation_rules)

if not is_valid:
    for error in errors:
        print(f"Field: {error['loc'][0]}, Error: {error['msg']}")
```

### Using the Validation Service

```python
from app.core.dependency_manager import get_service
from app.core.validation import get_validation_service

# In FastAPI endpoints
@router.post("/users")
async def create_user(
    user_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
):
    # Get validation service with database session
    validation_service = get_validation_service(db)

    # Validate email
    if not validation_service.validate_email(user_data.get("email", "")):
        raise ValidationException(
            "Validation failed",
            errors=[{
                "loc": ["email"],
                "msg": "Invalid email format",
                "type": "value_error.email"
            }]
        )

    # Check uniqueness
    is_email_unique = await validation_service.validate_unique(
        "email", user_data["email"], User
    )

    if not is_email_unique:
        raise ValidationException(
            "Validation failed",
            errors=[{
                "loc": ["email"],
                "msg": "Email already registered",
                "type": "unique_error"
            }]
        )

    # Create user
    # ...

# Or through dependency manager
validation_service = get_service("validation_service", db=db)
```

### Custom Validators

```python
from app.core.validation import Validator, ValidationResult, register_validator

# Create a custom validator
class PostalCodeValidator(Validator):
    def validate(self, value: Any, country: str = "US", **kwargs: Any) -> ValidationResult:
        if not isinstance(value, str):
            return ValidationResult(
                is_valid=False,
                errors=[{
                    "msg": "Postal code must be a string",
                    "type": "type_error"
                }]
            )

        if country == "US":
            # US ZIP code validation (5 digits or ZIP+4 format)
            import re
            pattern = r"^\d{5}(?:-\d{4})?$"
            if not re.match(pattern, value):
                return ValidationResult(
                    is_valid=False,
                    errors=[{
                        "msg": "Invalid US ZIP code format",
                        "type": "format_error"
                    }]
                )
        elif country == "CA":
            # Canadian postal code validation
            import re
            pattern = r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$"
            if not re.match(pattern, value):
                return ValidationResult(
                    is_valid=False,
                    errors=[{
                        "msg": "Invalid Canadian postal code format",
                        "type": "format_error"
                    }]
                )
        else:
            # Generic validation for other countries
            if len(value.strip()) == 0:
                return ValidationResult(
                    is_valid=False,
                    errors=[{
                        "msg": "Postal code cannot be empty",
                        "type": "empty_error"
                    }]
                )

        return ValidationResult(is_valid=True)

# Register the custom validator
register_validator("postal_code", PostalCodeValidator)

# Use the custom validator
from app.core.validation import create_validator

postal_code_validator = create_validator("postal_code", country="US")
is_valid_zip = postal_code_validator("90210")
```

## 6. Common Patterns

### API Endpoint Error Handling

```python
@router.get("/users/{user_id}")
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        user_service = get_service("user_service", db=db)
        user = await user_service.get_user(user_id)
        return user
    except ResourceNotFoundException as e:
        # App exceptions are automatically converted to proper responses
        # by the exception handlers, so just re-raise
        raise
    except Exception as e:
        # For unexpected errors, report and re-raise
        handle_exception(e, user_id=user_id)
        raise
```

### Service Layer Error Handling and Logging

```python
class OrderService:
    def __init__(self, db):
        self.db = db
        self.error_service = get_service("error_service")
        self.logger = get_logger("app.domains.orders.service")

    async def create_order(self, order_data, user_id):
        self.logger.info("Creating order", user_id=user_id, items_count=len(order_data["items"]))

        # Validate inventory availability
        for item in order_data["items"]:
            product = await self.product_repository.get_by_id(item["product_id"])
            if not product:
                self.logger.warning("Product not found", product_id=item["product_id"])
                raise self.error_service.resource_not_found(
                    resource_type="Product",
                    resource_id=item["product_id"]
                )

            if product.stock < item["quantity"]:
                self.logger.warning(
                    "Insufficient inventory",
                    product_id=product.id,
                    requested=item["quantity"],
                    available=product.stock
                )
                raise self.error_service.business_logic_error(
                    message="Insufficient inventory",
                    details={
                        "product_id": product.id,
                        "requested": item["quantity"],
                        "available": product.stock
                    }
                )

        # Process order...
        self.logger.info("Order created successfully", order_id=new_order.id)
        return new_order
```

### Validation in Services

```python
class UserService:
    def __init__(self, db):
        self.db = db
        self.validation_service = get_service("validation_service", db=db)
        self.logger = get_logger("app.domains.users.service")

    async def create_user(self, user_data):
        self.logger.info("Creating new user", email=user_data.get("email"))

        # Validate data against schema
        try:
            validated_data = self.validation_service.validate_data(user_data, UserCreateSchema)
        except ValidationException as e:
            self.logger.warning("User data validation failed", errors=e.errors)
            raise

        # Check for unique email
        is_unique = await self.validation_service.validate_unique(
            "email", validated_data.email, User
        )

        if not is_unique:
            self.logger.warning("Email already exists", email=validated_data.email)
            raise ValidationException(
                "Validation error",
                errors=[{
                    "loc": ["email"],
                    "msg": "Email already registered",
                    "type": "unique_error"
                }]
            )

        # Create user
        user = User(**validated_data.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        self.logger.info("User created successfully", user_id=user.id)
        return user
```

### Logging Best Practices

1. **Use Structured Logging**
   ```python
   # Good - structured and searchable
   logger.info("User registered", user_id=user.id, email=user.email, registration_source="web")

   # Avoid - unstructured string concatenation
   logger.info(f"User {user.id} with email {user.email} registered from web")
   ```

2. **Choose Appropriate Log Levels**
    - `DEBUG`: Detailed information, typically useful only when diagnosing problems
    - `INFO`: Confirmation that things are working as expected
    - `WARNING`: An indication that something unexpected happened, but the application still works
    - `ERROR`: The application has encountered an error that prevents a function from working
    - `CRITICAL`: A serious error that prevents the application from continuing to function

3. **Include Context**
   ```python
   # Include relevant context with every log
   logger.info(
       "Payment processed",
       user_id=user.id,
       payment_id=payment.id,
       amount=payment.amount,
       status=payment.status
   )
   ```

4. **Use Request Context When Available**
   ```python
   # Request context is automatically included
   logger.info("Processing request")  # Will include request_id and user_id automatically
   ```

5. **Log at Service Boundaries**
   ```python
   # Log at service boundaries and important events
   logger.info("Starting external API call", service="stripe", action="create_payment")
   try:
       result = await stripe_client.create_payment(payment_data)
       logger.info("External API call succeeded", service="stripe", duration_ms=duration)
       return result
   except Exception as e:
       logger.exception("External API call failed", service="stripe", error=str(e))
       raise
   ```

6. **Use Decorators for Common Patterns**
   ```python
   @log_execution_time()
   def process_report(report_id):
       # Complex processing...
       return result
   ```

7. **Avoid Sensitive Information**
   ```python
   # Don't log passwords, tokens, or other secrets
   logger.info("User authentication", username=username)  # Good
   logger.info("User authentication", username=username, password=password)  # BAD!
   ```
