# Module: app.core.security

**Path:** `app/core/security/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.security.api_keys import ApiKeyManager, generate_api_key, verify_api_key
from app.core.security.csrf import CsrfManager, generate_csrf_token, validate_csrf_token
from app.core.security.encryption import EncryptionManager, decrypt_data, encrypt_data, generate_secure_token
from app.core.security.models import ApiKeyData, PasswordPolicy, SecurityViolation, TokenClaimsModel, TokenPair, TokenType
from app.core.security.passwords import PasswordManager, get_password_hash, validate_password_policy, verify_password
from app.core.security.service import SecurityService, get_security_service
from app.core.security.tokens import TokenManager, add_token_to_blacklist, create_token, create_token_pair, decode_token, is_token_blacklisted, refresh_tokens, revoke_token
from app.core.security.validation import ValidationManager, detect_suspicious_content, get_security_headers, is_trusted_ip, is_valid_enum_value, is_valid_hostname, moderate_content, sanitize_input, validate_json_input
from app.core.security.dependencies import get_current_user_id, get_token_from_header, oauth2_scheme
```

## Global Variables
```python
__all__ = __all__ = [
    # Service
    "SecurityService",
    "get_security_service",
    # API Keys
    "ApiKeyManager",
    "generate_api_key",
    "verify_api_key",
    # CSRF Protection
    "CsrfManager",
    "generate_csrf_token",
    "validate_csrf_token",
    # Encryption
    "EncryptionManager",
    "decrypt_data",
    "encrypt_data",
    "generate_secure_token",
    # Models
    "ApiKeyData",
    "PasswordPolicy",
    "SecurityViolation",
    "TokenClaimsModel",
    "TokenPair",
    "TokenType",
    # Passwords
    "PasswordManager",
    "get_password_hash",
    "validate_password_policy",
    "verify_password",
    # Tokens
    "TokenManager",
    "add_token_to_blacklist",
    "create_token",
    "create_token_pair",
    "decode_token",
    "is_token_blacklisted",
    "refresh_tokens",
    "revoke_token",
    # Validation
    "ValidationManager",
    "detect_suspicious_content",
    "get_security_headers",
    "is_trusted_ip",
    "is_valid_enum_value",
    "is_valid_hostname",
    "moderate_content",
    "sanitize_input",
    "validate_json_input",
    # FastAPI Dependencies
    "get_current_user_id",
    "get_token_from_header",
    "oauth2_scheme",
]
```
