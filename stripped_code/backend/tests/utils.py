from __future__ import annotations
import json
import uuid
from typing import Any, Dict, List, Optional, Type, TypeVar
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from pydantic import BaseModel
M = TypeVar('M', bound=BaseModel)
async def make_authenticated_request(client: AsyncClient, method: str, url: str, token: str, **kwargs: Any) -> Any:
    headers = kwargs.get('headers', {})
    headers['Authorization'] = f'Bearer {token}'
    kwargs['headers'] = headers
    method = method.lower()
    if method == 'get':
        return await client.get(url, **kwargs)
    elif method == 'post':
        return await client.post(url, **kwargs)
    elif method == 'put':
        return await client.put(url, **kwargs)
    elif method == 'delete':
        return await client.delete(url, **kwargs)
    else:
        raise ValueError(f'Unsupported HTTP method: {method}')
def validate_model_response(response_data: Dict[str, Any], model_type: Type[M], exclude_fields: Optional[List[str]]=None) -> M:
    exclude_fields = exclude_fields or []
    exclude_set = {field: True for field in exclude_fields}
    try:
        model_instance = model_type(**response_data)
        return model_instance
    except Exception as e:
        raise ValueError(f"Response doesn't match {model_type.__name__} schema: {e}")
def assert_model_data_matches(model: Any, data: Dict[str, Any]) -> None:
    model_data = jsonable_encoder(model)
    for key, value in data.items():
        assert key in model_data, f"Key '{key}' not found in model data"
        assert model_data[key] == value, f"Value mismatch for '{key}': expected '{value}', got '{model_data[key]}'"
def create_random_string(length: int=10) -> str:
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
def create_random_email() -> str:
    return f'{create_random_string(8)}@example.com'