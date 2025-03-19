# /backend/app/core/cache/keys.py
from __future__ import annotations

import hashlib
import inspect
import json
import re
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union


def generate_cache_key(
    prefix: str,
    func: Callable,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    skip_args: Optional[List[int]] = None,
    skip_kwargs: Optional[List[str]] = None,
) -> str:
    """Generate a cache key for a function call.

    This function creates a deterministic key based on the function name,
    argument values, and keyword argument values. It's used by cache
    decorators to create unique keys for caching function results.

    Args:
        prefix: Key prefix
        func: Function being called
        args: Positional arguments
        kwargs: Keyword arguments
        skip_args: Indices of positional arguments to skip
        skip_kwargs: Names of keyword arguments to skip

    Returns:
        str: Cache key
    """
    # Normalize skip_args and skip_kwargs
    skip_args = skip_args or []
    skip_kwargs = skip_kwargs or []

    # Get function name and module
    func_name = f"{func.__module__}.{func.__qualname__}"

    # Get signature
    sig = inspect.signature(func)

    # Filter args
    filtered_args = [arg for i, arg in enumerate(args) if i not in skip_args]

    # Filter kwargs
    filtered_kwargs = {
        key: value for key, value in kwargs.items() if key not in skip_kwargs
    }

    # Convert args and kwargs to strings
    args_str = json.dumps(filtered_args, sort_keys=True, default=str)
    kwargs_str = json.dumps(filtered_kwargs, sort_keys=True, default=str)

    # Generate hash
    key_parts = [prefix, func_name, args_str, kwargs_str]
    key_hash = hashlib.md5(
        json.dumps(key_parts, default=str).encode("utf-8")
    ).hexdigest()

    # Create key
    return f"{prefix}:{func_name}:{key_hash}"


def generate_model_key(
    prefix: str, model_name: str, model_id: str, field: Optional[str] = None
) -> str:
    """Generate a cache key for a model instance.

    Args:
        prefix: Key prefix
        model_name: Model name
        model_id: Model ID
        field: Optional field name

    Returns:
        str: Cache key
    """
    key = f"{prefix}:{model_name}:{model_id}"
    if field:
        key = f"{key}:{field}"
    return key


def generate_list_key(
    prefix: str, model_name: str, filters: Optional[Dict[str, Any]] = None
) -> str:
    """Generate a cache key for a list of model instances.

    Args:
        prefix: Key prefix
        model_name: Model name
        filters: Optional filters

    Returns:
        str: Cache key
    """
    if not filters:
        return f"{prefix}:{model_name}:list"

    # Convert filters to string
    filters_str = json.dumps(filters, sort_keys=True, default=str)

    # Generate hash
    filters_hash = hashlib.md5(filters_str.encode("utf-8")).hexdigest()

    return f"{prefix}:{model_name}:list:{filters_hash}"


def generate_query_key(
    prefix: str, query_name: str, params: Optional[Dict[str, Any]] = None
) -> str:
    """Generate a cache key for a query result.

    Args:
        prefix: Key prefix
        query_name: Query name
        params: Optional query parameters

    Returns:
        str: Cache key
    """
    if not params:
        return f"{prefix}:{query_name}"

    # Convert params to string
    params_str = json.dumps(params, sort_keys=True, default=str)

    # Generate hash
    params_hash = hashlib.md5(params_str.encode("utf-8")).hexdigest()

    return f"{prefix}:{query_name}:{params_hash}"


def parse_pattern(pattern: str) -> re.Pattern:
    """Parse a glob pattern into a regex pattern.

    Args:
        pattern: Glob pattern

    Returns:
        re.Pattern: Regex pattern
    """
    # Escape special characters
    regex = re.escape(pattern)

    # Convert glob wildcards to regex wildcards
    regex = regex.replace(r"\*", ".*").replace(r"\?", ".")

    # Compile regex
    return re.compile(f"^{regex}$")
