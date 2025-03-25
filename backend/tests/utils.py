# /backend/tests/utils.py
from __future__ import annotations

import random
import string
from typing import Any, Dict, List, Optional, Type, TypeVar

from httpx import AsyncClient
from pydantic import BaseModel

M = TypeVar("M", bound=BaseModel)


def create_random_string(length: int = 10) -> str:
    """Create a random string for test data.

    Args:
        length: Length of the string to generate, defaults to 10

    Returns:
        str: Random string
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def create_random_email() -> str:
    """Create a random email for test data.

    Returns:
        str: Random email address
    """
    return f"{create_random_string(8)}@{create_random_string(6)}.com"


async def make_authenticated_request(
    client: AsyncClient, method: str, url: str, token: str, **kwargs: Any
) -> Any:
    """Make an authenticated request to the API.

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
    headers = {"Authorization": f"Bearer {token}"}
    if "headers" in kwargs:
        headers.update(kwargs.pop("headers"))

    if method.lower() == "get":
        return await client.get(url, headers=headers, **kwargs)
    elif method.lower() == "post":
        return await client.post(url, headers=headers, **kwargs)
    elif method.lower() == "put":
        return await client.put(url, headers=headers, **kwargs)
    elif method.lower() == "delete":
        return await client.delete(url, headers=headers, **kwargs)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")


def assert_model_data_matches(model: Any, data: Dict[str, Any]) -> None:
    """Assert that a model instance data matches the provided data.

    Args:
        model: Model instance
        data: Expected data

    Raises:
        AssertionError: If model data doesn't match expected data
    """
    for key, value in data.items():
        assert (
            getattr(model, key) == value
        ), f"Model {key} doesn't match: {getattr(model, key)} != {value}"


def validate_model_response(
    response_data: Dict[str, Any],
    model_type: Type[M],
    exclude_fields: Optional[List[str]] = None,
) -> M:
    """Validate that an API response matches a model schema.

    Args:
        response_data: API response data
        model_type: Pydantic model class to validate against
        exclude_fields: Fields to exclude from validation, defaults to None

    Returns:
        M: Validated model instance

    Raises:
        ValueError: If response doesn't match model schema
    """
    exclude_fields = exclude_fields or []

    # Remove excluded fields from response data
    filtered_data = {k: v for k, v in response_data.items() if k not in exclude_fields}

    try:
        # Try to parse the data using the model
        return model_type.model_validate(filtered_data)
    except Exception as e:
        raise ValueError(
            f"Response doesn't match {model_type.__name__} schema: {str(e)}"
        ) from e
