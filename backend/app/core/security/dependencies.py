from __future__ import annotations

"""FastAPI security dependencies.

This module provides dependency functions for FastAPI to handle authentication
and authorization in request handlers.
"""

import time
from typing import Optional, Union

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.dependency_manager import get_service
from app.core.error import handle_exception
from app.core.exceptions import AuthenticationException
from app.logging import get_logger, set_user_id
from app.core.security.service import get_security_service
from app.core.security.tokens import decode_token

logger = get_logger("app.core.security.dependencies")

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# Optional OAuth2 scheme that doesn't raise when token is missing
optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False
)


async def get_token_from_header(
    token: str = Depends(oauth2_scheme), request: Request = None
) -> str:
    """Extract and verify JWT token from authorization header.

    Args:
        token: The token from the OAuth2 scheme
        request: Optional request object for metrics and context

    Returns:
        str: The validated token

    Raises:
        HTTPException: If the token is invalid
    """
    start_time = time.monotonic()

    try:
        # Track metrics if available
        if request and hasattr(request.state, "request_id"):
            try:
                metrics_service = get_service("metrics_service")
                metrics_service.increment_counter(
                    "token_dependencies_total",
                    labels={"dependency": "get_token_from_header"},
                )
            except Exception:
                pass

        return token
    except Exception as e:
        logger.error(f"Error in token dependency: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    finally:
        # Track duration metrics if available
        if request:
            try:
                duration = time.monotonic() - start_time
                metrics_service = get_service("metrics_service")
                metrics_service.observe_histogram(
                    "token_dependency_duration_seconds",
                    duration,
                    {"dependency": "get_token_from_header"},
                )
            except Exception:
                pass


async def get_current_user_id(
    token: str = Depends(get_token_from_header), request: Request = None
) -> str:
    """Extract user ID from a valid JWT token.

    Args:
        token: The JWT token
        request: Optional request object for metrics and context

    Returns:
        str: The user ID from the token

    Raises:
        AuthenticationException: If the token is invalid
    """
    start_time = time.monotonic()
    request_id = getattr(request.state, "request_id", None) if request else None

    try:
        # Use security service if available
        try:
            security_service = get_security_service()
            token_data = await security_service.validate_token(token, request_id)

            # Set user ID in logging context
            set_user_id(token_data.sub)

            return token_data.sub
        except Exception:
            # Fall back to direct token decoding
            token_data = await decode_token(token)

            # Set user ID in logging context
            set_user_id(token_data.sub)

            return token_data.sub
    except AuthenticationException:
        raise
    except Exception as e:
        logger.error(f"Error getting user ID from token: {str(e)}")
        handle_exception(e, request_id=request_id)
        raise AuthenticationException(message="Could not authenticate user") from e
    finally:
        # Track metrics if available
        if request:
            try:
                duration = time.monotonic() - start_time
                metrics_service = get_service("metrics_service")
                metrics_service.observe_histogram(
                    "token_dependency_duration_seconds",
                    duration,
                    {"dependency": "get_current_user_id"},
                )
            except Exception:
                pass


async def get_optional_user_id(
    token: Optional[str] = Depends(optional_oauth2_scheme), request: Request = None
) -> Optional[str]:
    """Extract user ID from a token, returning None if no valid token.

    Args:
        token: The optional JWT token
        request: Optional request object for metrics and context

    Returns:
        Optional[str]: The user ID from the token, or None if no valid token
    """
    if not token:
        return None

    try:
        return await get_current_user_id(token, request)
    except (AuthenticationException, HTTPException):
        return None


async def get_current_user_with_permissions(
    token: str = Depends(get_token_from_header),
    request: Request = None,
    db=None,  # This would be replaced with the proper DB dependency
) -> Union[dict, Any]:
    """Get current user with their permissions from a valid token.

    Args:
        token: The JWT token
        request: Optional request object for metrics and context
        db: Optional database session

    Returns:
        dict: User data with permissions

    Raises:
        AuthenticationException: If authentication fails
    """
    start_time = time.monotonic()
    request_id = getattr(request.state, "request_id", None) if request else None

    try:
        # Decode token
        security_service = get_security_service()
        token_data = await security_service.validate_token(token, request_id)

        # Set user ID in logging context
        set_user_id(token_data.sub)

        # Get permissions if necessary
        user_data = {
            "id": token_data.sub,
            "role": token_data.role,
            "permissions": token_data.permissions or [],
        }

        # Add any user data from token
        if token_data.user_data:
            user_data.update(token_data.user_data)

        return user_data
    except AuthenticationException:
        raise
    except Exception as e:
        logger.error(f"Error getting user from token: {str(e)}")
        handle_exception(e, request_id=request_id)
        raise AuthenticationException(message="Could not authenticate user") from e
    finally:
        # Track metrics if available
        if request:
            try:
                duration = time.monotonic() - start_time
                metrics_service = get_service("metrics_service")
                metrics_service.observe_histogram(
                    "token_dependency_duration_seconds",
                    duration,
                    {"dependency": "get_current_user_with_permissions"},
                )
            except Exception:
                pass
