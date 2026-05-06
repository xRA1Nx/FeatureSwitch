from __future__ import annotations

import unittest.mock

import pytest

from src.apps.feature_flag.dtos import FeatureFlagDto
from src.apps.feature_flag.tests.factories_dto import FeatureFlagDtoFactory


@pytest.mark.asyncio
async def test__feature_flags_retrieve__api(api_client, mocked__feature_flags__retrieve):
    expected_pk = 100500
    expected_dto = FeatureFlagDtoFactory.build(id=expected_pk)
    mocked__feature_flags__retrieve.return_value = expected_dto

    response = api_client.get(f"/api/v1/feature_flags/{expected_pk}")
    test_result = FeatureFlagDto(**response.json())

    assert response.status_code == 200

    assert test_result == expected_dto
    mocked__feature_flags__retrieve.assert_called_once_with(pk=expected_pk, session=unittest.mock.ANY)
