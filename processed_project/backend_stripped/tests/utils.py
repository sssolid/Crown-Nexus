from __future__ import annotations
import random
import string
from typing import Any, Dict, List, Optional, Type, TypeVar
from httpx import AsyncClient
from pydantic import BaseModel
M = TypeVar('M', bound=BaseModel)
def create_random_string(length: int=10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
def create_random_email() -> str:
    return f'{create_random_string(8)}@{create_random_string(6)}.com'
async def make_authenticated_request(client: AsyncClient, method: str, url: str, token: str, **kwargs: Any) -> Any:
    headers = {'Authorization': f'Bearer {token}'}
    if 'headers' in kwargs:
        headers.update(kwargs.pop('headers'))
    if method.lower() == 'get':
        return await client.get(url, headers=headers, **kwargs)
    elif method.lower() == 'post':
        return await client.post(url, headers=headers, **kwargs)
    elif method.lower() == 'put':
        return await client.put(url, headers=headers, **kwargs)
    elif method.lower() == 'delete':
        return await client.delete(url, headers=headers, **kwargs)
    else:
        raise ValueError(f'Unsupported HTTP method: {method}')
def assert_model_data_matches(model: Any, data: Dict[str, Any]) -> None:
    for key, value in data.items():
        assert getattr(model, key) == value, f"Model {key} doesn't match: {getattr(model, key)} != {value}"
def validate_model_response(response_data: Dict[str, Any], model_type: Type[M], exclude_fields: Optional[List[str]]=None) -> M:
    exclude_fields = exclude_fields or []
    filtered_data = {k: v for k, v in response_data.items() if k not in exclude_fields}
    try:
        return model_type.model_validate(filtered_data)
    except Exception as e:
        raise ValueError(f"Response doesn't match {model_type.__name__} schema: {str(e)}") from e