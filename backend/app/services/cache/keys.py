# backend/app/services/cache/keys.py
"""Utilities for generating and managing cache keys.

This module provides functions for generating consistent and collision-resistant
cache keys based on function names, arguments, and other parameters.
"""
from __future__ import annotations

import hashlib
import inspect
import json
from typing import Any, Callable, Dict, List, Optional, Tuple, get_type_hints

from app.core.logging import get_logger

logger = get_logger(__name__)


def generate_cache_key(
    prefix: str,
    func: Callable,
    args: Tuple,
    kwargs: Dict[str, Any],
    skip_args: Optional[List[str]] = None,
) -> str:
    """
    Generate a cache key based on function name, arguments, and prefix.

    Args:
        prefix: Namespace prefix for the key
        func: The function being cached
        args: Positional arguments to the function
        kwargs: Keyword arguments to the function
        skip_args: Optional list of argument names to exclude

    Returns:
        A consistent cache key string
    """
    # Get function module and name
    module_name = func.__module__
    func_name = func.__qualname__

    # Prepare key parts
    key_parts = [prefix, module_name, func_name]

    # Process arguments and kwargs
    processed_args, processed_kwargs = process_args(func, args, kwargs, skip_args)

    # Add serialized arguments to key parts
    key_parts.append(serialize_for_key(processed_args))
    key_parts.append(serialize_for_key(processed_kwargs))

    # Join parts with colon
    full_key = ":".join(key_parts)

    # For very long keys, use a hash instead
    if len(full_key) > 250:
        hash_key = hashlib.md5(full_key.encode()).hexdigest()
        return f"{prefix}:hash:{hash_key}"

    return full_key


def process_args(
    func: Callable,
    args: Tuple,
    kwargs: Dict[str, Any],
    skip_args: Optional[List[str]] = None,
) -> Tuple[List[Any], Dict[str, Any]]:
    """
    Process function arguments for key generation.

    Args:
        func: The function being cached
        args: Positional arguments
        kwargs: Keyword arguments
        skip_args: Arguments to exclude

    Returns:
        Tuple of (processed_args, processed_kwargs)
    """
    skip_args = skip_args or []

    # Convert args to a list so we can modify it
    args_list = list(args)
    processed_kwargs = kwargs.copy()

    # Get function signature
    sig = inspect.signature(func)
    parameters = list(sig.parameters.values())

    # Handle self/cls for methods
    if args and parameters and parameters[0].name in ('self', 'cls'):
        # For methods, skip the first argument (self/cls)
        args_list = args_list[1:]
        parameters = parameters[1:]

    # Process positional args
    processed_args = []
    for i, arg in enumerate(args_list):
        if i < len(parameters):
            param_name = parameters[i].name
            if param_name not in skip_args:
                processed_args.append(arg)
        else:
            # Variadic args
            processed_args.append(arg)

    # Process keyword args
    for key in list(processed_kwargs.keys()):
        if key in skip_args:
            del processed_kwargs[key]

    return processed_args, processed_kwargs


def serialize_for_key(value: Any) -> str:
    """
    Serialize a value for use in a cache key.

    Args:
        value: The value to serialize

    Returns:
        A string representation suitable for a cache key
    """
    try:
        # Handle special cases
        if callable(value):
            # For callables, use the qualified name
            return f"func:{value.__module__}.{value.__qualname__}"
        elif hasattr(value, '__dict__'):
            # For objects with __dict__, use a stable representation
            return f"obj:{value.__class__.__name__}:{id(value)}"

        # Try to serialize to JSON for everything else
        return json.dumps(
            value,
            sort_keys=True,
            default=_json_default
        )
    except (TypeError, ValueError):
        # Fall back to string representation and ID
        return f"{str(value)}:{id(value)}"


def _json_default(obj: Any) -> Any:
    """
    Custom serializer for types that json can't handle.

    Args:
        obj: The object to serialize

    Returns:
        A serializable representation
    """
    if hasattr(obj, '__dict__'):
        # For objects, use their class name and id
        return f"obj:{obj.__class__.__name__}:{id(obj)}"
    elif hasattr(obj, '__str__'):
        # For objects with string representation
        return str(obj)
    else:
        # For everything else, use a default
        return f"unserializable:{type(obj).__name__}:{id(obj)}"


def make_versioned_key(key: str, version: str) -> str:
    """
    Add a version suffix to a cache key for cache invalidation.

    Args:
        key: The base cache key
        version: Version string

    Returns:
        Versioned cache key
    """
    return f"{key}:v{version}"


def make_prefixed_key(prefix: str, key: str) -> str:
    """
    Add a namespace prefix to a cache key.

    Args:
        prefix: Namespace prefix
        key: Base cache key

    Returns:
        Prefixed cache key
    """
    if not prefix.endswith(':'):
        prefix = f"{prefix}:"
    return f"{prefix}{key}"
