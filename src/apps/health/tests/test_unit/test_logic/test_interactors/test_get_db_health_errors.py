from __future__ import annotations

import pytest
from asyncpg import PostgresConnectionError
from pytest_mock import MockerFixture
from sqlalchemy.exc import SQLAlchemyError

from src.apps.health.dtos import HealthCheckErrorDto
from src.apps.health.enums import HealthCheckReason
from src.apps.health.logic.interactors import get_db_health_errors


@pytest.mark.asyncio
async def test__get_db_health_errors__no_errors():
    test_results = await get_db_health_errors()

    assert test_results == []


@pytest.mark.asyncio
async def test__get_db_health_errors__connection_error(mocked__get_async_engine, mocker: MockerFixture):
    mocked_connect = mocker.AsyncMock()
    mocked_execute = mocker.AsyncMock()
    mocked_result = mocker.AsyncMock()
    mocked_fetchone = mocker.Mock()
    mocked_result.fetchone = mocked_fetchone
    mocked_execute.return_value = mocked_result
    mocked_execute.side_effect = PostgresConnectionError("connection_error")
    mocked_connect.__aenter__.return_value.execute = mocked_execute
    mocked__get_async_engine.return_value.connect.return_value = mocked_connect

    expected_dto = HealthCheckErrorDto(
        reason=HealthCheckReason.DATABASE, message="Ошибка подключения к PostgreSQL: connection_error"
    )

    test_results = await get_db_health_errors()

    assert test_results == [expected_dto]
    mocked__get_async_engine.assert_called_once_with()
    mocked__get_async_engine.return_value.connect.assert_called_once()
    mocked_connect.__aenter__.assert_called_once()
    mocked_execute.assert_called_once_with(mocker.ANY)
    mocked_fetchone.assert_not_called()


@pytest.mark.asyncio
async def test__get_db_health_errors__sql_alchemy_error(mocked__get_async_engine, mocker: MockerFixture):
    mocked_connect = mocker.AsyncMock()
    mocked_execute = mocker.AsyncMock()
    mocked_result = mocker.AsyncMock()
    mocked_fetchone = mocker.Mock()
    mocked_result.fetchone = mocked_fetchone
    mocked_execute.return_value = mocked_result
    mocked_execute.side_effect = SQLAlchemyError("sql_alchemy_error")
    mocked_connect.__aenter__.return_value.execute = mocked_execute
    mocked__get_async_engine.return_value.connect.return_value = mocked_connect

    expected_dto = HealthCheckErrorDto(
        reason=HealthCheckReason.DATABASE, message="Ошибка SQLAlchemy: sql_alchemy_error"
    )

    test_results = await get_db_health_errors()

    assert test_results == [expected_dto]
    mocked__get_async_engine.assert_called_once_with()
    mocked__get_async_engine.return_value.connect.assert_called_once()
    mocked_connect.__aenter__.assert_called_once()
    mocked_execute.assert_called_once_with(mocker.ANY)
    mocked_fetchone.assert_not_called()


@pytest.mark.parametrize("error_class", [ValueError, TypeError, OSError])
@pytest.mark.asyncio
async def test__get_db_health_errors__unexpected_error(mocked__get_async_engine, mocker: MockerFixture, error_class):
    error = error_class("unexpected_error")
    mocked_connect = mocker.AsyncMock()
    mocked_execute = mocker.AsyncMock()
    mocked_result = mocker.AsyncMock()
    mocked_fetchone = mocker.Mock()
    mocked_result.fetchone = mocked_fetchone
    mocked_execute.return_value = mocked_result
    mocked_execute.side_effect = error
    mocked_connect.__aenter__.return_value.execute = mocked_execute
    mocked__get_async_engine.return_value.connect.return_value = mocked_connect

    expected_dto = HealthCheckErrorDto(
        reason=HealthCheckReason.DATABASE,
        message="Неизвестная ошибка при проверке подключения к Postgres: unexpected_error",
    )

    test_results = await get_db_health_errors()

    assert test_results == [expected_dto]
    mocked__get_async_engine.assert_called_once_with()
    mocked__get_async_engine.return_value.connect.assert_called_once()
    mocked_connect.__aenter__.assert_called_once()
    mocked_execute.assert_called_once_with(mocker.ANY)
    mocked_fetchone.assert_not_called()
