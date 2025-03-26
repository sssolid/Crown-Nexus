# Developer's Guide: Error Handling and Dependency Management Systems

This guide provides a practical overview of the error handling, exception, and dependency management systems. Use it as a reference when implementing these components in your code.

## 1. Exception System

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

## 2. Error Handling System

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

## 3. Dependency Management System

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

## 4. Common Patterns

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

### Service Layer Error Handling

```python
class OrderService:
    def __init__(self, db):
        self.db = db
        self.error_service = get_service("error_service")

    async def create_order(self, order_data, user_id):
        # Validate inventory availability
        for item in order_data["items"]:
            product = await self.product_repository.get_by_id(item["product_id"])
            if not product:
                raise self.error_service.resource_not_found(
                    resource_type="Product",
                    resource_id=item["product_id"]
                )

            if product.stock < item["quantity"]:
                raise self.error_service.business_logic_error(
                    message="Insufficient inventory",
                    details={
                        "product_id": product.id,
                        "requested": item["quantity"],
                        "available": product.stock
                    }
                )

        # Process order...
```
