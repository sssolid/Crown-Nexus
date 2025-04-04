from __future__ import annotations
'Permission models and enums.\n\nThis module defines the permission types and role-based permission mappings\nused throughout the application.\n'
import enum
from typing import Dict, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from app.domains.users.models import UserRole
else:
    class UserRole(str, enum.Enum):
        ADMIN = 'admin'
        MANAGER = 'manager'
        CLIENT = 'client'
        DISTRIBUTOR = 'distributor'
        READ_ONLY = 'read_only'
class Permission(str, enum.Enum):
    USER_CREATE = 'user:create'
    USER_READ = 'user:read'
    USER_UPDATE = 'user:update'
    USER_DELETE = 'user:delete'
    USER_ADMIN = 'user:admin'
    PRODUCT_CREATE = 'product:create'
    PRODUCT_READ = 'product:read'
    PRODUCT_UPDATE = 'product:update'
    PRODUCT_DELETE = 'product:delete'
    PRODUCT_ADMIN = 'product:admin'
    MEDIA_CREATE = 'media:create'
    MEDIA_READ = 'media:read'
    MEDIA_UPDATE = 'media:update'
    MEDIA_DELETE = 'media:delete'
    MEDIA_ADMIN = 'media:admin'
    FITMENT_CREATE = 'fitment:create'
    FITMENT_READ = 'fitment:read'
    FITMENT_UPDATE = 'fitment:update'
    FITMENT_DELETE = 'fitment:delete'
    FITMENT_ADMIN = 'fitment:admin'
    COMPANY_CREATE = 'company:create'
    COMPANY_READ = 'company:read'
    COMPANY_UPDATE = 'company:update'
    COMPANY_DELETE = 'company:delete'
    COMPANY_ADMIN = 'company:admin'
    SYSTEM_ADMIN = 'system:admin'
ROLE_PERMISSIONS: Dict[UserRole, Set[Permission]] = {UserRole.ADMIN: {p for p in Permission}, UserRole.MANAGER: {Permission.USER_READ, Permission.USER_CREATE, Permission.USER_UPDATE, Permission.PRODUCT_READ, Permission.PRODUCT_CREATE, Permission.PRODUCT_UPDATE, Permission.PRODUCT_DELETE, Permission.PRODUCT_ADMIN, Permission.MEDIA_READ, Permission.MEDIA_CREATE, Permission.MEDIA_UPDATE, Permission.MEDIA_DELETE, Permission.MEDIA_ADMIN, Permission.FITMENT_READ, Permission.FITMENT_CREATE, Permission.FITMENT_UPDATE, Permission.FITMENT_DELETE, Permission.FITMENT_ADMIN, Permission.COMPANY_READ}, UserRole.CLIENT: {Permission.PRODUCT_READ, Permission.FITMENT_READ, Permission.MEDIA_READ, Permission.COMPANY_READ}, UserRole.DISTRIBUTOR: {Permission.PRODUCT_READ, Permission.FITMENT_READ, Permission.MEDIA_READ, Permission.MEDIA_CREATE, Permission.COMPANY_READ}, UserRole.READ_ONLY: {Permission.PRODUCT_READ, Permission.FITMENT_READ, Permission.MEDIA_READ, Permission.COMPANY_READ}}