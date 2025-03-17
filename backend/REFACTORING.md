## Essential Core Services

1. **Logging Service**
    - Most modules initialize a logger using `get_logger("module.name")`
    - File: `/app/core/logging.py`

2. **Configuration**
    - Settings are accessed via `settings` singleton
    - File: `/app/core/config.py`

3. **Exception Handling**
    - Custom exceptions for various error scenarios
    - File: `/app/core/exceptions.py`

4. **Dependency Manager**
    - Used for service registration and retrieval
    - File: `/app/core/dependency_manager.py`

5. **Service Registry**
    - Centralized registry for application services
    - File: `/app/core/service_registry.py`

## Additional Common Services

Depending on the specific file you're working on, you might also need:

6. **Database Utilities**
    - Transaction management, CRUD operations
    - Files: `/app/db/utils.py`, `/app/db/base_class.py`

7. **Cache Service**
    - Used for data caching
    - File: `/app/services/cache_service.py`

8. **Security Service**
    - Authentication, authorization, encryption
    - File: `/app/services/security_service.py`

9. **Error Handling Service**
    - Centralized error formatting
    - File: `/app/services/error_handling_service.py`

10. **Metrics Service**
    - Application metrics tracking
    - File: `/app/services/metrics_service.py`

For API endpoints, you'll typically need:
- `/app/api/deps.py` - FastAPI dependencies
- `/app/api/responses.py` - Response formatting

For service implementations:
- `/app/services/base.py` - Base service class
- `/app/services/interfaces.py` - Service interfaces
