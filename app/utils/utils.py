import time
import functools
from typing import Callable, TypeVar, Any

T = TypeVar("T")


# Utility functions for the application
def timing_decorator(func: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time:.4f} seconds to execute")
        return result

    return wrapper
