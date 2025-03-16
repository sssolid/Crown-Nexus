# backend/app/api/deps.py
"""
API dependency providers.

This module defines FastAPI dependency providers for database sessions,
authentication, and authorization. These dependencies are used throughout
the API routes to ensure consistent access control and resource management.

The module provides:
- Database session dependency
- Authentication dependencies for different authorization levels
- Pagination parameter handling
- Error handling for auth failures
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Dict, Optional, Union

from fastapi import Depends, HTTPException, Query, WebSocket, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect

from app.core.config import settings
from app.core.logging import get_logger, set_user_id
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import TokenPayload

# Create a logger for this module
logger = get_logger("app.api.deps")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """
    Get the current authenticated user.

    This dependency validates the JWT token, decodes it, and retrieves
    the corresponding user from the database.

    Args:
        db: Database session
        token: JWT token

    Returns:
        User: Authenticated user

    Raises:
        HTTPException: If authentication fails, token is invalid,
            or user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode and validate the JWT token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)

        # Check if token has expired
        current_time = int(datetime.utcnow().timestamp())
        if token_data.exp < current_time:
            logger.warning(
                "Token expired",
                token_exp=token_data.exp,
                current_time=current_time,
                expires_in=token_data.exp - current_time
            )
            raise credentials_exception
            
    except (JWTError, ValidationError) as e:
        # Log the error with more details for debugging
        logger.warning(
            "Token validation failed",
            error=str(e),
            error_type=type(e).__name__
        )
        raise credentials_exception from e

    # Get the user from the database
    stmt = select(User).where(User.id == token_data.sub)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        logger.warning(
            "User from token not found",
            user_id=token_data.sub
        )
        raise credentials_exception

    # Add user ID to the logging context
    set_user_id(str(user.id))
    
    logger.debug(
        "User authenticated",
        user_id=str(user.id),
        user_role=user.role
    )
    
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Get the current active user.

    This dependency builds on get_current_user and ensures the user
    is active in the system.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current active user

    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        logger.warning(
            "Inactive user attempted access",
            user_id=str(current_user.id)
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user


async def get_admin_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """
    Get the current active admin user.

    This dependency builds on get_current_active_user and ensures the
    user has admin role.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current active admin user

    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.role != UserRole.ADMIN:
        logger.warning(
            "Non-admin user attempted admin action",
            user_id=str(current_user.id),
            user_role=current_user.role
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return current_user


async def get_manager_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """
    Get the current active manager or admin user.

    This dependency builds on get_current_active_user and ensures the
    user has manager or admin role.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current active manager or admin user

    Raises:
        HTTPException: If user is not a manager or admin
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        logger.warning(
            "Non-manager user attempted manager action",
            user_id=str(current_user.id),
            user_role=current_user.role
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return current_user


# Type definitions for pagination parameters
PaginationParams = Dict[str, Union[int, float]]


def get_pagination(
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
) -> PaginationParams:
    """
    Get pagination parameters.

    This dependency generates pagination parameters based on page number and size,
    with validation to ensure reasonable values.

    Args:
        page: Page number (starting from 1)
        page_size: Number of items per page (max 100)

    Returns:
        Dict: Pagination parameters including:
            - skip: Number of items to skip
            - limit: Number of items to return
            - page: Current page number
            - page_size: Items per page
    """
    # Ensure valid values
    page = max(1, page)
    page_size = max(1, min(100, page_size))

    return {
        "skip": (page - 1) * page_size,
        "limit": page_size,
        "page": page,
        "page_size": page_size,
    }


# Optional authenticated user dependency for endpoints that accept both
# authenticated and anonymous users
async def get_optional_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: str = Depends(OAuth2PasswordBearer(
        tokenUrl=f"{settings.API_V1_STR}/auth/login",
        auto_error=False
    )),
) -> Optional[User]:
    """
    Get the current user if authenticated, otherwise None.

    This dependency is useful for endpoints that can be accessed both
    by authenticated and anonymous users, with different behavior.

    Args:
        db: Database session
        token: Optional JWT token

    Returns:
        Optional[User]: Authenticated user or None
    """
    if not token:
        logger.debug("No authentication token provided")
        return None

    try:
        # Decode and validate the JWT token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)

        # Check if token has expired
        current_time = int(datetime.utcnow().timestamp())
        if token_data.exp < current_time:
            logger.debug(
                "Optional token expired",
                token_exp=token_data.exp,
                current_time=current_time
            )
            return None

        # Get the user from the database
        stmt = select(User).where(User.id == token_data.sub)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user and user.is_active:
            # Add user ID to the logging context
            set_user_id(str(user.id))
            
            logger.debug(
                "Optional user authenticated",
                user_id=str(user.id),
                user_role=user.role
            )
            return user
        
        if not user:
            logger.debug(
                "Optional token user not found",
                user_id=token_data.sub
            )
        elif not user.is_active:
            logger.debug(
                "Optional token user is inactive",
                user_id=str(user.id)
            )

    except (JWTError, ValidationError) as e:
        logger.debug(
            "Optional token validation failed",
            error=str(e),
            error_type=type(e).__name__
        )

    return None


async def get_current_user_ws(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Get the current authenticated user from WebSocket connection.
    
    This dependency extracts the JWT token from WebSocket query parameters
    or cookies, validates it, and returns the corresponding user.
    
    Args:
        websocket: WebSocket connection
        db: Database session
        
    Returns:
        User: Authenticated user
        
    Raises:
        WebSocketDisconnect: If authentication fails
    """
    try:
        # Try to get token from query parameters
        token = websocket.query_params.get("token")
        
        # If not in query params, try to get from cookies
        if not token and "token" in websocket.cookies:
            token = websocket.cookies["token"]
        
        # If not in cookies, try authorization header
        if not token:
            headers = dict(websocket.headers)
            auth_header = headers.get("authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
        
        if not token:
            # No token found
            logger.warning(
                "WebSocket connection without token",
                client=websocket.client.host
            )
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION)
        
        # Validate token
        credentials_exception = WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION)
        
        try:
            # Decode and validate the JWT token
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            token_data = TokenPayload(**payload)
            
            # Check if token has expired
            current_time = int(datetime.utcnow().timestamp())
            if token_data.exp < current_time:
                logger.warning(
                    "WebSocket token expired",
                    token_exp=token_data.exp,
                    current_time=current_time,
                    client=websocket.client.host
                )
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                raise credentials_exception
        except (JWTError, ValidationError) as e:
            logger.warning(
                "WebSocket token validation failed",
                error=str(e),
                error_type=type(e).__name__,
                client=websocket.client.host
            )
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise credentials_exception
        
        # Get the user from the database
        stmt = select(User).where(User.id == token_data.sub)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user is None or not user.is_active:
            logger.warning(
                "WebSocket user not found or inactive",
                user_id=token_data.sub,
                client=websocket.client.host
            )
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise credentials_exception
        
        # Add user ID to the logging context
        set_user_id(str(user.id))
        
        logger.debug(
            "WebSocket user authenticated",
            user_id=str(user.id),
            user_role=user.role,
            client=websocket.client.host
        )
        
        return user
    
    except WebSocketDisconnect:
        raise
    except Exception as e:
        logger.exception(
            "Unexpected error in WebSocket authentication",
            error=str(e),
            error_type=type(e).__name__,
            client=getattr(websocket, "client", {}).get("host", "unknown")
        )
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION)