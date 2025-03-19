Standardize exception usage across all services to use core exception classes.

Ensure all services use get_logger from app.core.logging.

The following are better as core modules then as services
Move app/services/error/* out of services and make it core functionality in app/core/error
Move app/services/pagination/* out of services and make it core functionality in app/core/pagination
Move app/services/validation/* out of services and make it core functionality in app/core/validation
Move app/services/metrics/* out of services and make it core functionality in app/core/metrics

audit, media, search, and base_service all stay as services

Migrate any unique functionality from app/services/base_service/permissions.py to app/core/permissions.py.  Decompose app/core/permissions.py into different files if necessary.

Consolidate app/core/security/rate_limiting.py to app/core/rate_limiting.py and use only the app/core/rate_limiting.py.

Enforce consistent use of BaseService for all services that need CRUD operations. Create simpler base classes for services that don't need full CRUD operations.

Standardize all repositories to follow BaseRepository pattern.  Ensure all database access goes through repositories.  Remove direct SQL queries from services.  Create a consistent pattern for custom repository methods.

Use a single approach for service registration through dependency_manager.py.  Remove redundant service registration in main.py.  Create a proper dependency graph to order initialization correctly.  Implement a clear distinction between singleton and per-request services.

Explicitly define service initialization order based on dependencies.  Add dependency tracking to detect circular dependencies. Implement a phased initialization approach for complex dependencies.  Add better error handling during initialization.

Review middleware stack for redundancy.  Ensure consistent middleware ordering.  Considering combining related middleware functionality. Document middleware dependencies and requirements.

Consolidate utility functions, remove unused ones.  Ensure consistent usage of utilities throughout the project. Move utility functions that belong in core to appropriate core modules.  Establish clear boundaries between utils and services.
