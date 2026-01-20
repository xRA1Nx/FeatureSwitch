from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.apps.common.exceptions import ConfigurationsException
from src.apps.common.models import BaseModel
from src.apps.router import api_router
from src.server.db import get_async_session, get_db_url, get_test_db_name
from src.server.settings import get_settings
from src.utils.sql_alchemy import check_db_exists
from src.utils.testing import SessionHolder


if TYPE_CHECKING:
    from unittest.mock import Mock

pytest_plugins = ()


@pytest.fixture(autouse=True)
def setup_factories(db_async_session):
    SessionHolder.set_session(db_async_session)


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def async_test_database():
    """Создает Асинхронный движок базы данных."""
    is_testing_mode = os.getenv("IS_TESTING_MODE")
    db_name = get_test_db_name()
    test_db_url = get_db_url(is_async=True)
    test_engine = create_async_engine(url=test_db_url)
    if not is_testing_mode or not db_name.startswith("test"):
        raise ConfigurationsException("Ошибка конфигурации тестовой БД проекта")

    settings = get_settings()
    admin_url = (
        f"postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    admin_engine = create_async_engine(url=admin_url, isolation_level="AUTOCOMMIT")

    async with admin_engine.connect() as connection:
        is_db_exists = await check_db_exists(async_connection=connection, dbname=db_name)
        if not is_db_exists:
            quoted_db_name = await connection.scalar(text("SELECT quote_ident(:db_name)"), {"db_name": db_name})
            await connection.execute(text(f"CREATE DATABASE {quoted_db_name}"))

    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield test_engine
    try:
        async with admin_engine.connect() as connection:
            if await check_db_exists(async_connection=connection, dbname=db_name):
                quoted_db_name = await connection.scalar(text("SELECT quote_ident(:db_name)"), {"db_name": db_name})
                await connection.execute(text(f"DROP DATABASE {quoted_db_name} WITH (FORCE)"))
    finally:
        await test_engine.dispose()
        await admin_engine.dispose()


@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def db_async_connection(async_test_database):
    """Создает сессию для каждого теста."""
    connection = await async_test_database.connect()

    yield connection

    await connection.close()


@pytest_asyncio.fixture(autouse=True)
async def truncate_all_tables(db_async_connection):
    """Очищает все таблицы перед каждым тестом и сбрасывает SEQUENCE."""
    table_names = [table.name for table in reversed(BaseModel.metadata.sorted_tables)]
    if table_names:
        joined = ", ".join(f'"{name}"' for name in table_names)
        await db_async_connection.execute(text(f"TRUNCATE {joined} RESTART IDENTITY CASCADE"))
    yield


@pytest_asyncio.fixture()
async def db_async_session(db_async_connection):
    """Создает сессию для каждого теста."""
    session = AsyncSession(bind=db_async_connection, expire_on_commit=False)

    yield session

    await session.rollback()
    await session.close()


@pytest.fixture
def mock_for_module(mocker):
    def with_args(module_name: str, function_name: str, *args, **kwargs) -> Mock:
        return mocker.patch(f"{module_name}.{function_name}", *args, **kwargs)

    return with_args


@pytest.fixture
def mocked_async_session(mocker: MockerFixture):
    session = mocker.MagicMock(spec=AsyncSession)
    mocked_async_session.add_all = mocker.Mock()
    mocked_async_session.commit = mocker.AsyncMock()
    mocked_async_session.close = mocker.AsyncMock()
    mocked_async_session.flush = mocker.AsyncMock()
    return session


@pytest.fixture
def mocked_api_client_session(mocker: MockerFixture):
    return mocker.patch("server.settings.db.AsyncSession")


@pytest.fixture
def api_base_url():
    return os.getenv("API_BASE_URL")


@pytest.fixture
def test_app(db_async_session):
    """
    Базовая настройка приложения.
    """
    app = FastAPI(title="News Parser")
    app.include_router(api_router)
    app.dependency_overrides[get_async_session] = lambda: db_async_session
    return app


@pytest.fixture
def api_client(api_base_url, test_app):
    return TestClient(base_url=api_base_url, app=test_app)


@pytest_asyncio.fixture()
def mock_for_async_session_generator(mocker, db_async_session):
    def with_args(module_name):
        mock_generator = mocker.MagicMock()
        mock_generator.return_value.__aenter__.return_value = db_async_session
        mock_generator.return_value.__aexit__.return_value = False
        mocker.patch(f"{module_name}.async_session_generator", new=mock_generator)
        return mock_generator

    return with_args


@pytest_asyncio.fixture()
def mock_for_optional_session_generator(mocker, db_async_session):
    def with_args(module_name):
        mock_generator = mocker.MagicMock()
        mock_generator.return_value.__aenter__.return_value = db_async_session
        mock_generator.return_value.__aexit__.return_value = False
        mocker.patch(f"{module_name}.optional_session_generator", new=mock_generator)
        return mock_generator

    return with_args


@pytest.fixture
def mock_for_optional_session_generator_with_fake_session(mocker):
    def with_args(module_name):
        mock_session = mocker.AsyncMock()
        mock_session.add = mocker.Mock()
        mock_session.flush = mocker.AsyncMock()
        mock_session.commit = mocker.AsyncMock()
        mock_generator = mocker.MagicMock()
        mock_generator.return_value.__aenter__.return_value = mock_session
        mock_generator.return_value.__aexit__.return_value = False
        mocker.patch(f"{module_name}.optional_session_generator", new=mock_generator)
        return mock_generator

    return with_args


@pytest.fixture
def mock_for_async_session_generator_with_fake_session(mocker):
    def with_args(module_name):
        mock_session = mocker.AsyncMock()
        mock_session.add = mocker.Mock()
        mock_session.flush = mocker.AsyncMock()
        mock_session.commit = mocker.AsyncMock()
        mock_generator = mocker.MagicMock()
        mock_generator.return_value.__aenter__.return_value = mock_session
        mock_generator.return_value.__aexit__.return_value = False
        mocker.patch(f"{module_name}.async_session_generator", new=mock_generator)
        return mock_generator

    return with_args
