from __future__ import annotations

import inspect
import time
import typing
from functools import wraps
from logging import getLogger


logger = getLogger(__name__)


T = typing.TypeVar("T")


def log_execution_time(operation_name: str, warning_threshold: float = 1.0) -> typing.Callable:
    def decorator(func: typing.Callable) -> typing.Callable:
        def _calculate_and_log(start_time: float) -> None:
            end_time = time.perf_counter()
            execution_time = end_time - start_time

            if execution_time > warning_threshold:
                logger.warning(
                    f"{operation_name} | Время: {execution_time:.2f} сек | Статус: МЕДЛЕННО (>{warning_threshold}сек)"
                )

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
                start_time = time.perf_counter()
                result = await func(*args, **kwargs)
                _calculate_and_log(start_time=start_time)
                return result

            return async_wrapper

        @wraps(func)
        def sync_wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            _calculate_and_log(start_time=start_time)
            return result

        return sync_wrapper

    return decorator
