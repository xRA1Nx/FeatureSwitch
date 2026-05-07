from __future__ import annotations

import unittest.mock

import pytest

from src.apps.feature_flag.dtos import FeatureFlagDto
from src.apps.feature_flag.tests.factories_dto import FeatureFlagDtoFactory, FeatureFlagListRequestDtoFactory


@pytest.mark.asyncio
async def test__feature_flags_list__api(api_client, mocked__feature_flags__list):
    request_dto = FeatureFlagListRequestDtoFactory.build(
        is_active=True, team_name="team_name", service_name="service_name", name="name"
    )
    expected_dto = FeatureFlagDtoFactory.build()
    mocked__feature_flags__list.return_value = [expected_dto]

    response = api_client.get("/api/v1/feature_flags", params=request_dto.model_dump())
    test_result = [FeatureFlagDto(**response.json()[0])]

    assert response.status_code == 200

    assert test_result == [expected_dto]
    mocked__feature_flags__list.assert_called_once_with(request_dto=request_dto, session=unittest.mock.ANY)
