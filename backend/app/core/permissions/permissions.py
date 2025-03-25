# /app/core/permissions.py
from __future__ import annotations

"""Permission system for application-wide authorization.

This module re-exports the components from the permissions package
to maintain backward compatibility.
"""

# Redirect imports to the new package structure
from app.core.permissions.decorators import (
    require_permission,
    require_permissions,
    require_admin,
)

# For backward compatibility
require_permission = require_permission
require_permissions = require_permissions
require_admin = require_admin
