from __future__ import annotations

import pytest

from src.apps.feature_flag.dtos import FeatureFlagFilterDto, FeatureFlagListRequestDto
from src.apps.feature_flag.logic.facades.feature_flag import feature_flag__filter_dto
from src.apps.team.tests.factories_model import TeamFactory, TeamServiceFactory


@pytest.mark.parametrize("is_active", [True, False])
@pytest.mark.asyncio
async def test__feature_flag__filter_dto__is_active(
    mocked__team_service__find_by_name_or_raise, mocked__team__find_by_name_or_raise, mocked_async_session, is_active
):
    request_dto = FeatureFlagListRequestDto(is_active=is_active)
    expected_result = FeatureFlagFilterDto(is_active=is_active)

    test_result = await feature_flag__filter_dto(request_dto=request_dto, session=mocked_async_session)

    assert test_result == expected_result
    mocked__team_service__find_by_name_or_raise.assert_not_called()
    mocked__team__find_by_name_or_raise.assert_not_called()


@pytest.mark.asyncio
async def test__feature_flag__filter_dto__service_name(
    mocked__team_service__find_by_name_or_raise, mocked__team__find_by_name_or_raise, mocked_async_session
):
    team_service = TeamServiceFactory.build(name=" тестовый сервис ")
    mocked__team_service__find_by_name_or_raise.return_value = team_service
    request_dto = FeatureFlagListRequestDto(service_name=team_service.name)
    expected_result = FeatureFlagFilterDto(service_id=team_service.id)

    test_result = await feature_flag__filter_dto(request_dto=request_dto, session=mocked_async_session)

    assert test_result == expected_result
    mocked__team_service__find_by_name_or_raise.assert_called_once_with(
        name="ТЕСТОВЫЙ СЕРВИС", session=mocked_async_session
    )
    mocked__team__find_by_name_or_raise.assert_not_called()


@pytest.mark.asyncio
async def test__feature_flag__filter_dto__team_name(
    mocked__team_service__find_by_name_or_raise, mocked__team__find_by_name_or_raise, mocked_async_session
):
    team = TeamFactory.build(name=" тестовая команда ")
    mocked__team__find_by_name_or_raise.return_value = team
    request_dto = FeatureFlagListRequestDto(team_name=team.name)
    expected_result = FeatureFlagFilterDto(team_id=team.id)

    test_result = await feature_flag__filter_dto(request_dto=request_dto, session=mocked_async_session)

    assert test_result == expected_result
    mocked__team_service__find_by_name_or_raise.assert_not_called()
    mocked__team__find_by_name_or_raise.assert_called_once_with(name="ТЕСТОВАЯ КОМАНДА", session=mocked_async_session)


@pytest.mark.parametrize("is_active", [True, False])
@pytest.mark.asyncio
async def test__feature_flag__filter_dto__all_fields(
    mocked__team_service__find_by_name_or_raise, mocked__team__find_by_name_or_raise, mocked_async_session, is_active
):
    team_service = TeamServiceFactory.build(name=" тестовый сервис ")
    team = TeamFactory.build(name=" тестовая команда ")
    mocked__team_service__find_by_name_or_raise.return_value = team_service
    mocked__team__find_by_name_or_raise.return_value = team
    request_dto = FeatureFlagListRequestDto(is_active=is_active, service_name=team_service.name, team_name=team.name)
    expected_result = FeatureFlagFilterDto(is_active=is_active, service_id=team_service.id, team_id=team.id)

    test_result = await feature_flag__filter_dto(request_dto=request_dto, session=mocked_async_session)

    assert test_result == expected_result
    mocked__team_service__find_by_name_or_raise.assert_called_once_with(
        name="ТЕСТОВЫЙ СЕРВИС", session=mocked_async_session
    )
    mocked__team__find_by_name_or_raise.assert_called_once_with(name="ТЕСТОВАЯ КОМАНДА", session=mocked_async_session)
