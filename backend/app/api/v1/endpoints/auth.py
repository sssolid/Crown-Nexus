# backend/app/api/v1/endpoints/auth.py
"""
Authentication API endpoints.

This module provides endpoints for user authentication and token management:
- Login endpoint for retrieving JWT tokens
- Token validation endpoint
- Current user information endpoint

The endpoints implement OAuth2 password flow for compatibility with
standard authentication libraries and tools.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.core.config import settings
from app.models.user import User, UserRole, create_access_token, verify_password
from app.schemas.user import Token, TokenPayload, User as UserSchema

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


@router.post("/login", response_model=Token)
async def login_for_access_token(
    db: Annotated[AsyncSession, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Any:
    """
    OAuth2 compatible token login endpoint.

    This endpoint authenticates a user and provides a JWT access token
    for use in subsequent requests. It conforms to the OAuth2 password
    flow specification.

    Args:
        db: Database session
        form_data: Form data with username (email) and password

    Returns:
        Dict: JWT access token and type

    Raises:
        HTTPException: If authentication fails due to invalid credentials
            or inactive user account
    """
    # Get user by email (username in OAuth2 form)
    stmt = select(User).where(User.email == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    # Check credentials
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account"
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        role=user.role,
        expires_delta=access_token_expires
    )

    # Return the token
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/validate-token")
async def validate_token(
    token: Annotated[TokenPayload, Depends(get_current_active_user)],
) -> dict:
    """
    Validate a JWT token.

    This endpoint verifies if a token is valid and active.
    It's useful for client applications to check token validity
    without making a full API request.

    Args:
        token: Decoded token payload (via dependency)

    Returns:
        dict: Token validation status
    """
    return {"valid": True}


@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Any:
    """
    Get current user information.

    This endpoint returns information about the currently
    authenticated user based on their JWT token.

    Args:
        current_user: Current authenticated user (via dependency)

    Returns:
        User: Current user information
    """
    return current_user
