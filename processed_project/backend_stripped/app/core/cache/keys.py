from __future__ import annotations
import hashlib
import inspect
import json
import re
from typing import Any, Callable, Dict, List, Optional, Tuple
def generate_cache_key(prefix: str, func: Callable, args: Tuple[Any, ...], kwargs: Dict[str, Any], skip_args: Optional[List[int]]=None, skip_kwargs: Optional[List[str]]=None) -> str:
    skip_args = skip_args or []
    skip_kwargs = skip_kwargs or []
    func_name = f'{func.__module__}.{func.__qualname__}'
    sig = inspect.signature(func)
    filtered_args = [arg for i, arg in enumerate(args) if i not in skip_args]
    filtered_kwargs = {key: value for key, value in kwargs.items() if key not in skip_kwargs}
    args_str = json.dumps(filtered_args, sort_keys=True, default=str)
    kwargs_str = json.dumps(filtered_kwargs, sort_keys=True, default=str)
    key_parts = [prefix, func_name, args_str, kwargs_str]
    key_hash = hashlib.md5(json.dumps(key_parts, default=str).encode('utf-8')).hexdigest()
    return f'{prefix}:{func_name}:{key_hash}'
def generate_model_key(prefix: str, model_name: str, model_id: str, field: Optional[str]=None) -> str:
    key = f'{prefix}:{model_name}:{model_id}'
    if field:
        key = f'{key}:{field}'
    return key
def generate_list_key(prefix: str, model_name: str, filters: Optional[Dict[str, Any]]=None) -> str:
    if not filters:
        return f'{prefix}:{model_name}:list'
    filters_str = json.dumps(filters, sort_keys=True, default=str)
    filters_hash = hashlib.md5(filters_str.encode('utf-8')).hexdigest()
    return f'{prefix}:{model_name}:list:{filters_hash}'
def generate_query_key(prefix: str, query_name: str, params: Optional[Dict[str, Any]]=None) -> str:
    if not params:
        return f'{prefix}:{query_name}'
    params_str = json.dumps(params, sort_keys=True, default=str)
    params_hash = hashlib.md5(params_str.encode('utf-8')).hexdigest()
    return f'{prefix}:{query_name}:{params_hash}'
def parse_pattern(pattern: str) -> re.Pattern:
    regex = re.escape(pattern)
    regex = regex.replace('\\*', '.*').replace('\\?', '.')
    return re.compile(f'^{regex}$')