from __future__ import annotations

import functools
import hashlib
import pickle
import typing
from functools import lru_cache
from logging import getLogger

import redis.asyncio as redis
from redis.asyncio import Redis

from src.apps.common.custom_types import EMPTY
from src.server.settings import Settings, get_settings
from src.utils.hash import convert_to_hashtable_value


logger = getLogger(__name__)

SYSTEM_ARGS = {"self", "info", "context", "root", "parent"}


@lru_cache
def get_redis_client() -> redis.Redis | None:
    settings = get_settings()

    if settings.IS_TESTING_MODE:
        return None

    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=False,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True,
        db=settings.REDIS_DB,
    )


def redis_cache(ttl: int = 300) -> typing.Callable:
    """
    Декоратор для кеширования результатов функции в Redis

    Args:
        ttl: время жизни кеша в секундах (default: 300)
    """

    def decorator(func: typing.Callable) -> typing.Callable:
        @functools.wraps(func)
        async def async_wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            settings = get_settings()
            redis_client = await _init_redis_client(settings=settings)
            if not redis_client:
                return await func(*args, **kwargs)
            cache_key = _generate_cache_key(func, *args, **kwargs)
            if not cache_key:
                return await func(*args, **kwargs)
            redis_data = await _get_redis_deserialized_data(redis_client=redis_client, cache_key=cache_key)
            if redis_data is not EMPTY:
                return redis_data
            result = await func(*args, **kwargs)
            await _save_data_to_redis(redis_client=redis_client, function_result=result, ttl=ttl, cache_key=cache_key)
            return result

        return async_wrapper

    return decorator


def _generate_cache_key(func: typing.Callable, *args: typing.Any, **kwargs: typing.Any) -> str | None:
    """Генерирует ключ для кеша. Возвращает None при ошибке."""
    module = getattr(func, "__module__", "unknown")
    qualname = getattr(func, "__qualname__", getattr(func, "__name__", "unknown"))

    # Убираем self/cls из args если это метод класса или его объекта
    if args and hasattr(args[0], "__class__"):
        class_name = args[0].__class__.__name__
        if class_name in qualname:
            args = args[1:]

    filtered_args = [convert_to_hashtable_value(arg) for arg in args]
    filtered_kwargs = {k: convert_to_hashtable_value(v) for k, v in kwargs.items() if k not in SYSTEM_ARGS}

    hash_data = {"module": module, "qualname": qualname, "args": filtered_args, "kwargs": filtered_kwargs}

    try:
        serialized = pickle.dumps(hash_data, protocol=pickle.HIGHEST_PROTOCOL)
        hash_digest = hashlib.md5(serialized).hexdigest()
    except (pickle.PickleError, TypeError) as e:
        logger.warning(f"Cache key generation failed: {e}")
        return None

    return f"cache:{module}:{qualname}:{hash_digest}"


def _convert_for_caching(*, data: typing.Any) -> typing.Any:
    """Конвертирует данные для сохранения в кеш"""
    if isinstance(data, list):
        return [_convert_for_caching(data=item_data) for item_data in data]
    if hasattr(data, "to_pydantic"):
        return data.to_pydantic()
    return data


async def _init_redis_client(*, settings: Settings) -> Redis | None:
    try:
        redis_client = get_redis_client()
        if not redis_client and not settings.IS_TESTING_MODE:
            logger.error("Не удалось инициализировать клиент Redis")
    except (redis.ConnectionError, redis.TimeoutError, redis.RedisError) as e:
        logger.error(f"Redis client connection failed: {e}")
        return None
    return redis_client


async def _get_redis_deserialized_data(*, redis_client: Redis, cache_key: str) -> typing.Any:
    try:
        cached_data = await redis_client.get(cache_key)
    except (redis.ConnectionError, redis.TimeoutError, redis.ResponseError) as e:
        logger.error(f"Redis get operation failed: {e}")
        return EMPTY
    if cached_data is None:
        return EMPTY
    try:
        return pickle.loads(cached_data)
    except (pickle.PickleError, pickle.UnpicklingError, AttributeError, ImportError, EOFError) as e:
        logger.error(f"Cache unpickling failed: {e}")
        return EMPTY


async def _save_data_to_redis(*, function_result: typing.Any, redis_client: Redis, cache_key: str, ttl: int) -> None:
    result_for_hash = _convert_for_caching(data=function_result)
    try:
        serialized = pickle.dumps(result_for_hash)
        await redis_client.setex(cache_key, ttl, serialized)
    except (pickle.PickleError, TypeError) as e:
        logger.warning(f"Failed to serialize result for caching: {e}")
    except (redis.ConnectionError, redis.TimeoutError, redis.ResponseError) as e:
        logger.warning(f"Failed to save to cache: {e}")
