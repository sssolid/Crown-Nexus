from __future__ import annotations
import inspect
import logging
from typing import Any, Callable, Dict, Optional, Type, TypeVar, cast
T = TypeVar('T')
class DependencyManager:
    _instance = None
    _dependencies: Dict[str, Any] = {}
    _factories: Dict[str, Callable[..., Any]] = {}
    def __new__(cls) -> DependencyManager:
        if cls._instance is None:
            cls._instance = super(DependencyManager, cls).__new__(cls)
            cls._instance._dependencies = {}
            cls._instance._factories = {}
        return cls._instance
    def register_dependency(self, name: str, instance: Any) -> None:
        self._dependencies[name] = instance
    def register_factory(self, name: str, factory: Callable[..., Any]) -> None:
        self._factories[name] = factory
    def get(self, name: str, **kwargs: Any) -> Any:
        if name in self._dependencies:
            return self._dependencies[name]
        if name in self._factories:
            instance = self._factories[name](**kwargs)
            self._dependencies[name] = instance
            return instance
        raise ValueError(f'Dependency not registered: {name}')
    def get_instance(self, cls: Type[T], **kwargs: Any) -> T:
        class_name = cls.__name__
        return cast(T, self.get(class_name, **kwargs))
    def clear(self) -> None:
        self._dependencies.clear()
    def clear_instance(self, name: str) -> None:
        if name in self._dependencies:
            del self._dependencies[name]
dependency_manager = DependencyManager()
def get_dependency(name: str, **kwargs: Any) -> Any:
    return dependency_manager.get(name, **kwargs)
def inject_dependency(dependency_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            dependency = get_dependency(dependency_name)
            kwargs[dependency_name] = dependency
            return func(*args, **kwargs)
        return wrapper
    return decorator