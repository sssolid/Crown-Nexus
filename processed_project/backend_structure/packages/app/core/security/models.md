# Module: app.core.security.models

**Path:** `app/core/security/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
```

## Classes

| Class | Description |
| --- | --- |
| `ApiKeyData` |  |
| `PasswordPolicy` |  |
| `SecurityViolation` |  |
| `TokenClaimsModel` |  |
| `TokenPair` |  |
| `TokenType` |  |

### Class: `ApiKeyData`
**Inherits from:** BaseModel

### Class: `PasswordPolicy`
**Inherits from:** BaseModel

### Class: `SecurityViolation`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `INVALID_TOKEN` | `'invalid_token'` |
| `EXPIRED_TOKEN` | `'expired_token'` |
| `CSRF_VIOLATION` | `'csrf_violation'` |
| `RATE_LIMIT_EXCEEDED` | `'rate_limit_exceeded'` |
| `BRUTE_FORCE_ATTEMPT` | `'brute_force_attempt'` |
| `SUSPICIOUS_ACTIVITY` | `'suspicious_activity'` |
| `UNAUTHORIZED_ACCESS` | `'unauthorized_access'` |
| `INVALID_IP` | `'invalid_ip'` |
| `PERMISSION_VIOLATION` | `'permission_violation'` |
| `INJECTION_ATTEMPT` | `'injection_attempt'` |
| `XSS_ATTEMPT` | `'xss_attempt'` |

### Class: `TokenClaimsModel`
**Inherits from:** BaseModel

### Class: `TokenPair`
**Inherits from:** BaseModel

### Class: `TokenType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `ACCESS` | `'access'` |
| `REFRESH` | `'refresh'` |
| `RESET_PASSWORD` | `'reset_password'` |
| `EMAIL_VERIFICATION` | `'email_verification'` |
| `INVITATION` | `'invitation'` |
| `API_KEY` | `'api_key'` |
| `CSRF` | `'csrf'` |
| `SESSION` | `'session'` |
