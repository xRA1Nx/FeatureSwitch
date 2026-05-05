from __future__ import annotations

import pytest

from src.apps.feature_flag.dtos import FeatureFlagFilterDto
from src.apps.feature_flag.logic.selectors.feature_flag import feature_flags__by_filter_list_dto
from src.apps.feature_flag.tests.factories_model import FeatureFlagFactory
from src.apps.team.tests.factories_model import TeamFactory, TeamServiceFactory


@pytest.mark.parametrize("is_active", [True, False])
@pytest.mark.asyncio
async def test__feature_flags__by_filter_dto(mocked__optional_session_generator, is_active):
    expected_team = await TeamFactory.create()
    not_expected_team = await TeamFactory.create()
    expected_service = await TeamServiceFactory.create(team=expected_team)
    not_expected_team_service = await TeamServiceFactory.create(team=not_expected_team)
    expected_feature_flag = await FeatureFlagFactory.create(team_service_id=expected_service.id, is_active=is_active)
    await FeatureFlagFactory.create(team_service_id=not_expected_team_service.id, is_active=is_active)
    await FeatureFlagFactory.create(team_service_id=expected_service.id, is_active=not is_active)
    filter_dto = FeatureFlagFilterDto(is_active=is_active, service_id=expected_service.id, team_id=expected_team.id)

    test_result = await feature_flags__by_filter_list_dto(filter_dto=filter_dto)

    assert len(test_result) == 1
    assert test_result[0] == expected_feature_flag
    mocked__optional_session_generator.assert_called_once_with(session=None)
