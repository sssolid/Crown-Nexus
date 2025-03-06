# backend/tests/utils.py
"""
Testing utilities and helpers.

This module provides utility functions for:
- Creating test data
- Making authenticated API requests
- Comparing API responses
- Validating model instances

These utilities help reduce code duplication in tests and
provide consistent patterns for common testing tasks.
"""

from __future__ import annotations

import json
import uuid
from typing import Any, Dict, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from pydantic import BaseModel

# Generic type for model
M = TypeVar('M', bound=BaseModel)


async def make_authenticated_request(
    client: AsyncClient,
    method: str,
    url: str,
    token: str,
    **kwargs: Any
) -> Any:
    """
    Make an authenticated request to the API.

    Args:
        client: HTTPX AsyncClient
        method: HTTP method (get, post, put, delete)
        url: API endpoint URL
        token: JWT token for authentication
        **kwargs: Additional arguments to pass to the client method

    Returns:
        Any: API response

    Raises:
        ValueError: If invalid HTTP method is provided
    """
    # Add authorization header
    headers = kwargs.get("headers", {})
    headers["Authorization"] = f"Bearer {token}"
    kwargs["headers"] = headers

    # Call appropriate client method
    method = method.lower()
    if method == "get":
        return await client.get(url, **kwargs)
    elif method == "post":
        return await client.post(url, **kwargs)
    elif method == "put":
        return await client.put(url, **kwargs)
    elif method == "delete":
        return await client.delete(url, **kwargs)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")


def validate_model_response(
    response_data: Dict[str, Any],
    model_type: Type[M],
    exclude_fields: Optional[List[str]] = None
) -> M:
    """
    Validate that an API response matches a model schema.

    Args:
        response_data: API response data
        model_type: Pydantic model class to validate against
        exclude_fields: Fields to exclude from validation

    Returns:
        M: Validated model instance

    Raises:
        ValueError: If response doesn't match model schema
    """
    # Parse response data with model
    exclude_fields = exclude_fields or []
    exclude_set = {field: True for field in exclude_fields}

    try:
        model_instance = model_type(**response_data)
        return model_instance
    except Exception as e:
        raise ValueError(f"Response doesn't match {model_type.__name__} schema: {e}")


def assert_model_data_matches(model: Any, data: Dict[str, Any]) -> None:
    """
    Assert that a model instance data matches the provided data.

    Args:
        model: Model instance
        data: Expected data

    Raises:
        AssertionError: If model data doesn't match expected data
    """
    model_data = jsonable_encoder(model)

    # Check each expected data field
    for key, value in data.items():
        assert key in model_data, f"Key '{key}' not found in model data"
        assert model_data[key] == value, f"Value mismatch for '{key}': expected '{value}', got '{model_data[key]}'"


def create_random_string(length: int = 10) -> str:
    """
    Create a random string for test data.

    Args:
        length: Length of the string to generate

    Returns:
        str: Random string
    """
    import random
    import string

    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def create_random_email() -> str:
    """
    Create a random email for test data.

    Returns:
        str: Random email address
    """
    return f"{create_random_string(8)}@example.com"
