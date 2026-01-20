from __future__ import annotations

import pytest
from app.health.dtos import HealthCheckErrorDto, HealthCheckIsReadyResponseDto
from app.health.enums import HealthCheckReason
from app.health.tests.factories_dto import HealthCheckErrorDtoFactory


@pytest.mark.asyncio
async def test__ready__200__no_errors(api_client, mocked__app__readiness_result):
    expected_readiness_result = HealthCheckIsReadyResponseDto(is_ok=True, errors=[])
    mocked__app__readiness_result.return_value = expected_readiness_result
    expected_content = b'{"status":"ok"}'

    response = api_client.get("/api/ready")

    assert response.status_code == 200
    assert response.content == expected_content
    mocked__app__readiness_result.assert_called_once_with()


@pytest.mark.asyncio
async def test__ready__200__errors(api_client, mocked__app__readiness_result):
    error_dto = HealthCheckErrorDtoFactory.build()
    expected_readiness_result = HealthCheckIsReadyResponseDto(is_ok=True, errors=[error_dto])
    mocked__app__readiness_result.return_value = expected_readiness_result
    expected_content = b'{"status":"ok"}'

    response = api_client.get("/api/ready")

    assert response.status_code == 200
    assert response.content == expected_content
    mocked__app__readiness_result.assert_called_once_with()


@pytest.mark.asyncio
async def test__ready__500(api_client, mocked__app__readiness_result):
    error_dto = HealthCheckErrorDto(reason=HealthCheckReason.KAFKA, message="kafka trouble")
    expected_readiness_result = HealthCheckIsReadyResponseDto(is_ok=False, errors=[error_dto])
    mocked__app__readiness_result.return_value = expected_readiness_result
    expected_content = b'[{"reason":"KAFKA","message":"kafka trouble"}]'

    response = api_client.get("/api/ready")

    assert response.status_code == 503
    assert response.content == expected_content
    mocked__app__readiness_result.assert_called_once_with()
