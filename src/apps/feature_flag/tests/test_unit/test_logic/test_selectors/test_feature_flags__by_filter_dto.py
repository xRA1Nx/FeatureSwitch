from __future__ import annotations

from datetime import timedelta

import pytest

from src.apps.feature_flag.dtos import FeatureFlagFilterDto
from src.apps.feature_flag.logic.selectors.feature_flag import feature_flags__by_filter_dto
from src.apps.feature_flag.tests.factories_model import FeatureFlagFactory
from src.apps.team.tests.factories_model import TeamFactory, TeamServiceFactory
from src.utils.datetime import datetime_now_with_server_tz


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
    filter_dto = FeatureFlagFilterDto(
        is_active=is_active, service_id=expected_service.id, team_id=expected_team.id, is_expired=None
    )

    test_result = await feature_flags__by_filter_dto(filter_dto=filter_dto)

    assert len(test_result) == 1
    assert test_result[0] == expected_feature_flag
    mocked__optional_session_generator.assert_called_once_with(session=None)


@pytest.mark.asyncio
async def test__feature_flags__by_filter_dto_with_expired_true(mocked__optional_session_generator):
    """Фильтр is_expired=True возвращает только просроченные флаги"""
    team = await TeamFactory.create()
    service = await TeamServiceFactory.create(team=team)
    now = datetime_now_with_server_tz()
    expired_flag = await FeatureFlagFactory.create(
        team_service_id=service.id, is_active=True, activated_at=now - timedelta(days=10), ttl_days=5
    )
    await FeatureFlagFactory.create(team_service_id=service.id, is_active=True, activated_at=now, ttl_days=5)
    filter_dto = FeatureFlagFilterDto(is_expired=True, service_id=service.id, team_id=team.id)

    test_result = await feature_flags__by_filter_dto(filter_dto=filter_dto)

    assert len(test_result) == 1
    assert test_result[0] == expired_flag
    mocked__optional_session_generator.assert_called_with(session=None)


@pytest.mark.asyncio
async def test__feature_flags__by_filter_dto_with_expired_false(mocked__optional_session_generator):
    """Фильтр is_expired=False возвращает актуальные флаги (включая не активированные)"""
    team = await TeamFactory.create()
    service = await TeamServiceFactory.create(team=team)
    now = datetime_now_with_server_tz()
    actual_active_flag = await FeatureFlagFactory.create(
        team_service_id=service.id, is_active=True, activated_at=now, ttl_days=5
    )
    inactive_flag = await FeatureFlagFactory.create(
        team_service_id=service.id, is_active=False, activated_at=None, ttl_days=5
    )
    await FeatureFlagFactory.create(
        team_service_id=service.id, is_active=True, activated_at=now - timedelta(days=10), ttl_days=5
    )

    filter_dto = FeatureFlagFilterDto(is_expired=False, service_id=service.id, team_id=team.id)

    test_result = await feature_flags__by_filter_dto(filter_dto=filter_dto)

    assert len(test_result) == 2
    assert actual_active_flag in test_result
    assert inactive_flag in test_result
    mocked__optional_session_generator.assert_called_with(session=None)
