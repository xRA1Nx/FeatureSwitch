from __future__ import annotations

import functools
import os
import typing
from contextlib import asynccontextmanager
from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from src.apps.common.constants import POSTGRES_DB_URL_ASYNC_PREFIX, POSTGRES_DB_URL_PREFIX
from src.server.settings import Settings, get_settings


logger = getLogger(__name__)


def get_db_url(*, is_async: bool) -> str:
    """Получение ссылки БД postgresql."""
    settings = get_settings()
    if not settings.IS_TESTING_MODE:
        return get_postgres_db_url(is_async=is_async, settings=settings)
    return get_postgres_test_db_url(is_async=is_async, settings=settings)


def get_postgres_db_url(*, is_async: bool, settings: Settings) -> str:
    url_prefix = POSTGRES_DB_URL_ASYNC_PREFIX if is_async else POSTGRES_DB_URL_PREFIX
    return make_url_for_postgres_db(url_prefix=url_prefix, settings=settings)


def get_postgres_test_db_url(*, is_async: bool, settings: Settings) -> str:
    url_prefix = POSTGRES_DB_URL_ASYNC_PREFIX if is_async else POSTGRES_DB_URL_PREFIX
    return make_url_for_test_postgres_db(url_prefix=url_prefix, settings=settings)


def make_url_for_postgres_db(*, url_prefix: str, settings: Settings) -> str:
    return (
        f"{url_prefix}://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


def get_test_db_name() -> str:
    test_db_postfix = os.getenv("CI_JOB_ID", "local")
    return f"test_{test_db_postfix}"


def make_url_for_test_postgres_db(*, url_prefix: str, settings: Settings) -> str:
    db_name = get_test_db_name()
    return (
        f"{url_prefix}://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{db_name}"
    )


@functools.lru_cache
def get_async_engine() -> AsyncEngine:
    url = get_db_url(is_async=True)
    return create_async_engine(url=url, pool_size=20, max_overflow=10, pool_pre_ping=True, pool_recycle=3600)


def get_async_session() -> AsyncSession:
    """Создание объекта асинхронной сессии."""
    engine = get_async_engine()
    return AsyncSession(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def async_session_generator() -> typing.AsyncGenerator[AsyncSession]:
    """Асинхронный контекстный менеджер для работы с удалённой БД."""
    engine = get_async_engine()
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def optional_session_generator(*, session: AsyncSession | None) -> typing.AsyncGenerator[AsyncSession]:
    """Возвращает либо переданную сессию, либо созданную генератором сессий."""
    if session is None:
        async with async_session_generator() as new_session:
            yield new_session
    else:
        yield session
