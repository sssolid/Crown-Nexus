from __future__ import annotations
'Permission system for application-wide authorization.\n\nThis module re-exports the components from the permissions package\nto maintain backward compatibility.\n'
from app.core.permissions.decorators import require_permission, require_permissions, require_admin
require_permission = require_permission
require_permissions = require_permissions
require_admin = require_admin