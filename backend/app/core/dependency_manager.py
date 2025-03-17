# /backend/app/core/dependency_manager.py
from __future__ import annotations

import inspect
import logging
from typing import Any, Callable, Dict, Optional, Type, TypeVar, cast

# Type variable for dependency classes
T = TypeVar('T')

class DependencyManager:
    """Manager for application dependencies.
    
    This class provides a central registry for all dependencies in the application,
    allowing for better organization, testing, and dependency injection.
    """
    
    _instance = None
    _dependencies: Dict[str, Any] = {}
    _factories: Dict[str, Callable[..., Any]] = {}
    
    def __new__(cls) -> DependencyManager:
        """Create a singleton instance of the dependency manager.
        
        Returns:
            DependencyManager: The singleton instance
        """
        if cls._instance is None:
            cls._instance = super(DependencyManager, cls).__new__(cls)
            cls._instance._dependencies = {}
            cls._instance._factories = {}
        return cls._instance
    
    def register_dependency(self, name: str, instance: Any) -> None:
        """Register a dependency instance.
        
        Args:
            name: Dependency name
            instance: Dependency instance
        """
        self._dependencies[name] = instance
        
    def register_factory(self, name: str, factory: Callable[..., Any]) -> None:
        """Register a factory function for creating dependencies.
        
        Args:
            name: Dependency name
            factory: Factory function
        """
        self._factories[name] = factory
        
    def get(self, name: str, **kwargs: Any) -> Any:
        """Get a dependency instance.
        
        If the dependency is not already registered, it will be created using
        the registered factory function.
        
        Args:
            name: Dependency name
            **kwargs: Arguments to pass to the factory function
        
        Returns:
            Any: Dependency instance
        
        Raises:
            ValueError: If dependency is not registered
        """
        # Return existing instance if available
        if name in self._dependencies:
            return self._dependencies[name]
            
        # Create instance using factory if available
        if name in self._factories:
            instance = self._factories[name](**kwargs)
            self._dependencies[name] = instance
            return instance
            
        raise ValueError(f"Dependency not registered: {name}")
    
    def get_instance(self, cls: Type[T], **kwargs: Any) -> T:
        """Get a dependency instance by class.
        
        Args:
            cls: Dependency class
            **kwargs: Arguments to pass to the factory function
        
        Returns:
            T: Dependency instance
        
        Raises:
            ValueError: If dependency is not registered
        """
        class_name = cls.__name__
        return cast(T, self.get(class_name, **kwargs))
        
    def clear(self) -> None:
        """Clear all registered dependencies.
        
        This is useful for testing to ensure a clean state.
        """
        self._dependencies.clear()
        
    def clear_instance(self, name: str) -> None:
        """Clear a specific dependency instance.
        
        Args:
            name: Dependency name
        """
        if name in self._dependencies:
            del self._dependencies[name]

# Create singleton instance
dependency_manager = DependencyManager()

def get_dependency(name: str, **kwargs: Any) -> Any:
    """Get a dependency instance.
    
    This is a convenience function for getting a dependency instance.
    
    Args:
        name: Dependency name
        **kwargs: Arguments to pass to the factory function
    
    Returns:
        Any: Dependency instance
    """
    return dependency_manager.get(name, **kwargs)

def inject_dependency(dependency_name: str) -> Callable:
    """Decorator for injecting dependencies.
    
    This decorator injects a dependency into a function or method.
    
    Args:
        dependency_name: Name of the dependency to inject
    
    Returns:
        Callable: Decorated function or method
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get dependency
            dependency = get_dependency(dependency_name)
            
            # Inject dependency into kwargs
            kwargs[dependency_name] = dependency
            
            # Call function with injected dependency
            return func(*args, **kwargs)
        return wrapper
    return decorator
