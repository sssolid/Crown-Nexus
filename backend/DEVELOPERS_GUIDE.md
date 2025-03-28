# Developer's Guide: Logging, Error Handling, Dependency Management, Validation, and Metrics Systems

This guide provides a practical overview of the logging, error handling, exception, dependency management, validation, metrics, and rate limiting systems. Use it as a reference when implementing these components in your code.

## Table of Contents
1. [Logging System](#1-logging-system)
2. [Exception System](#2-exception-system)
3. [Error Handling System](#3-error-handling-system)
4. [Dependency Management System](#4-dependency-management-system)
5. [Validation System](#5-validation-system)
6. [Metrics System](#6-metrics-system)
7. [Pagination System](#7-pagination-system)
8. [Rate Limiting System](#8-rate-limiting-system)
9. [Common Patterns](#9-common-patterns)

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

## 6. Metrics System

The metrics system provides tools for measuring and monitoring application performance and behavior. It supports various metric types and integrates with Prometheus for visualization and alerting.

### Key Features
- Multiple metric types (counter, gauge, histogram, summary)
- Automatic tracking of HTTP requests, DB queries, service calls, and cache operations
- Timing decorators for function execution
- Prometheus integration
- Configurable metric collection and reporting

### Basic Usage

```python
from app.core.dependency_manager import get_service

# Get the metrics service
metrics_service = get_service("metrics_service")

# Create and use counter metrics
counter = metrics_service.create_counter(
    name="user_registrations_total",
    description="Total number of user registrations",
    labelnames=["source", "role"]
)

# Increment counter
metrics_service.increment_counter(
    "user_registrations_total",
    amount=1,
    labels={"source": "web", "role": "customer"}
)

# Create and use gauge metrics
gauge = metrics_service.create_gauge(
    name="active_users",
    description="Number of currently active users",
    labelnames=["tenant"]
)

# Set gauge value
metrics_service.set_gauge(
    "active_users",
    value=42,
    labels={"tenant": "main"}
)

# Create and use histogram metrics
histogram = metrics_service.create_histogram(
    name="order_processing_seconds",
    description="Time spent processing orders",
    labelnames=["type"],
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0]
)

# Observe histogram value
metrics_service.observe_histogram(
    "order_processing_seconds",
    value=1.7,
    labels={"type": "standard"}
)
```

### Tracking Operations

The metrics system provides pre-built trackers for common operations:

```python
from app.core.dependency_manager import get_service

metrics_service = get_service("metrics_service")

# Track HTTP request
metrics_service.track_request(
    method="GET",
    endpoint="/api/users",
    status_code=200,
    duration=0.125
)

# Track database query
metrics_service.track_db_query(
    operation="SELECT",
    entity="user",
    duration=0.087
)

# Track service call
metrics_service.track_service_call(
    component="external_api",
    action="get_weather",
    duration=0.342
)

# Track cache operation
metrics_service.track_cache_operation(
    operation="get",
    backend="redis",
    hit=True,
    duration=0.004,
    component="user_profile"
)
```

### Function Timing

Measure function performance with decorators:

```python
from app.core.dependency_manager import get_service
from app.core.metrics import MetricType

metrics_service = get_service("metrics_service")

# Timing synchronous functions
@metrics_service.timed_function(
    name="process_user_data_duration",
    metric_type=MetricType.HISTOGRAM
)
def process_user_data(user_id, data):
    # Processing logic
    return result

# Timing asynchronous functions with labels
@metrics_service.async_timed_function(
    name="fetch_external_data_duration",
    metric_type=MetricType.HISTOGRAM,
    labels_func=lambda resource_id, **kwargs: {"resource_type": resource_id.split("-")[0]}
)
async def fetch_external_data(resource_id):
    # Async processing logic
    return result

# Tracking in-progress operations
@metrics_service.async_timed_function(
    name="long_running_operation_duration",
    track_in_progress_flag=True,
    in_progress_metric="long_running_operations_in_progress"
)
async def long_running_operation():
    # Long-running operation logic
    return result
```

### Integration with Database Operations

Track database operation performance:

```python
from app.core.metrics import track_db_select, track_db_insert

# Track SELECT operations
@track_db_select(entity="user")
async def get_users_by_role(db, role):
    query = select(User).where(User.role == role)
    result = await db.execute(query)
    return list(result.scalars().all())

# Track INSERT operations
@track_db_insert(entity="order")
async def create_order(db, order_data):
    order = Order(**order_data)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order
```

### Middleware Integration

```python
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.dependency_manager import get_service
from app.core.metrics import MetricName, MetricTag

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        metrics_service = get_service("metrics_service")
        start_time = time.monotonic()

        # Track in-progress requests
        labels = {
            MetricTag.METHOD: request.method,
            MetricTag.ENDPOINT: request.url.path
        }
        metrics_service.track_in_progress(MetricName.HTTP_IN_PROGRESS, labels, 1)

        try:
            response = await call_next(request)
            duration = time.monotonic() - start_time

            # Track completed request
            metrics_service.track_request(
                method=request.method,
                endpoint=request.url.path,
                status_code=response.status_code,
                duration=duration,
                error_code=response.headers.get("X-Error-Code")
            )

            return response
        except Exception as e:
            duration = time.monotonic() - start_time

            # Track failed request
            metrics_service.track_request(
                method=request.method,
                endpoint=request.url.path,
                status_code=500,
                duration=duration,
                error_code=type(e).__name__
            )

            raise
        finally:
            # Ensure we decrement the in-progress counter
            metrics_service.track_in_progress(MetricName.HTTP_IN_PROGRESS, labels, -1)
```

### Configuration

Configure the metrics system at application startup:

```python
from app.core.metrics import MetricsConfig
from app.core.dependency_manager import get_service

# In app startup
async def startup():
    metrics_config = MetricsConfig(
        namespace="crown_nexus",
        subsystem="api",
        default_labels={"environment": settings.ENVIRONMENT.value},
        enable_prometheus=True,
        endpoint_port=9090
    )

    metrics_service = get_service("metrics_service")
    await metrics_service.initialize(metrics_config)
```

## 7. Pagination System

The pagination system provides standardized, flexible pagination for database queries, supporting both offset-based and cursor-based pagination approaches.

### Key Features
- Support for both offset-based and cursor-based pagination
- Integration with SQLAlchemy for efficient database queries
- Automatic counting and metadata calculation
- Customizable sort fields and directions
- Data transformation capabilities
- Type-safe interfaces with Pydantic models
- Comprehensive error handling
- Metrics tracking
- Easy integration through dependency injection

### Pagination Models

```python
from app.core.pagination import (
    OffsetPaginationParams,
    CursorPaginationParams,
    SortDirection,
    SortField
)
from pydantic import BaseModel

# Create offset-based pagination parameters
offset_params = OffsetPaginationParams(
    page=2,
    page_size=20,
    sort=[
        SortField(field="created_at", direction=SortDirection.DESC),
        SortField(field="id", direction=SortDirection.ASC)
    ]
)

# Create cursor-based pagination parameters
cursor_params = CursorPaginationParams(
    cursor="eyJpZCI6IjEyMyIsImNyZWF0ZWRfYXQiOiIyMDIzLTA1LTE1VDEyOjMwOjAwIn0=",
    limit=20,
    sort=[
        SortField(field="created_at", direction=SortDirection.DESC),
        SortField(field="id", direction=SortDirection.ASC)
    ]
)

# Define a Pydantic model for the response
class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime
```

### Basic Usage

```python
from app.core.pagination import paginate_with_offset, paginate_with_cursor
from sqlalchemy import select

# In a service or repository
async def get_users_paginated(db, params: OffsetPaginationParams):
    # Create a query
    query = select(User).where(User.is_active == True)

    # Apply pagination
    result = await paginate_with_offset(
        db=db,
        model_class=User,
        query=query,
        params=params,
        response_model=UserResponse
    )

    return result

# Converting pagination result to a response format
def to_response(pagination_result):
    return {
        "items": pagination_result.items,
        "metadata": {
            "page": pagination_result.page,
            "page_size": pagination_result.page_size,
            "total": pagination_result.total,
            "pages": pagination_result.pages,
            "has_next": pagination_result.has_next,
            "has_prev": pagination_result.has_prev
        }
    }
```

### Using the Pagination Service

```python
from app.core.dependency_manager import get_service
from app.core.pagination import get_pagination_service

# In FastAPI endpoints
@router.get("/users")
async def list_users(
    page: int = 1,
    page_size: int = 20,
    sort_by: str = "created_at",
    sort_order: SortDirection = SortDirection.DESC,
    db: AsyncSession = Depends(get_db)
):
    # Get pagination service with database session
    pagination_service = get_pagination_service(db)

    # Create pagination parameters
    params = OffsetPaginationParams(
        page=page,
        page_size=page_size,
        sort=[SortField(field=sort_by, direction=sort_order)]
    )

    # Create query
    query = select(User).where(User.is_active == True)

    # Apply pagination
    result = await pagination_service.paginate_with_offset(
        model_class=User,
        query=query,
        params=params,
        response_model=UserResponse
    )

    return {
        "items": result.items,
        "metadata": {
            "page": result.page,
            "page_size": result.page_size,
            "total": result.total,
            "pages": result.pages,
            "has_next": result.has_next,
            "has_prev": result.has_prev
        }
    }

# Cursor-based pagination example
@router.get("/users/cursor")
async def list_users_with_cursor(
    cursor: Optional[str] = None,
    limit: int = 20,
    sort_by: str = "created_at",
    sort_order: SortDirection = SortDirection.DESC,
    db: AsyncSession = Depends(get_db)
):
    pagination_service = get_pagination_service(db)

    params = CursorPaginationParams(
        cursor=cursor,
        limit=limit,
        sort=[SortField(field=sort_by, direction=sort_order)]
    )

    query = select(User).where(User.is_active == True)

    result = await pagination_service.paginate_with_cursor(
        model_class=User,
        query=query,
        params=params,
        response_model=UserResponse
    )

    return {
        "items": result.items,
        "metadata": {
            "total": result.total,
            "has_next": result.has_next,
            "has_prev": result.has_prev,
            "next_cursor": result.next_cursor
        }
    }
```

### Error Handling

```python
from app.core.pagination.exceptions import (
    PaginationException,
    InvalidPaginationParamsException,
    InvalidCursorException,
    InvalidSortFieldException
)

@router.get("/products")
async def list_products(
    page: int = 1,
    page_size: int = 20,
    sort_by: str = "name",
    sort_order: SortDirection = SortDirection.ASC,
    db: AsyncSession = Depends(get_db)
):
    try:
        pagination_service = get_pagination_service(db)

        params = OffsetPaginationParams(
            page=page,
            page_size=page_size,
            sort=[SortField(field=sort_by, direction=sort_order)]
        )

        query = select(Product)

        result = await pagination_service.paginate_with_offset(
            model_class=Product,
            query=query,
            params=params,
            response_model=ProductResponse
        )

        return to_response(result)
    except InvalidSortFieldException as e:
        # Handle invalid sort field
        raise HTTPException(
            status_code=422,
            detail=f"Invalid sort field: {e.details.get('field')}"
        )
    except InvalidPaginationParamsException as e:
        # Handle invalid pagination parameters
        raise HTTPException(
            status_code=422,
            detail=f"Invalid pagination parameters: {str(e)}"
        )
    except PaginationException as e:
        # Handle other pagination exceptions
        raise HTTPException(
            status_code=e.status_code,
            detail=str(e)
        )
```

### Custom Transformations

```python
from app.core.pagination import paginate_with_offset
from sqlalchemy import select, func

async def get_products_with_categories(db, params):
    # Join with categories
    query = (
        select(Product, Category)
        .join(Category, Product.category_id == Category.id)
        .where(Product.is_active == True)
    )

    # Define a custom transform function
    def transform_product(result):
        product, category = result
        return {
            "id": str(product.id),
            "name": product.name,
            "price": product.price,
            "category": {
                "id": str(category.id),
                "name": category.name
            }
        }

    # Apply pagination with custom transformation
    result = await paginate_with_offset(
        db=db,
        model_class=Product,
        query=query,
        params=params,
        transform_func=transform_product
    )

    return result
```

### Integration with Metrics

The pagination system automatically integrates with the metrics system to track performance:

```python
# These metrics are recorded automatically when using the pagination service
# - pagination_duration_seconds (histogram)
# - pagination_operations_total (counter)

# Manual tracking for custom pagination implementations
from app.core.dependency_manager import get_service

metrics_service = get_service("metrics_service")

async def custom_pagination(db, params):
    start_time = time.monotonic()
    error = None

    try:
        # Custom pagination logic
        # ...
        return result
    except Exception as e:
        error = type(e).__name__
        raise
    finally:
        duration = time.monotonic() - start_time
        metrics_service.observe_histogram(
            "custom_pagination_duration_seconds",
            duration,
            {"type": "custom", "error": str(error or "")}
        )
```

## 8. Rate Limiting System

The rate limiting system provides mechanisms to protect the application from excessive use by limiting the number of requests a client can make within a specified time window.

### Key Features
- Support for different rate limit strategies (IP-based, user-based, combined)
- Multiple configurable rate limit rules
- Both Redis-backed and in-memory implementations
- Path-specific rules and path exclusions
- Rate limit headers in responses
- Metrics tracking
- Integration with the exception system

### Rate Limit Models

```python
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy

# Create a basic rate limit rule
basic_rule = RateLimitRule(
    requests_per_window=100,
    window_seconds=60,
    strategy=RateLimitStrategy.IP
)

# Create a rule for specific paths
api_rule = RateLimitRule(
    requests_per_window=50,
    window_seconds=60,
    strategy=RateLimitStrategy.COMBINED,
    path_pattern="/api/v1/",
    exclude_paths=["/api/v1/health", "/api/v1/docs"]
)

# Create a rule with burst allowance
auth_rule = RateLimitRule(
    requests_per_window=20,
    window_seconds=60,
    strategy=RateLimitStrategy.IP,
    burst_multiplier=2.0,  # Allow up to 40 requests in bursts
    path_pattern="/api/v1/auth/"
)
```

### Basic Usage with Middleware

The simplest way to use rate limiting is through middleware:

```python
from fastapi import FastAPI
from app.middleware.rate_limiting import RateLimitMiddleware
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy

app = FastAPI()

# Add rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    rules=[
        RateLimitRule(
            requests_per_window=100,
            window_seconds=60,
            strategy=RateLimitStrategy.IP
        ),
        RateLimitRule(
            requests_per_window=20,
            window_seconds=60,
            strategy=RateLimitStrategy.IP,
            path_pattern="/api/v1/auth/"
        )
    ],
    use_redis=True,
    enable_headers=True,
    block_exceeding_requests=True
)
```

### Using the Rate Limiting Service

For more control, you can use the rate limiting service directly:

```python
from app.core.dependency_manager import get_service
from app.core.rate_limiting import get_rate_limiting_service
from app.core.rate_limiting.models import RateLimitRule
from app.core.rate_limiting.exceptions import RateLimitExceededException

# In FastAPI endpoints
@router.post("/custom-rate-limited")
async def custom_rate_limited_endpoint(
    request: Request,
    data: Dict[str, Any]
):
    # Get rate limiting service
    rate_limiting_service = get_rate_limiting_service()

    # Define custom rule for this endpoint
    rule = RateLimitRule(
        requests_per_window=5,
        window_seconds=60
    )

    # Get key for current request
    key = rate_limiting_service.get_key_for_request(request, rule)

    # Check rate limit
    is_limited, count, limit = await rate_limiting_service.is_rate_limited(key, rule)

    # Handle rate limit exceeded
    if is_limited:
        headers = {
            "X-RateLimit-Limit": str(limit),
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(rule.window_seconds),
            "Retry-After": str(rule.window_seconds)
        }

        raise RateLimitExceededException(
            message="Custom rate limit exceeded",
            details={"path": request.url.path},
            headers=headers,
            reset_seconds=rule.window_seconds
        )

    # Process the request
    # ...

    return {"success": True, "rate_limit": {"current": count, "limit": limit}}
```

### Manual Rate Limiting

For specific operations that need rate limiting within the application:

```python
from app.core.rate_limiting.utils import check_rate_limit

async def send_email(user_id: str, subject: str, body: str):
    # Check if user has exceeded email sending limit
    key = f"email:{user_id}"
    is_limited, count, reset_seconds = await check_rate_limit(
        key=key,
        max_requests=10,  # 10 emails
        window_seconds=3600  # per hour
    )

    if is_limited:
        logger.warning(
            "Email rate limit exceeded",
            user_id=user_id,
            current_count=count,
            reset_seconds=reset_seconds
        )
        raise RateLimitExceededException(
            message="Email sending limit exceeded",
            details={"user_id": user_id, "limit": 10, "window": "1 hour"},
            reset_seconds=reset_seconds
        )

    # Send email
    # ...

    return {"success": True}
```

### Exception Handling

```python
from fastapi import Request, HTTPException
from app.core.rate_limiting.exceptions import RateLimitExceededException

@app.exception_handler(RateLimitExceededException)
async def rate_limit_exception_handler(request: Request, exc: RateLimitExceededException):
    # Get response headers from exception
    headers = {}
    if isinstance(exc.details, dict) and "headers" in exc.details:
        headers = exc.details["headers"]

    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "message": str(exc),
            "code": "RATE_LIMIT_EXCEEDED",
            "retry_after": headers.get("Retry-After", "60")
        },
        headers=headers
    )
```

### Integration with Metrics

The rate limiting system automatically integrates with the metrics system to track performance:

```python
# These metrics are recorded automatically when using the rate limiting service
# - rate_limit_exceeded_total (counter)
# - rate_limiting_requests_total (counter)
# - rate_limiting_middleware_duration_seconds (histogram)
# - rate_limiting_check_duration_seconds (histogram)
# - rate_limiting_checks_total (counter)

# Example metrics queries for Prometheus:
# - rate(rate_limit_exceeded_total[5m]) # Rate of exceeded limits in the last 5 minutes
# - sum by (path) (rate_limit_exceeded_total) # Total exceeded limits by path
# - histogram_quantile(0.95, sum(rate_limiting_check_duration_seconds_bucket) by (le)) # 95th percentile rate limit check duration
```

## 9. Common Patterns

### API Endpoint Error Handling with Rate Limiting

```python
@router.get("/products")
async def list_products(
    request: Request,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Get product service
        product_service = get_service("product_service", db=db)

        # Apply pagination
        pagination_params = OffsetPaginationParams(
            page=page,
            page_size=page_size,
            sort=[SortField(field="created_at", direction=SortDirection.DESC)]
        )

        result = await product_service.list_products(pagination_params)
        return result
    except RateLimitExceededException as e:
        # This exception is already properly formatted by the exception handlers
        raise
    except ResourceNotFoundException as e:
        # App exceptions are automatically converted to proper responses
        raise
    except Exception as e:
        # For unexpected errors, report and re-raise
        handle_exception(e, request_id=getattr(request.state, "request_id", None))
        raise
```

### Standard API Endpoint Error Handling

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

### Rate Limited Service Methods

```python
class AnalyticsService:
    def __init__(self, db):
        self.db = db
        self.logger = get_logger("app.domains.analytics.service")
        self.rate_limiting_service = get_service("rate_limiting_service")

    async def generate_report(self, user_id: str, report_type: str):
        """Generate a complex analytical report.

        This method is rate limited to prevent resource abuse.
        """
        self.logger.info("Generate report requested", user_id=user_id, report_type=report_type)

        # Define a rate limit rule for report generation
        rule = RateLimitRule(
            requests_per_window=5,  # 5 reports
            window_seconds=3600,    # per hour
            strategy=RateLimitStrategy.USER
        )

        # Use user ID directly as the key for consistent limits
        key = f"report_generation:{user_id}"

        # Check rate limit
        is_limited, count, limit = await self.rate_limiting_service.is_rate_limited(key, rule)

        if is_limited:
            self.logger.warning(
                "Report generation rate limit exceeded",
                user_id=user_id,
                report_type=report_type,
                count=count,
                limit=limit
            )

            raise RateLimitExceededException(
                message="Report generation limit exceeded",
                details={
                    "user_id": user_id,
                    "limit": limit,
                    "window": "1 hour",
                    "report_type": report_type
                }
            )

        # Generate report
        self.logger.info(
            "Generating report",
            user_id=user_id,
            report_type=report_type,
            remaining_limit=limit - count
        )

        # Complex report logic...

        self.logger.info("Report generated successfully", user_id=user_id, report_type=report_type)
        return report
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

### Metrics in Services

```python
class ProductService:
    def __init__(self, db):
        self.db = db
        self.metrics_service = get_service("metrics_service")
        self.logger = get_logger("app.domains.products.service")

    @track_db_select(entity="product")
    async def search_products(self, query, filters=None):
        self.logger.info("Searching products", query=query, filters=filters)

        # Track search operation
        start_time = time.monotonic()
        result_count = 0
        error = None

        try:
            # Perform search
            products = await self.repository.search(query, filters)
            result_count = len(products)
            return products
        except Exception as e:
            error = type(e).__name__
            raise
        finally:
            duration = time.monotonic() - start_time

            # Track search metrics
            self.metrics_service.track_service_call(
                component="product_service",
                action="search",
                duration=duration,
                error=error
            )

            # Track result count
            if not error:
                self.metrics_service.set_gauge(
                    "product_search_result_count",
                    value=result_count,
                    labels={"query_type": "text" if query else "filter"}
                )
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
