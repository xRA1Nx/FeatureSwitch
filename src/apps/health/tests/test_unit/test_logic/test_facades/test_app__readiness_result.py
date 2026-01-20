from __future__ import annotations

import pytest
from app.health.dtos import HealthCheckIsReadyResponseDto
from app.health.logic.facades import app__readiness_result
from app.health.tests.factories_dto import HealthCheckErrorDtoFactory


@pytest.mark.asyncio
async def test__app__readiness_result__no_errors(mocked__get_db_health_errors):
    mocked__get_db_health_errors.return_value = []
    expected_result = HealthCheckIsReadyResponseDto(is_ok=True, errors=[])

    test_result = await app__readiness_result()

    assert test_result == expected_result
    mocked__get_db_health_errors.assert_called_once_with()


@pytest.mark.asyncio
async def test__app__readiness_result__errors(mocked__get_db_health_errors):
    error_dto = HealthCheckErrorDtoFactory.build()
    mocked__get_db_health_errors.return_value = [error_dto]
    expected_result = HealthCheckIsReadyResponseDto(is_ok=False, errors=[error_dto])

    test_result = await app__readiness_result()

    assert test_result == expected_result
    mocked__get_db_health_errors.assert_called_once_with()
