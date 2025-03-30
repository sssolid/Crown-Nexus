# Developer's Guide: Application Core Systems

This guide provides a practical overview of the core systems used throughout the application. Use it as a reference when implementing features and integrating with these systems.

## Table of Contents
1. [Logging System](#1-logging-system)
2. [Exception System](#2-exception-system)
3. [Error Handling System](#3-error-handling-system)
4. [Dependency Management System](#4-dependency-management-system)
5. [Validation System](#5-validation-system)
6. [Metrics System](#6-metrics-system)
7. [Pagination System](#7-pagination-system)
8. [Rate Limiting System](#8-rate-limiting-system)
9. [Cache System](#9-cache-system)
10. [Event System](#10-event-system)
11. [Permission System](#11-permission-system)
12. [Security System](#12-security-system)
13. [Middleware System](#13-middleware-system)
14. [Common Patterns and Best Practices](#14-common-patterns-and-best-practices)

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

### Caching with Fallback and Metrics

This pattern demonstrates how to implement robust caching with proper fallback mechanisms, metrics tracking, and integration with the error handling system:

```python
from app.core.dependency_manager import get_service
from app.core.cache.exceptions import CacheOperationException
from app.logging import get_logger
from app.core.error import handle_exception
import time

logger = get_logger("app.services.product_service")

class ProductService:
    def __init__(self, db):
        self.db = db
        self.cache_service = get_service("cache_service")
        self.metrics_service = get_service("metrics_service")

    async def get_product_with_details(self, product_id: str):
        """Get product with complete details, using caching with proper fallback.

        This method demonstrates caching with:
        1. Proper key generation
        2. Error handling with fallback
        3. Metrics tracking
        4. Cache invalidation on updates
        """
        logger.info("Fetching product with details", product_id=product_id)

        # Define cache key
        cache_key = f"product:details:{product_id}"

        # Start metrics timer
        start_time = time.monotonic()
        cache_hit = False

        try:
            # Try to get from cache first
            cached_data = await self.cache_service.get(cache_key)

            if cached_data is not None:
                logger.debug("Cache hit for product details", product_id=product_id)
                cache_hit = True
                return cached_data

            logger.debug("Cache miss for product details", product_id=product_id)

            # Get from database
            product = await self.db.execute(
                select(Product).where(Product.id == product_id)
            )
            product = product.scalar_one_or_none()

            if not product:
                logger.warning("Product not found", product_id=product_id)
                return None

            # Get additional data
            reviews = await self.db.execute(
                select(Review).where(Review.product_id == product_id)
            )
            reviews = list(reviews.scalars().all())

            inventory = await self.inventory_repository.get_levels(product_id)
            related_products = await self.get_related_products(product_id)

            # Combine into a complete response
            result = {
                "product": product.to_dict(),
                "reviews": [r.to_dict() for r in reviews],
                "inventory": inventory,
                "related_products": related_products,
                "calculated_rating": self._calculate_rating(reviews)
            }

            # Cache the result (15 minutes TTL)
            try:
                await self.cache_service.set(
                    cache_key,
                    result,
                    ttl=900,
                    tags=["products", f"product:{product_id}"]
                )
            except CacheOperationException as cache_err:
                # Log but don't fail if caching fails
                logger.warning(
                    "Failed to cache product details",
                    product_id=product_id,
                    error=str(cache_err)
                )

            return result

        except Exception as e:
            # Handle and report the exception
            handle_exception(e, product_id=product_id)
            logger.error(
                "Error fetching product details",
                product_id=product_id,
                error=str(e)
            )
            raise

        finally:
            # Record metrics regardless of success/failure
            duration = time.monotonic() - start_time
            self.metrics_service.observe_histogram(
                "product_details_duration_seconds",
                duration,
                {
                    "cache_hit": str(cache_hit),
                    "product_id": product_id[:5]  # First 5 chars for cardinality
                }
            )

    async def update_product(self, product_id: str, data: dict, user_id: str):
        """Update product data and invalidate related caches."""
        logger.info("Updating product", product_id=product_id, user_id=user_id)

        try:
            # Update in database
            product = await self.repository.update(product_id, data, user_id)

            # Invalidate caches
            try:
                # Invalidate specific product cache
                await self.cache_service.delete(f"product:details:{product_id}")

                # Invalidate any list caches that might contain this product
                await self.cache_service.invalidate_pattern(f"products:list:*")

                # If using Redis with tags
                redis_backend = self.cache_service._get_backend("redis")
                if hasattr(redis_backend, "get_set_members"):
                    # Invalidate all caches tagged with this product
                    tag_key = f"cache:tag:product:{product_id}"
                    tagged_keys = await redis_backend.get_set_members(tag_key)
                    if tagged_keys:
                        await self.cache_service.delete_many(tagged_keys)
                        await redis_backend.delete(tag_key)

            except Exception as cache_err:
                # Log but continue if cache invalidation fails
                logger.warning(
                    "Failed to invalidate cache for product update",
                    product_id=product_id,
                    error=str(cache_err)
                )

            # Audit log the update
            audit_service = get_service("audit_service")
            await audit_service.log_action(
                user_id=user_id,
                action="product_update",
                resource_id=product_id,
                details={"fields_updated": list(data.keys())}
            )

            return product

        except Exception as e:
            handle_exception(e, product_id=product_id, user_id=user_id)
            raise
```

This pattern demonstrates several important practices:

1. **Proper cache key generation** - Using consistent, structured cache keys
2. **Error handling with fallback** - Gracefully handling cache failures without affecting core functionality
3. **Cache invalidation strategy** - Both targeted invalidation and pattern-based invalidation
4. **Metrics tracking** - Recording performance metrics for both cache hits and misses
5. **Integration with other systems** - Working with logging, metrics, and error handling
6. **Tag-based invalidation** - Using Redis tags for grouped invalidation
7. **Audit logging** - Recording significant data changes

### Event-Driven Architecture Patterns

#### Event-Based Workflow

This pattern demonstrates using events to create a decoupled workflow:

```python
# In OrderService
async def place_order(self, order_data, user_id):
    """Create an order and publish events for subsequent processing."""
    self.logger.info("Creating order", user_id=user_id, items_count=len(order_data["items"]))

    # Create order in database
    order = Order(
        user_id=user_id,
        items=order_data["items"],
        status="pending",
        total_amount=calculate_total(order_data["items"])
    )
    self.db.add(order)
    await self.db.commit()
    await self.db.refresh(order)

    # Publish order created event
    event_service = get_service("event_service")
    await event_service.publish(
        event_name="order.created",
        payload={
            "order_id": str(order.id),
            "user_id": user_id,
            "items": order_data["items"],
            "total_amount": order.total_amount
        }
    )

    self.logger.info("Order created successfully", order_id=str(order.id))
    return order

# In InventoryService as an event handler
@event_service.event_handler("order.created")
async def reserve_inventory(event):
    """Reserve inventory items when an order is created."""
    order_data = event["data"]
    logger.info("Reserving inventory for order", order_id=order_data["order_id"])

    # Reserve inventory
    for item in order_data["items"]:
        await inventory_repository.reserve(
            product_id=item["product_id"],
            quantity=item["quantity"],
            order_id=order_data["order_id"]
        )

    # Publish inventory reserved event
    await event_service.publish(
        event_name="inventory.reserved",
        payload={
            "order_id": order_data["order_id"],
            "user_id": order_data["user_id"],
            "items": order_data["items"]
        }
    )

    logger.info("Inventory reserved for order", order_id=order_data["order_id"])

# In PaymentService as an event handler
@event_service.event_handler("inventory.reserved")
async def process_payment(event):
    """Process payment after inventory is reserved."""
    order_data = event["data"]
    logger.info("Processing payment for order", order_id=order_data["order_id"])

    # Get payment details from user profile
    user = await user_repository.get_by_id(order_data["user_id"])

    # Process payment
    payment_result = await payment_gateway.process_payment(
        amount=order_data["total_amount"],
        payment_method=user.default_payment_method,
        order_id=order_data["order_id"]
    )

    if payment_result.success:
        # Publish payment succeeded event
        await event_service.publish(
            event_name="payment.succeeded",
            payload={
                "order_id": order_data["order_id"],
                "payment_id": payment_result.payment_id,
                "amount": order_data["total_amount"]
            }
        )
        logger.info("Payment succeeded for order", order_id=order_data["order_id"])
    else:
        # Publish payment failed event
        await event_service.publish(
            event_name="payment.failed",
            payload={
                "order_id": order_data["order_id"],
                "error": payment_result.error,
                "reason": payment_result.error_message
            }
        )
        logger.error("Payment failed for order", order_id=order_data["order_id"], error=payment_result.error)

# In OrderService as event handlers for payment outcomes
@event_service.event_handler("payment.succeeded")
async def finalize_order(event):
    """Finalize the order after successful payment."""
    payment_data = event["data"]
    logger.info("Finalizing order after payment", order_id=payment_data["order_id"])

    # Update order status
    order = await order_repository.get_by_id(payment_data["order_id"])
    order.status = "completed"
    order.payment_id = payment_data["payment_id"]
    await db.commit()

    # Publish order completed event
    await event_service.publish(
        event_name="order.completed",
        payload={
            "order_id": payment_data["order_id"],
            "user_id": order.user_id,
            "total_amount": payment_data["amount"],
            "status": "completed"
        }
    )

    logger.info("Order finalized successfully", order_id=payment_data["order_id"])

@event_service.event_handler("payment.failed")
async def handle_payment_failure(event):
    """Handle payment failure by updating order and releasing inventory."""
    payment_data = event["data"]
    logger.info("Handling payment failure", order_id=payment_data["order_id"])

    # Update order status
    order = await order_repository.get_by_id(payment_data["order_id"])
    order.status = "payment_failed"
    order.failure_reason = payment_data["reason"]
    await db.commit()

    # Publish event to release inventory
    await event_service.publish(
        event_name="inventory.release_requested",
        payload={
            "order_id": payment_data["order_id"],
            "reason": "payment_failed"
        }
    )

    logger.info("Order marked as payment failed", order_id=payment_data["order_id"])
```

This event-driven workflow demonstrates several benefits:
1. **Decoupling** - Each service focuses on its own responsibility
2. **Scalability** - Services can scale independently
3. **Resilience** - If one part fails, other parts can continue or retry
4. **Traceability** - The entire workflow is trackable through events
5. **Extensibility** - New steps can be added by subscribing to existing events
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

## 9. Cache System

The cache system provides a flexible, configurable caching mechanism that supports multiple backends (memory, Redis, etc.) and offers various caching strategies.

### Key Features
- Multiple cache backends (Memory, Redis, Null)
- Key generation utilities for consistent caching
- Function decorators for easy caching
- Integration with metrics system
- Customizable TTL (time-to-live)
- Cache invalidation patterns
- Tagged caching for bulk invalidation
- Exception handling and resilience
- Service pattern for dependency injection

### Basic Usage

```python
from app.core.dependency_manager import get_service

# Get the cache service
cache_service = get_service("cache_service")

# Basic cache operations
async def get_user_profile(user_id: str):
    # Try to get from cache first
    cache_key = f"user:profile:{user_id}"
    cached_profile = await cache_service.get(cache_key)

    if cached_profile is not None:
        return cached_profile

    # Not in cache, fetch from database
    profile = await user_repository.get_profile(user_id)

    # Store in cache for future requests (TTL: 10 minutes)
    await cache_service.set(cache_key, profile, ttl=600)

    return profile
```

### Using Decorators

The cache system provides decorators for easy function-level caching:

```python
from app.core.cache import cached, invalidate_cache

# Cache the result of this function for 5 minutes
@cached(ttl=300)
async def get_product_details(product_id: str):
    # This expensive operation will only run on cache misses
    result = await product_repository.get_details(product_id)
    return result

# Invalidate cache entries when data changes
@invalidate_cache(pattern="product:*")
async def update_product(product_id: str, data: dict):
    # This will invalidate all cache keys matching the pattern
    await product_repository.update(product_id, data)
    return {"status": "updated"}
```

### Advanced Caching Patterns

```python
from app.core.cache import cached, cache_aside, memoize
from app.core.cache.keys import generate_model_key, generate_list_key

# Memoize an expensive function (in-memory caching)
@memoize(ttl=60)  # 60 seconds
def calculate_complex_value(input_value: int):
    # Complex calculation
    return result

# Cache using custom key generation
@cache_aside(
    key_func=lambda category_id, **kwargs: generate_list_key(
        prefix="products",
        model_name="product",
        filters={"category_id": category_id}
    ),
    ttl=600,
    tags=["products", "catalog"]
)
async def get_products_by_category(category_id: str):
    # Fetch from database
    return await product_repository.list_by_category(category_id)
```

### Cache Tags for Group Invalidation

```python
from app.core.dependency_manager import get_service

cache_service = get_service("cache_service")

# Invalidate all product-related cache entries
async def clear_product_cache():
    # Get Redis backend
    redis_backend = cache_service._get_backend("redis")

    # Get all keys with product tag
    tag_key = "cache:tag:products"
    keys = await redis_backend.get_set_members(tag_key)

    # Delete all keys
    if keys:
        await cache_service.delete_many(keys)

        # Also remove the tag itself
        await redis_backend.delete(tag_key)

    return {"invalidated": len(keys)}
```

### Exception Handling

```python
from app.core.cache.exceptions import CacheException, CacheOperationException

async def get_cached_data(key: str):
    try:
        cache_service = get_service("cache_service")
        return await cache_service.get(key)
    except CacheOperationException as e:
        logger.warning(f"Cache operation failed: {e}")
        # Fallback to database
        return await fetch_from_database()
    except CacheException as e:
        logger.error(f"Cache system error: {e}")
        # More severe error, may need to be reported
        raise
```

### Integration with Metrics

The cache system automatically tracks metrics:

- `cache_hit_total` - Counter of cache hits
- `cache_miss_total` - Counter of cache misses
- `cache_operations_total` - Counter of all cache operations
- `cache_operation_duration_seconds` - Histogram of cache operation durations

These metrics can be used to monitor cache effectiveness:

- Hit rate: `sum(rate(cache_hit_total[5m])) / sum(rate(cache_operations_total[5m]))`
- Miss rate: `sum(rate(cache_miss_total[5m])) / sum(rate(cache_operations_total[5m]))`
- Operation latency: `histogram_quantile(0.95, sum(rate(cache_operation_duration_seconds_bucket[5m])) by (le))`

### System Integration

The cache system is designed to seamlessly integrate with other application systems:

#### Error Handling Integration

The cache system uses a dedicated exception hierarchy that integrates with the application's exception system:

```python
from app.core.cache.exceptions import CacheException, CacheOperationException

try:
    value = await cache_service.get("my_key")
except CacheOperationException as e:
    # Handle specific operation errors
    logger.warning(f"Cache operation failed: {e}")
    # Fallback logic
except CacheException as e:
    # Handle general cache errors
    logger.error(f"Cache error: {e}")
    # More severe error handling
```

When cache operations fail, the system will automatically log errors with appropriate context and fall back to database operations where possible, rather than causing application failures.

#### Metrics Integration

Cache operations are automatically tracked with the metrics system:

```python
# These metrics are available automatically
metrics_service = get_service("metrics_service")

# Get hit rate over the last 5 minutes
hit_rate = metrics_service.get_counter_rate("cache_hit_total") / \
           metrics_service.get_counter_rate("cache_operations_total")

# Get p95 latency for cache operations
latency = metrics_service.get_histogram_quantile(
    "cache_operation_duration_seconds",
    0.95,
    {"component": "product_service"}
)

# Get miss count by backend
miss_count = metrics_service.get_counter_sum(
    "cache_miss_total",
    {"backend": "redis"}
)
```

#### Dependency Injection

The cache service is automatically registered with the dependency manager:

```python
# In service classes
class ProductService:
    def __init__(self, db):
        self.db = db
        self.cache_service = get_service("cache_service")

    async def get_product(self, product_id):
        # Use cache service
        cache_key = f"product:{product_id}"
        product = await self.cache_service.get(cache_key)
        if product:
            return product

        # Cache miss - get from database
        product = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )
        product = product.scalar_one_or_none()

        # Cache for next time
        if product:
            await self.cache_service.set(cache_key, product, ttl=300)

        return product
```

### Configuration

The cache system can be configured in the settings:

```python
# In settings.py or .env

# Cache backend settings
CACHE_DEFAULT_BACKEND="redis"  # "redis", "memory", or "null"

# Redis connection settings
REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD="optional_password"
REDIS_URI="redis://localhost:6379/0"

# Default TTL settings (in seconds)
CACHE_DEFAULT_TTL=300  # 5 minutes
```

### Available Backends

The cache system provides multiple backends:

1. **Redis Backend**: Production-ready backend with all features, including pattern-based invalidation, atomic counters, and tag-based operations. Recommended for production.

2. **Memory Backend**: In-process memory cache. Fast but doesn't persist or share between processes. Good for development, testing, or as a fallback when Redis is unavailable.

3. **Null Backend**: A non-caching implementation that acts like a cache but doesn't store anything. Useful for testing or disabling caching without changing code.

The system automatically falls back to the memory backend if Redis is unavailable, ensuring resilience.

## 10. Event System

The event system provides a robust framework for implementing domain events and event-driven architecture patterns throughout the application. It supports both in-memory and distributed event processing.

### Key Features
- Support for both in-memory and distributed (Celery) event processing
- Typed domain events with dataclasses
- Automatic event handler registration
- Asynchronous event processing
- Exception handling and error reporting
- Integration with metrics system
- Contextual information in events

### Event Backends

The system supports two event backends:

1. **Memory Backend**: In-process event handling, ideal for development and testing. Simple to set up with no external dependencies.

2. **Celery Backend**: Distributed event processing using Celery tasks, suitable for production environments where reliability and scalability are required.

### Basic Usage

#### Initializing the Event System

```python
from app.core.dependency_manager import get_service
from app.core.events import EventBackendType

# In your application startup
async def startup():
    # Get event service through dependency injection
    event_service = get_service("event_service")

    # Initialize with desired backend
    await event_service.initialize(EventBackendType.MEMORY)  # or EventBackendType.CELERY
```

#### Publishing Events

```python
from app.core.dependency_manager import get_service

# Get event service
event_service = get_service("event_service")

# Publish a simple event
async def create_user(user_data):
    # Create user in database
    user = await user_repository.create(user_data)

    # Publish event
    await event_service.publish(
        event_name="user.created",
        payload={
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email
        },
        context={
            "user_id": user.id,
            "request_id": get_current_request_id()
        }
    )

    return user
```

#### Subscribing to Events

```python
from app.core.dependency_manager import get_service
from app.core.events import get_event_service

# Get event service
event_service = get_event_service()

# Using decorator to subscribe to events
@event_service.event_handler("user.created")
async def handle_new_user(event):
    # Extract data from event
    user_data = event["data"]
    user_id = user_data["user_id"]

    # Process the event
    logger.info(f"Processing new user creation", user_id=user_id)

    # Send welcome email
    await email_service.send_welcome_email(user_data["email"])
```

### Using Typed Domain Events

```python
from app.core.events.domain_events import DomainEvent, UserCreatedEvent, UserData
from app.core.dependency_manager import get_service

# Get event service
event_service = get_service("event_service")

# Creating and publishing a typed event
async def create_user(user_data):
    # Create user in database
    user = await user_repository.create(user_data)

    # Create typed event
    user_created = UserCreatedEvent.create(
        data={
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email
        },
        user_id=str(user.id),
        request_id=get_current_request_id()
    )

    # Convert to dict and publish
    await event_service.publish(
        event_name=user_created.event_name,
        payload=user_created.data,
        context=user_created.to_dict()
    )

    return user

# Using strongly typed events
@event_service.event_handler("user.created.typed")
async def handle_typed_user_event(event):
    # Convert dict back to typed event
    typed_event = UserCreatedEvent.from_dict(event)

    # Access typed data
    user_data = typed_event.data
    logger.info(f"Processing new user creation", user_id=user_data.user_id)

    # Send welcome email
    await email_service.send_welcome_email(user_data.email)
```

### Filtering Events

```python
from app.core.dependency_manager import get_service

# Get event service
event_service = get_service("event_service")

# Subscribe with filtering
@event_service.event_handler(
    "order.completed",
    filter_func=lambda event: event["data"]["total_amount"] > 1000
)
async def handle_large_orders(event):
    """This handler will only be called for large orders."""
    order_data = event["data"]
    logger.info(f"Processing large order", order_id=order_data["order_id"], amount=order_data["total_amount"])

    # Special processing for large orders
    await notification_service.notify_sales_team(order_data["order_id"])
```

### Creating Custom Domain Events

```python
from dataclasses import dataclass, field
from app.core.events.domain_events import DomainEvent
from typing import Dict, Any, ClassVar, Optional

# Define a custom event
@dataclass
class PaymentProcessedEvent(DomainEvent[Dict[str, Any]]):
    event_name: ClassVar[str] = "payment.processed"

# Define a typed data structure for an event
@dataclass
class PaymentData:
    payment_id: str
    order_id: str
    amount: float
    status: str
    processor: str

@dataclass
class PaymentProcessedTypedEvent(DomainEvent[PaymentData]):
    event_name: ClassVar[str] = "payment.processed.typed"
```

### Integration with Metrics

The event system automatically integrates with the metrics system to track performance:

```python
# These metrics are recorded automatically:
# - events_published_total (counter)
# - event_handler_errors_total (counter)
# - event_handler_duration_seconds (histogram)

# Example metrics queries for Prometheus:
# - rate(events_published_total[5m]) # Event publication rate
# - sum by (event_type) (event_handler_errors_total) # Error count by event type
# - histogram_quantile(0.95, sum(event_handler_duration_seconds_bucket) by (le, event_type)) # 95th percentile handler duration
```

### Error Handling

The event system integrates with the application's exception system:

```python
from app.core.events.exceptions import (
    EventPublishException,
    EventHandlerException,
    EventConfigurationException
)

# Publishing with error handling
async def publish_with_error_handling(event_data):
    try:
        await event_service.publish("order.created", event_data)
    except EventPublishException as e:
        # Handle publication error
        logger.error(f"Failed to publish order.created event: {str(e)}")
        # Report to error service
        await error_service.report_error(e, {"event_data": event_data})

# Error handling in event handlers is automatic:
# If an exception occurs in a handler, it will:
# 1. Log the error
# 2. Report it to the error service
# 3. Update metrics
# 4. Continue processing (won't break the application)
```

### Advanced Configuration

```python
from app.core.dependency_manager import get_service
from app.core.events import EventBackendType

# Get event service
event_service = get_service("event_service")

# Set default context for all events
event_service.set_default_context({
    "application": "my-app",
    "environment": settings.ENVIRONMENT,
    "version": "1.0.0"
})

# Custom initialization for Celery backend
async def initialize_with_celery():
    from app.core.celery_app import celery_app

    await event_service.initialize(
        backend_type=EventBackendType.CELERY
    )

    # Additional Celery-specific configuration can be done here
```

## 11. Permission System

The permission system provides a comprehensive framework for authorization, controlling access to resources and actions throughout the application. It supports role-based and permission-based access control with fine-grained control at both resource and object levels.

### Key Features
- Role-based permission mapping
- Permission enums for clear, consistent access control
- Object-level permission checking
- Permission decorators for endpoint security
- Integration with metrics, caching, and event systems
- Comprehensive logging of permission violations
- Support for both service-level and decorator-based authorization
- Permission caching for improved performance
- Declarative permission requirements

### Permission Models

```python
from app.core.permissions.models import Permission, UserRole, ROLE_PERMISSIONS

# Using predefined permissions
required_permission = Permission.USER_CREATE

# Check if a role has necessary permissions
admin_permissions = ROLE_PERMISSIONS[UserRole.ADMIN]
if Permission.USER_CREATE in admin_permissions:
    print("Admins can create users")

# Available permissions are defined as enums
print("Available permissions:")
for permission in Permission:
    print(f"- {permission.name}: {permission.value}")
```

### Basic Permission Checking

```python
from app.core.permissions.checker import PermissionChecker

# Simple permission check
def check_user_access(user, permission):
    if PermissionChecker.has_permission(user, permission):
        print(f"User has permission: {permission}")
        return True
    else:
        print(f"Permission denied: {permission}")
        return False

# Check multiple permissions with AND logic
def check_advanced_access(user, permissions):
    if PermissionChecker.has_permissions(user, permissions, require_all=True):
        print("User has all required permissions")
        return True
    else:
        print("User is missing one or more required permissions")
        return False

# Check multiple permissions with OR logic
def check_any_permission(user, permissions):
    if PermissionChecker.has_permissions(user, permissions, require_all=False):
        print("User has at least one of the required permissions")
        return True
    else:
        print("User has none of the required permissions")
        return False
```

### Object-Level Permissions

Object-level permissions allow checking if a user has permissions for a specific resource instance:

```python
from app.core.permissions.checker import PermissionChecker

# Check if user can access a specific product
def check_product_access(user, product, permission):
    if PermissionChecker.check_object_permission(user, product, permission, owner_field="created_by_id"):
        print(f"User can {permission.name} this product")
        return True
    else:
        print(f"User cannot {permission.name} this product")
        return False

# Enforce object permission with automatic exception
def enforce_product_access(user, product, permission):
    try:
        PermissionChecker.ensure_object_permission(user, product, permission, owner_field="created_by_id")
        print(f"Access granted: {permission}")
        return True
    except PermissionDeniedException as e:
        print(f"Access denied: {e}")
        # Re-raise or handle as needed
        raise
```

### Using Permission Decorators

Decorators provide a clean way to enforce permissions on API endpoints:

```python
from app.core.permissions.decorators import require_permission, require_permissions, require_admin
from app.core.permissions.models import Permission

# Simple permission requirement
@router.post("/products/")
@require_permission(Permission.PRODUCT_CREATE)
async def create_product(product_data: ProductCreate, current_user: User = Depends(get_current_user)):
    """
    Create a new product.
    Requires product:create permission.
    """
    return await product_service.create_product(product_data, current_user.id)

# Multiple permission requirements (ALL)
@router.put("/products/{product_id}")
@require_permissions([Permission.PRODUCT_UPDATE, Permission.PRODUCT_ADMIN], require_all=True)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update a product.
    Requires both product:update AND product:admin permissions.
    """
    return await product_service.update_product(product_id, product_data, current_user.id)

# Multiple permission requirements (ANY)
@router.get("/reports/")
@require_permissions([Permission.PRODUCT_ADMIN, Permission.SYSTEM_ADMIN], require_all=False)
async def view_reports(current_user: User = Depends(get_current_user)):
    """
    View system reports.
    Requires EITHER product:admin OR system:admin permission.
    """
    return await report_service.get_reports()

# Admin-only endpoint
@router.delete("/users/{user_id}")
@require_admin()
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete a user.
    Requires system:admin permission.
    """
    return await user_service.delete_user(user_id)
```

### Permission Service

For more complex permission scenarios or service-level authorization:

```python
from app.core.dependency_manager import get_service
from app.core.permissions import get_permission_service

# Get permission service through dependency injection
@router.get("/products/{product_id}/sensitive-data")
async def get_product_sensitive_data(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Get permission service
    permission_service = get_permission_service(db)

    # Get the product
    product = await product_repository.get_by_id(db, product_id)
    if not product:
        raise ResourceNotFoundException(resource_type="Product", resource_id=product_id)

    # Check object-level permission
    await permission_service.ensure_object_permission(
        current_user,
        product,
        Permission.PRODUCT_ADMIN,
        owner_field="created_by_id"
    )

    # If we get here, the user has permission
    return await product_service.get_sensitive_data(product_id)
```

### Permission in Service Classes

```python
from app.core.dependency_manager import get_service

class ProductService:
    def __init__(self, db):
        self.db = db
        self.permission_service = get_service("permission_service", db=db)

    async def update_product_price(self, product_id: str, new_price: float, user_id: str):
        # Get the user
        user = await get_user_by_id(self.db, user_id)

        # Get the product
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundException(resource_type="Product", resource_id=product_id)

        # Check permissions
        has_permission = await self.permission_service.check_object_permission(
            user,
            product,
            Permission.PRODUCT_UPDATE,
            owner_field="created_by_id"
        )

        if not has_permission:
            # For price changes > 20%, require admin permission
            price_change_pct = abs(new_price - product.price) / product.price * 100
            if price_change_pct > 20:
                await self.permission_service.ensure_permission(
                    user,
                    Permission.PRODUCT_ADMIN,
                    resource_type="Product",
                    resource_id=product_id
                )

        # Update the product
        product.price = new_price
        await self.repository.save(product)

        return product
```

### Retrieving User Permissions

```python
from app.core.dependency_manager import get_service

# Get all permissions for a user
async def get_user_permissions(user_id: str, db: AsyncSession):
    permission_service = get_permission_service(db)

    try:
        # Get all permissions for the user
        permissions = await permission_service.get_user_permissions(user_id)

        return {
            "user_id": user_id,
            "permissions": [p.value for p in permissions]
        }
    except Exception as e:
        logger.error(f"Error retrieving user permissions: {e}", user_id=user_id)
        handle_exception(e, user_id=user_id)
        raise
```

### Utility Functions

```python
from app.core.permissions.utils import has_any_permission, has_all_permissions, check_owner_permission

# Utility to check ownership
def is_owner(user_id: str, entity_user_id: str):
    return check_owner_permission(user_id, entity_user_id)

# Utility to check if user has any of the specified permissions
def can_perform_any(user, permissions: List[str]):
    return has_any_permission(user, permissions)

# Utility to check if user has all specified permissions
def can_perform_all(user, permissions: List[str]):
    return has_all_permissions(user, permissions)
```

### Cache Integration

The permission system integrates with the cache system for improved performance:

```python
# The permission service automatically caches permission checks
# Cache keys format:
# - permission:check:{user_id}:{permission}
# - permissions:user:{user_id}

# Invalidate cached permissions when user roles/permissions change
async def update_user_role(user_id: str, new_role: UserRole):
    # Update in database
    user = await user_repository.get_by_id(user_id)
    user.role = new_role
    await db.commit()

    # Invalidate permission cache
    permission_service = get_permission_service(db)
    await permission_service.invalidate_permissions_cache(user_id)

    return user
```

### Metrics Integration

The permission system automatically tracks metrics for monitoring:

```python
# These metrics are recorded automatically:
# - permission_check_duration_seconds (histogram)
# - permission_checks_total (counter)
# - multiple_permissions_check_duration_seconds (histogram)
# - multiple_permissions_checks_total (counter)
# - object_permission_check_duration_seconds (histogram)
# - object_permission_checks_total (counter)
# - get_user_permissions_duration_seconds (histogram)
# - user_permissions_cache_hits_total (counter)
# - permission_check_cache_hits_total (counter)

# Example metrics queries for Prometheus:
# - sum by (permission, granted) (rate(permission_checks_total[5m]))
# - histogram_quantile(0.95, sum by (le) (rate(permission_check_duration_seconds[5m])))
# - sum by (object_type) (rate(object_permission_checks_total[5m]))
```

### Events Integration

The permission system publishes events when permission checks fail:

```python
# The permission service automatically publishes these events:
# - permission.denied - When a general permission check fails
# - permission.object_denied - When an object permission check fails

# Example event handler for security monitoring
@event_service.event_handler("permission.denied")
async def log_permission_denied(event):
    data = event["data"]
    logger.warning(
        "Permission denied event",
        user_id=data["user_id"],
        permission=data["permission"],
        resource_type=data["resource_type"],
        resource_id=data["resource_id"],
        action=data["action"]
    )

    # Add to security audit log
    await security_audit_service.log_event(
        "PERMISSION_DENIED",
        user_id=data["user_id"],
        details=data
    )
```

## 12. Security System

The security system provides comprehensive security functionality for the application, including authentication, encryption, token management, API key handling, password management, CSRF protection, and input validation.

### Key Features
- JWT-based authentication with access and refresh tokens
- Token blacklisting for secure logout
- API key generation and validation
- Password hashing, validation, and policy enforcement
- Data encryption and decryption
- CSRF token protection
- Input validation and sanitization
- Security headers generation
- Metrics tracking for security operations
- Integration with event system for security auditing
- FastAPI dependency functions for authentication

### Token Management

```python
from app.core.security import create_token, create_token_pair, TokenType, TokenPair

# Create a simple token
access_token = create_token(
    subject="user-123",  # User ID
    token_type=TokenType.ACCESS,
    role="admin",
    permissions=["user:read", "user:write"]
)

# Create a token pair (access + refresh tokens)
token_pair: TokenPair = create_token_pair(
    user_id="user-123",
    role="admin",
    permissions=["user:read", "user:write"],
    user_data={"name": "John Doe", "email": "john@example.com"}
)

print(f"Access token: {token_pair.access_token}")
print(f"Refresh token: {token_pair.refresh_token}")
print(f"Expires in: {token_pair.expires_in} seconds")
```

### Token Validation and Refresh

```python
from app.core.security import decode_token, refresh_tokens, revoke_token

# Validate a token
async def validate_user_token(token: str):
    try:
        # Decode and validate the token
        token_data = await decode_token(token)

        # Token is valid, return user information
        return {
            "user_id": token_data.sub,
            "role": token_data.role,
            "permissions": token_data.permissions,
            "expires_at": token_data.exp.isoformat()
        }
    except AuthenticationException as e:
        logger.warning(f"Token validation failed: {str(e)}")
        raise

# Refresh tokens
async def refresh_user_tokens(refresh_token: str):
    try:
        # Refresh tokens (will validate and blacklist the old refresh token)
        new_tokens = await refresh_tokens(refresh_token)
        return new_tokens
    except AuthenticationException as e:
        logger.warning(f"Token refresh failed: {str(e)}")
        raise

# Logout (revoke token)
async def logout_user(token: str, user_id: str):
    try:
        # Revoke the token (add to blacklist)
        await revoke_token(token)
        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout failed: {str(e)}")
        handle_exception(e, user_id=user_id)
        raise
```

### Using the Security Service

```python
from app.core.dependency_manager import get_service
from app.core.security import get_security_service

# Get security service through dependency injection
@router.post("/auth/login")
async def login(
    login_data: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    # Get security service
    security_service = get_security_service(db)

    # Validate credentials
    user = await user_repository.get_by_email(login_data.email)
    if not user:
        raise AuthenticationException(message="Invalid credentials")

    # Verify password
    is_valid = await security_service.verify_password(
        login_data.password,
        user.hashed_password,
        user_id=str(user.id)
    )

    if not is_valid:
        raise AuthenticationException(message="Invalid credentials")

    # Create tokens
    token_pair = await security_service.create_token_pair(
        user_id=str(user.id),
        role=user.role,
        permissions=[p.value for p in user.permissions],
        user_data={"name": user.name, "email": user.email}
    )

    # Set CSRF token (for cookie-based auth)
    csrf_token = security_service.generate_csrf_token(str(user.id))
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,  # Accessible by JavaScript
        secure=True,
        samesite="strict"
    )

    return token_pair
```

### Password Management

```python
from app.core.security import get_password_hash, verify_password, validate_password_policy

# Hash a password
def hash_user_password(plain_password: str):
    hashed = get_password_hash(plain_password)
    return hashed

# Verify a password
def check_user_password(plain_password: str, hashed_password: str):
    return verify_password(plain_password, hashed_password)

# Validate password against security policy
async def validate_new_password(password: str, user_id: Optional[str] = None):
    is_valid, message = await validate_password_policy(password, user_id)

    if not is_valid:
        raise ValidationException(
            message="Password policy validation failed",
            errors=[{
                "loc": ["password"],
                "msg": message,
                "type": "password_policy_error"
            }]
        )

    return True
```

### API Key Management

```python
from app.core.security import generate_api_key, verify_api_key

# Generate an API key for a user
def create_user_api_key(user_id: str, name: str, permissions: List[str]):
    api_key_data = generate_api_key(user_id, name, permissions)

    # Store the hashed key in database (never store the actual key)
    db_api_key = ApiKey(
        id=api_key_data.key_id,
        user_id=user_id,
        name=name,
        hashed_secret=api_key_data.hashed_secret,
        permissions=permissions,
        created_at=datetime.datetime.now(datetime.UTC)
    )
    db.add(db_api_key)
    await db.commit()

    # Return the API key to the user (this is the only time they'll see it)
    return {
        "api_key": api_key_data.api_key,
        "name": name,
        "permissions": permissions,
        "created_at": db_api_key.created_at.isoformat()
    }

# Verify an API key
async def verify_user_api_key(api_key: str):
    # Extract key ID from the API key
    parts = api_key.split(".")
    if len(parts) != 2:
        raise AuthenticationException(message="Invalid API key format")

    key_id, _ = parts

    # Find the stored key data
    stored_key = await db.execute(select(ApiKey).where(ApiKey.id == key_id))
    stored_key = stored_key.scalar_one_or_none()

    if not stored_key:
        raise AuthenticationException(message="Invalid API key")

    # Verify the key
    if not verify_api_key(api_key, stored_key.hashed_secret):
        raise AuthenticationException(message="Invalid API key")

    # At this point, the API key is valid
    return {
        "user_id": stored_key.user_id,
        "key_id": stored_key.id,
        "name": stored_key.name,
        "permissions": stored_key.permissions
    }
```

### CSRF Protection

```python
from app.core.security import generate_csrf_token, validate_csrf_token

# Generate a CSRF token
def get_csrf_token(session_id: str):
    return generate_csrf_token(session_id)

# Validate a CSRF token
def check_csrf_token(token: str, session_id: str):
    is_valid = validate_csrf_token(token, session_id)

    if not is_valid:
        raise SecurityException(
            message="CSRF validation failed",
            code=ErrorCode.SECURITY_ERROR,
            details={"error": "Invalid or expired CSRF token"}
        )

    return True

# Example of CSRF protection in a FastAPI endpoint
@router.post("/users/{user_id}/settings")
async def update_user_settings(
    user_id: str,
    settings_data: Dict[str, Any],
    csrf_token: str = Header(...),
    current_user_id: str = Depends(get_current_user_id)
):
    # Verify user identity
    if user_id != current_user_id:
        raise PermissionDeniedException(message="Cannot modify another user's settings")

    # Validate CSRF token
    security_service = get_security_service()
    if not security_service.validate_csrf_token(csrf_token, current_user_id):
        raise SecurityException(message="Invalid CSRF token")

    # Process the request
    # ...

    return {"success": True}
```

### Encryption

```python
from app.core.security import encrypt_data, decrypt_data

# Encrypt sensitive data
def store_secure_data(user_id: str, sensitive_data: dict):
    try:
        # Encrypt the data
        encrypted = encrypt_data(sensitive_data)

        # Store in database
        secure_record = UserSecureData(
            user_id=user_id,
            encrypted_data=encrypted
        )
        db.add(secure_record)
        await db.commit()

        return {"id": secure_record.id, "success": True}
    except Exception as e:
        logger.error(f"Encryption error: {str(e)}")
        handle_exception(e, user_id=user_id)
        raise

# Decrypt sensitive data
def retrieve_secure_data(user_id: str, record_id: str):
    try:
        # Get from database
        record = await db.execute(
            select(UserSecureData)
            .where(UserSecureData.id == record_id)
            .where(UserSecureData.user_id == user_id)
        )
        record = record.scalar_one_or_none()

        if not record:
            raise ResourceNotFoundException(
                resource_type="UserSecureData",
                resource_id=record_id
            )

        # Decrypt the data
        decrypted = decrypt_data(record.encrypted_data)

        return decrypted
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        handle_exception(e, user_id=user_id)
        raise
```

### Input Validation and Sanitization

```python
from app.core.security.validation import (
    sanitize_input,
    detect_suspicious_content,
    validate_json_input,
    is_valid_hostname,
    is_trusted_ip,
    moderate_content
)

# Sanitize user input
def clean_user_input(input_text: str):
    return sanitize_input(input_text)

# Detect potentially malicious content
def check_user_content(content: str):
    if detect_suspicious_content(content):
        logger.warning("Suspicious content detected", content_length=len(content))
        raise SecurityException(
            message="Potentially malicious content detected",
            code=ErrorCode.SECURITY_ERROR
        )
    return content

# Validate JSON input
def validate_client_json(json_data: Any):
    if not validate_json_input(json_data):
        raise ValidationException(
            message="Invalid JSON data",
            errors=[{
                "loc": ["body"],
                "msg": "Invalid or malicious JSON data",
                "type": "json_validation_error"
            }]
        )
    return json_data

# Content moderation
async def moderate_user_content(content: str, content_type: str = "text"):
    is_allowed, reason = moderate_content(content, content_type)

    if not is_allowed:
        raise ValidationException(
            message="Content moderation failed",
            errors=[{
                "loc": ["content"],
                "msg": reason or "Content violates community guidelines",
                "type": "content_moderation_error"
            }]
        )

    return content
```

### Security Headers

```python
from app.core.security import get_security_headers

# Middleware to add security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    # Get security headers
    security_service = get_security_service()
    security_headers = security_service.get_security_headers()

    # Add headers to response
    for name, value in security_headers.items():
        response.headers[name] = value

    return response
```

### FastAPI Authentication Dependencies

```python
from app.core.security.dependencies import (
    get_current_user_id,
    get_optional_user_id,
    get_current_user_with_permissions
)

# Endpoint requiring authentication
@router.get("/users/me")
async def get_current_user_profile(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    # Get user by ID
    user = await user_repository.get_by_id(current_user_id)

    if not user:
        raise ResourceNotFoundException(resource_type="User", resource_id=current_user_id)

    return user.to_response()

# Endpoint with optional authentication
@router.get("/products/{product_id}")
async def get_product(
    product_id: str,
    user_id: Optional[str] = Depends(get_optional_user_id),
    db: AsyncSession = Depends(get_db)
):
    # Get product
    product = await product_repository.get_by_id(product_id)

    if not product:
        raise ResourceNotFoundException(resource_type="Product", resource_id=product_id)

    # If user is authenticated, record view
    if user_id:
        await product_view_service.record_view(product_id, user_id)

    return product.to_response()

# Endpoint requiring authentication with permissions
@router.post("/products")
async def create_product(
    product_data: ProductCreate,
    user_data: dict = Depends(get_current_user_with_permissions),
    db: AsyncSession = Depends(get_db)
):
    # Check permission
    if "product:create" not in user_data["permissions"]:
        raise PermissionDeniedException(
            message="You don't have permission to create products",
            action="create",
            resource_type="product",
            permission="product:create"
        )

    # Create product
    product = await product_repository.create(product_data, user_data["id"])

    return product.to_response()
```

### Metrics and Events Integration

```python
# The security service automatically tracks these metrics:
# - token_validation_duration_seconds (histogram)
# - token_validations_total (counter)
# - tokens_created_total (counter)
# - token_creation_duration_seconds (histogram)
# - password_verification_duration_seconds (histogram)
# - password_verifications_total (counter)
# - api_keys_created_total (counter)
# - api_key_verification_duration_seconds (histogram)
# - csrf_validations_total (counter)
# - suspicious_content_detections_total (counter)

# The security service publishes these events:
# - security.token_created - When a token is created
# - security.token_revoked - When a token is revoked
# - security.api_key_created - When an API key is created
# - security.password_verification_failed - When a password verification fails

# Example event handler for monitoring
@event_service.event_handler("security.token_revoked")
async def log_token_revocation(event):
    data = event["data"]
    logger.info(
        "Token revoked",
        user_id=data["user_id"],
        reason=data["reason"]
    )
```

## 13. Middleware System

The middleware system provides a framework for processing HTTP requests and responses throughout their lifecycle. Middleware components handle cross-cutting concerns like logging, security, and performance monitoring.

### Key Features
- Request context and tracking
- Request/response logging
- Security protections and headers
- Performance monitoring and metrics
- Rate limiting and timeout enforcement
- Response formatting and compression
- Error handling and standardization
- Distributed tracing
- Cache control

### Available Middleware

#### RequestContextMiddleware
Sets up the request context with a unique ID and user ID for tracking requests throughout the system.

```python
from app.middleware import RequestContextMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(RequestContextMiddleware)
```

#### TracingMiddleware
Implements distributed tracing for tracking requests across multiple services and components.

```python
from app.middleware import TracingMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(TracingMiddleware, service_name="api-service")
```

#### MetricsMiddleware
Collects request metrics like counts, durations, and status codes for performance monitoring.

```python
from app.middleware import MetricsMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(MetricsMiddleware, ignore_paths=["/metrics", "/health"])
```

#### SecurityMiddleware
Adds security headers and blocks suspicious requests to protect against common attacks.

```python
from app.middleware import SecurityHeadersMiddleware, SecureRequestMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(SecurityHeadersMiddleware, content_security_policy="default-src 'self'")
app.add_middleware(SecureRequestMiddleware, block_suspicious_requests=True)
```

#### RateLimitMiddleware
Controls request rates to prevent abuse and ensure fair resource usage.

```python
from app.middleware import RateLimitMiddleware
from app.core.rate_limiting import RateLimitRule, RateLimitStrategy
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(
    RateLimitMiddleware,
    rules=[
        RateLimitRule(
            requests_per_window=100,
            window_seconds=60,
            strategy=RateLimitStrategy.IP
        )
    ],
    use_redis=True
)
```

#### TimeoutMiddleware
Enforces request timeouts to prevent long-running requests from consuming resources.

```python
from app.middleware import TimeoutMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(TimeoutMiddleware, timeout_seconds=30.0)
```

#### CacheControlMiddleware
Adds appropriate cache control headers to responses based on request path and method.

```python
from app.middleware import CacheControlMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(CacheControlMiddleware)
```

#### ResponseFormatterMiddleware
Standardizes API responses to ensure consistent format with success flag, data, and metadata.

```python
from app.middleware import ResponseFormatterMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(ResponseFormatterMiddleware)
```

#### CompressionMiddleware
Compresses response data to reduce bandwidth and improve performance.

```python
from app.middleware import CompressionMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(CompressionMiddleware, minimum_size=1000)
```

#### ErrorHandlerMiddleware
Catches exceptions and provides standardized error responses.

```python
from app.middleware import ErrorHandlerMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(ErrorHandlerMiddleware)
```

### Middleware Ordering

Middleware order is critical as it affects request processing flow. The recommended order is:

1. **RequestContextMiddleware** - First to establish request context
2. **TracingMiddleware** - Early for accurate tracing
3. **MetricsMiddleware** - Early to measure full request lifecycle
4. **SecurityMiddleware** - Block malicious requests early
5. **RateLimitMiddleware** - Control request rates early
6. **TimeoutMiddleware** - Enforce timeouts before heavy processing
7. **CORSMiddleware** - Handle cross-origin requests
8. **SecurityHeadersMiddleware** - Add security headers
9. **CacheControlMiddleware** - Add cache control headers
10. **ResponseFormatterMiddleware** - Format responses
11. **CompressionMiddleware** - Compress response data
12. **ErrorHandlerMiddleware** - Last to catch all exceptions

### Creating Custom Middleware

Custom middleware can be created by extending the BaseHTTPMiddleware class:

```python
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Any

from app.logging import get_logger

logger = get_logger("app.middleware.custom")

class CustomMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any, option1: str = "default") -> None:
        super().__init__(app)
        self.option1 = option1
        logger.info("CustomMiddleware initialized", option1=option1)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        # Pre-processing logic
        logger.info("Processing request in custom middleware")

        try:
            # Call the next middleware or route handler
            response = await call_next(request)

            # Post-processing logic
            logger.info("Request processed successfully")

            return response
        except Exception as e:
            # Error handling logic
            logger.error(f"Error in custom middleware: {str(e)}")
            raise
```

### Middleware Best Practices

1. **Order Matters**: Be mindful of middleware execution order
2. **Performance Impact**: Keep middleware lightweight and efficient
3. **Error Handling**: Always handle exceptions properly
4. **Metrics**: Include performance metrics for observability
5. **Context Preservation**: Don't lose request context between middleware
6. **Exclusion Paths**: Provide ways to exclude certain paths from processing
7. **Graceful Degradation**: Middleware should degrade gracefully if dependencies fail
8. **Configuration**: Support external configuration through settings
9. **Minimal Work**: Do only what's necessary and delegate complex logic to services
10. **Documentation**: Document middleware purpose, options, and behavior clearly

### Integration with Other Systems

Middleware components often interact with other application systems:

#### Logging System Integration

```python
from app.logging import get_logger, request_context
from fastapi import Request

# In your middleware
logger = get_logger("app.middleware.example")

async def dispatch(self, request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    with request_context(request_id=request_id):
        logger.info("Processing request", path=request.url.path)
        # Process request
        return await call_next(request)
```

#### Metrics System Integration

```python
from app.core.dependency_manager import get_service

# In your middleware
metrics_service = get_service("metrics_service")
metrics_service.increment_counter(
    "requests_total",
    1,
    {"path": request.url.path}
)
```

#### Error System Integration

```python
from app.core.error import handle_exception

# In your middleware
try:
    # Process request
    return await call_next(request)
except Exception as e:
    request_id = getattr(request.state, "request_id", None)
    handle_exception(e, request_id=request_id)
    raise
```

#### Cache System Integration

```python
from app.core.dependency_manager import get_service

# In your middleware
cache_service = get_service("cache_service")
cached_response = await cache_service.get(f"response:{request.url.path}")
if cached_response:
    return cached_response
```

### Common Middleware Patterns

#### Request/Response Timing

```python
async def dispatch(self, request: Request, call_next):
    start_time = time.monotonic()

    response = await call_next(request)

    # Calculate duration
    duration = time.monotonic() - start_time
    response.headers["X-Response-Time"] = f"{duration:.4f}s"

    return response
```

#### Authentication Check

```python
async def dispatch(self, request: Request, call_next):
    # Extract token
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        # Validate token
        # Set user in request state
        request.state.user_id = user_id

    return await call_next(request)
```

#### Response Modification

```python
async def dispatch(self, request: Request, call_next):
    response = await call_next(request)

    # Modify response headers
    response.headers["X-Custom-Header"] = "value"

    # Modify response body (for JSON responses)
    if isinstance(response, JSONResponse):
        content = response.body
        modified_content = json.loads(content)
        modified_content["extra_field"] = "value"

        return JSONResponse(
            content=modified_content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )

    return response
```

#### Conditional Processing

```python
async def dispatch(self, request: Request, call_next):
    # Skip processing for certain paths
    if any(request.url.path.startswith(prefix) for prefix in self.exclude_paths):
        return await call_next(request)

    # Skip processing for certain methods
    if request.method in ["OPTIONS", "HEAD"]:
        return await call_next(request)

    # Normal processing
    # ...

    return await call_next(request)
```

## 14. Common Patterns and Best Practices

This section provides examples of common patterns and best practices for using the various systems together effectively.

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
                "Validation failed",
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

### Caching with Fallback and Metrics

This pattern demonstrates how to implement robust caching with proper fallback mechanisms, metrics tracking, and integration with the error handling system:

```python
from app.core.dependency_manager import get_service
from app.core.cache.exceptions import CacheOperationException
from app.logging import get_logger
from app.core.error import handle_exception
import time

logger = get_logger("app.services.product_service")

class ProductService:
    def __init__(self, db):
        self.db = db
        self.cache_service = get_service("cache_service")
        self.metrics_service = get_service("metrics_service")

    async def get_product_with_details(self, product_id: str):
        """Get product with complete details, using caching with proper fallback.

        This method demonstrates caching with:
        1. Proper key generation
        2. Error handling with fallback
        3. Metrics tracking
        4. Cache invalidation on updates
        """
        logger.info("Fetching product with details", product_id=product_id)

        # Define cache key
        cache_key = f"product:details:{product_id}"

        # Start metrics timer
        start_time = time.monotonic()
        cache_hit = False

        try:
            # Try to get from cache first
            cached_data = await self.cache_service.get(cache_key)

            if cached_data is not None:
                logger.debug("Cache hit for product details", product_id=product_id)
                cache_hit = True
                return cached_data

            logger.debug("Cache miss for product details", product_id=product_id)

            # Get from database
            product = await self.db.execute(
                select(Product).where(Product.id == product_id)
            )
            product = product.scalar_one_or_none()

            if not product:
                logger.warning("Product not found", product_id=product_id)
                return None

            # Get additional data
            reviews = await self.db.execute(
                select(Review).where(Review.product_id == product_id)
            )
            reviews = list(reviews.scalars().all())

            inventory = await self.inventory_repository.get_levels(product_id)
            related_products = await self.get_related_products(product_id)

            # Combine into a complete response
            result = {
                "product": product.to_dict(),
                "reviews": [r.to_dict() for r in reviews],
                "inventory": inventory,
                "related_products": related_products,
                "calculated_rating": self._calculate_rating(reviews)
            }

            # Cache the result (15 minutes TTL)
            try:
                await self.cache_service.set(
                    cache_key,
                    result,
                    ttl=900,
                    tags=["products", f"product:{product_id}"]
                )
            except CacheOperationException as cache_err:
                # Log but don't fail if caching fails
                logger.warning(
                    "Failed to cache product details",
                    product_id=product_id,
                    error=str(cache_err)
                )

            return result

        except Exception as e:
            # Handle and report the exception
            handle_exception(e, product_id=product_id)
            logger.error(
                "Error fetching product details",
                product_id=product_id,
                error=str(e)
            )
            raise

        finally:
            # Record metrics regardless of success/failure
            duration = time.monotonic() - start_time
            self.metrics_service.observe_histogram(
                "product_details_duration_seconds",
                duration,
                {
                    "cache_hit": str(cache_hit),
                    "product_id": product_id[:5]  # First 5 chars for cardinality
                }
            )

    async def update_product(self, product_id: str, data: dict, user_id: str):
        """Update product data and invalidate related caches."""
        logger.info("Updating product", product_id=product_id, user_id=user_id)

        try:
            # Update in database
            product = await self.repository.update(product_id, data, user_id)

            # Invalidate caches
            try:
                # Invalidate specific product cache
                await self.cache_service.delete(f"product:details:{product_id}")

                # Invalidate any list caches that might contain this product
                await self.cache_service.invalidate_pattern(f"products:list:*")

                # If using Redis with tags
                redis_backend = self.cache_service._get_backend("redis")
                if hasattr(redis_backend, "get_set_members"):
                    # Invalidate all caches tagged with this product
                    tag_key = f"cache:tag:product:{product_id}"
                    tagged_keys = await redis_backend.get_set_members(tag_key)
                    if tagged_keys:
                        await self.cache_service.delete_many(tagged_keys)
                        await redis_backend.delete(tag_key)

            except Exception as cache_err:
                # Log but continue if cache invalidation fails
                logger.warning(
                    "Failed to invalidate cache for product update",
                    product_id=product_id,
                    error=str(cache_err)
                )

            # Audit log the update
            audit_service = get_service("audit_service")
            await audit_service.log_action(
                user_id=user_id,
                action="product_update",
                resource_id=product_id,
                details={"fields_updated": list(data.keys())}
            )

            return product

        except Exception as e:
            handle_exception(e, product_id=product_id, user_id=user_id)
            raise
```

This pattern demonstrates several important practices:

1. **Proper cache key generation** - Using consistent, structured cache keys
2. **Error handling with fallback** - Gracefully handling cache failures without affecting core functionality
3. **Cache invalidation strategy** - Both targeted invalidation and pattern-based invalidation
4. **Metrics tracking** - Recording performance metrics for both cache hits and misses
5. **Integration with other systems** - Working with logging, metrics, and error handling
6. **Tag-based invalidation** - Using Redis tags for grouped invalidation
7. **Audit logging** - Recording significant data changes

### Event-Driven Architecture Patterns

#### Event-Based Workflow

This pattern demonstrates using events to create a decoupled workflow:

```python
# In OrderService
async def place_order(self, order_data, user_id):
    """Create an order and publish events for subsequent processing."""
    self.logger.info("Creating order", user_id=user_id, items_count=len(order_data["items"]))

    # Create order in database
    order = Order(
        user_id=user_id,
        items=order_data["items"],
        status="pending",
        total_amount=calculate_total(order_data["items"])
    )
    self.db.add(order)
    await self.db.commit()
    await self.db.refresh(order)

    # Publish order created event
    event_service = get_service("event_service")
    await event_service.publish(
        event_name="order.created",
        payload={
            "order_id": str(order.id),
            "user_id": user_id,
            "items": order_data["items"],
            "total_amount": order.total_amount
        }
    )

    self.logger.info("Order created successfully", order_id=str(order.id))
    return order

# In InventoryService as an event handler
@event_service.event_handler("order.created")
async def reserve_inventory(event):
    """Reserve inventory items when an order is created."""
    order_data = event["data"]
    logger.info("Reserving inventory for order", order_id=order_data["order_id"])

    # Reserve inventory
    for item in order_data["items"]:
        await inventory_repository.reserve(
            product_id=item["product_id"],
            quantity=item["quantity"],
            order_id=order_data["order_id"]
        )

    # Publish inventory reserved event
    await event_service.publish(
        event_name="inventory.reserved",
        payload={
            "order_id": order_data["order_id"],
            "user_id": order_data["user_id"],
            "items": order_data["items"]
        }
    )

    logger.info("Inventory reserved for order", order_id=order_data["order_id"])

# In PaymentService as an event handler
@event_service.event_handler("inventory.reserved")
async def process_payment(event):
    """Process payment after inventory is reserved."""
    order_data = event["data"]
    logger.info("Processing payment for order", order_id=order_data["order_id"])

    # Get payment details from user profile
    user = await user_repository.get_by_id(order_data["user_id"])

    # Process payment
    payment_result = await payment_gateway.process_payment(
        amount=order_data["total_amount"],
        payment_method=user.default_payment_method,
        order_id=order_data["order_id"]
    )

    if payment_result.success:
        # Publish payment succeeded event
        await event_service.publish(
            event_name="payment.succeeded",
            payload={
                "order_id": order_data["order_id"],
                "payment_id": payment_result.payment_id,
                "amount": order_data["total_amount"]
            }
        )
        logger.info("Payment succeeded for order", order_id=order_data["order_id"])
    else:
        # Publish payment failed event
        await event_service.publish(
            event_name="payment.failed",
            payload={
                "order_id": order_data["order_id"],
                "error": payment_result.error,
                "reason": payment_result.error_message
            }
        )
        logger.error("Payment failed for order", order_id=order_data["order_id"], error=payment_result.error)

# In OrderService as event handlers for payment outcomes
@event_service.event_handler("payment.succeeded")
async def finalize_order(event):
    """Finalize the order after successful payment."""
    payment_data = event["data"]
    logger.info("Finalizing order after payment", order_id=payment_data["order_id"])

    # Update order status
    order = await order_repository.get_by_id(payment_data["order_id"])
    order.status = "completed"
    order.payment_id = payment_data["payment_id"]
    await db.commit()

    # Publish order completed event
    await event_service.publish(
        event_name="order.completed",
        payload={
            "order_id": payment_data["order_id"],
            "user_id": order.user_id,
            "total_amount": payment_data["amount"],
            "status": "completed"
        }
    )

    logger.info("Order finalized successfully", order_id=payment_data["order_id"])

@event_service.event_handler("payment.failed")
async def handle_payment_failure(event):
    """Handle payment failure by updating order and releasing inventory."""
    payment_data = event["data"]
    logger.info("Handling payment failure", order_id=payment_data["order_id"])

    # Update order status
    order = await order_repository.get_by_id(payment_data["order_id"])
    order.status = "payment_failed"
    order.failure_reason = payment_data["reason"]
    await db.commit()

    # Publish event to release inventory
    await event_service.publish(
        event_name="inventory.release_requested",
        payload={
            "order_id": payment_data["order_id"],
            "reason": "payment_failed"
        }
    )

    logger.info("Order marked as payment failed", order_id=payment_data["order_id"])
```

This event-driven workflow demonstrates several benefits:
1. **Decoupling** - Each service focuses on its own responsibility
2. **Scalability** - Services can scale independently
3. **Resilience** - If one part fails, other parts can continue or retry
4. **Traceability** - The entire workflow is trackable through events
5. **Extensibility** - New steps can be added by subscribing to existing events

### Combining Authentication, Permissions and Business Logic

This pattern demonstrates how to effectively combine authentication, permissions, and business logic in a service method:

```python
class DocumentService:
    def __init__(self, db):
        self.db = db
        self.logger = get_logger("app.domains.documents.service")
        self.security_service = get_service("security_service", db=db)
        self.permission_service = get_service("permission_service", db=db)
        self.validation_service = get_service("validation_service", db=db)
        self.cache_service = get_service("cache_service")
        self.metrics_service = get_service("metrics_service")

    async def share_document(self, document_id: str, share_data: Dict[str, Any], user_id: str):
        """Share a document with another user or group.

        This method demonstrates combining:
        1. Authentication validation
        2. Object-level permission checks
        3. Business logic validation
        4. Metrics tracking
        5. Auditing
        6. Cache invalidation
        """
        start_time = time.monotonic()
        success = False

        try:
            self.logger.info("Document share requested", document_id=document_id, user_id=user_id)

            # Get current user
            user = await get_user_by_id(self.db, user_id)

            # Get the document
            document = await self.repository.get_by_id(document_id)
            if not document:
                raise ResourceNotFoundException(resource_type="Document", resource_id=document_id)

            # Check document permission (requires either document:admin or document:share)
            await self.permission_service.ensure_object_permission(
                user,
                document,
                Permission.DOCUMENT_SHARE,
                owner_field="owner_id"
            )

            # Validate share data
            validated_data = self.validation_service.validate_data(share_data, DocumentShareSchema)

            # Business logic validations
            if validated_data.recipient_id == user_id:
                raise BusinessException(
                    message="Cannot share a document with yourself",
                    details={"document_id": document_id}
                )

            # Check if recipient exists
            recipient = await get_user_by_id(self.db, validated_data.recipient_id)

            # Check if already shared
            existing_share = await self.repository.get_share(document_id, validated_data.recipient_id)
            if existing_share:
                # Update existing share
                existing_share.permissions = validated_data.permissions
                existing_share.updated_at = datetime.datetime.now(datetime.UTC)
                existing_share.updated_by = user_id
            else:
                # Create new share
                share = DocumentShare(
                    document_id=document_id,
                    recipient_id=validated_data.recipient_id,
                    permissions=validated_data.permissions,
                    created_by=user_id,
                    created_at=datetime.datetime.now(datetime.UTC)
                )
                self.db.add(share)

            await self.db.commit()

            # Invalidate caches
            await self.cache_service.delete(f"document:access:{document_id}:{validated_data.recipient_id}")
            await self.cache_service.delete(f"user:documents:{validated_data.recipient_id}")

            # Audit logging
            audit_service = get_service("audit_service")
            await audit_service.log_action(
                user_id=user_id,
                action="document_share",
                resource_type="Document",
                resource_id=document_id,
                target_id=validated_data.recipient_id,
                details={"permissions": validated_data.permissions}
            )

            # Publish event
            event_service = get_service("event_service")
            await event_service.publish(
                event_name="document.shared",
                payload={
                    "document_id": document_id,
                    "shared_by": user_id,
                    "shared_with": validated_data.recipient_id,
                    "permissions": validated_data.permissions,
                    "document_name": document.name
                }
            )

            success = True
            self.logger.info(
                "Document shared successfully",
                document_id=document_id,
                user_id=user_id,
                recipient_id=validated_data.recipient_id
            )

            return {
                "document_id": document_id,
                "recipient_id": validated_data.recipient_id,
                "permissions": validated_data.permissions,
                "success": True
            }

        except Exception as e:
            handle_exception(
                e,
                document_id=document_id,
                user_id=user_id,
                recipient_id=share_data.get("recipient_id")
            )
            raise

        finally:
            # Record metrics
            duration = time.monotonic() - start_time
            self.metrics_service.observe_histogram(
                "document_share_duration_seconds",
                duration,
                {
                    "success": str(success),
                    "document_type": getattr(document, "type", "unknown")
                }
            )
            self.metrics_service.increment_counter(
                "document_shares_total",
                labels={
                    "success": str(success),
                    "document_type": getattr(document, "type", "unknown")
                }
            )
```

This example demonstrates how to effectively layer multiple concerns in a service method:

1. **Authentication** - Verifying the current user
2. **Permission checking** - Using the permission service for object-level checks
3. **Data validation** - Validating input data with schemas
4. **Business logic validation** - Checking additional business rules
5. **Database operations** - Performing the core functionality
6. **Cache invalidation** - Clearing affected caches
7. **Auditing** - Logging important actions for accountability
8. **Event publishing** - Notifying other parts of the system about the change
9. **Metrics tracking** - Recording performance and business metrics
10. **Structured logging** - Providing context at each step
11. **Error handling** - Proper exception handling and reporting

### Securing API Endpoints with Multiple Layers

This pattern demonstrates securing API endpoints with multiple layers of protection:

```python
from fastapi import Depends, Request, APIRouter
from app.core.security.dependencies import get_current_user_id
from app.core.permissions.decorators import require_permission
from app.core.security.validation import detect_suspicious_content
from app.core.exceptions import SecurityException, ErrorCode

router = APIRouter()

# Define multiple security layers
async def validate_content(request: Request):
    """Middleware to check for malicious content."""
    body = await request.json()
    content = json.dumps(body)

    if detect_suspicious_content(content):
        raise SecurityException(
            message="Potentially malicious content detected",
            code=ErrorCode.SECURITY_ERROR
        )
    return body

@router.post("/documents")
@require_permission(Permission.DOCUMENT_CREATE)  # Permission check
async def create_document(
    request: Request,
    body: Dict[str, Any] = Depends(validate_content),  # Content validation
    current_user_id: str = Depends(get_current_user_id),  # Authentication
    db: AsyncSession = Depends(get_db)
):
    """Create a new document.

    This endpoint is protected by:
    1. Authentication (get_current_user_id)
    2. Permission check (require_permission)
    3. Content validation (validate_content)
    4. Rate limiting (RateLimitMiddleware)
    5. CSRF protection (from security middleware)
    """
    security_service = get_security_service()

    # Get CSRF token from header
    csrf_token = request.headers.get("X-CSRF-Token")
    if not csrf_token or not security_service.validate_csrf_token(csrf_token, current_user_id):
        raise SecurityException(message="Invalid CSRF token")

    # Create document
    document_service = get_service("document_service", db=db)
    document = await document_service.create_document(body, current_user_id)

    return document
```

This endpoint is protected by multiple security layers:

1. **Authentication** - Verifying the user's identity with tokens
2. **Authorization** - Checking permission requirements
3. **Content validation** - Detecting potentially malicious payloads
4. **CSRF protection** - Preventing cross-site request forgery attacks
5. **Rate limiting** - Protecting against abuse (applied via middleware)

### Feature Flags and Progressive Rollouts

This pattern demonstrates how to implement feature flags for controlled feature rollouts:

```python
from app.core.dependency_manager import get_service
from app.core.features import Flag, FeatureTarget

class NotificationService:
    def __init__(self, db):
        self.db = db
        self.logger = get_logger("app.services.notification")
        self.feature_service = get_service("feature_service")

    async def send_notification(self, user_id: str, message: str, channel: str = "email"):
        """Send a notification to a user.

        This method uses feature flags to control rollout of new channels.
        """
        self.logger.info("Sending notification", user_id=user_id, channel=channel)

        # Check if push notifications are enabled for this user
        if channel == "push" and not await self.feature_service.is_enabled(
            Flag.PUSH_NOTIFICATIONS,
            target=FeatureTarget.USER,
            target_id=user_id
        ):
            self.logger.info("Push notifications not enabled for user, falling back to email", user_id=user_id)
            channel = "email"

        # Check if we should use the new notification pipeline
        use_new_pipeline = await self.feature_service.is_enabled(
            Flag.NEW_NOTIFICATION_PIPELINE,
            target=FeatureTarget.GLOBAL
        )

        if use_new_pipeline:
            self.logger.info("Using new notification pipeline", user_id=user_id)
            result = await self._send_notification_v2(user_id, message, channel)
        else:
            result = await self._send_notification_v1(user_id, message, channel)

        # If new SMS channel is enabled, send SMS as well for important notifications
        if (
            message.startswith("IMPORTANT") and
            await self.feature_service.is_enabled(
                Flag.SMS_NOTIFICATIONS,
                target=FeatureTarget.USER,
                target_id=user_id,
                percentage=10  # Only 10% of users
            )
        ):
            self.logger.info("Sending additional SMS for important notification", user_id=user_id)
            await self._send_sms(user_id, message)

        return result
```

This pattern demonstrates how to use feature flags for:

1. **User-based targeting** - Enabling features for specific users
2. **Percentage rollouts** - Gradually rolling out to a percentage of users
3. **Global flags** - Enabling/disabling features system-wide
4. **Graceful fallbacks** - Providing alternative behaviors when features aren't enabled
5. **Progressive deployment** - Testing new implementations alongside existing ones
