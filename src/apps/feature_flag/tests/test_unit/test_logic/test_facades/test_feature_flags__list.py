from __future__ import annotations

import pytest

from src.apps.feature_flag.dtos import FeatureFlagListItemDto
from src.apps.feature_flag.logic.facades.feature_flag import feature_flags__list
from src.apps.feature_flag.tests.factories_dto import FeatureFlagListRequestDtoFactory


@pytest.mark.asyncio
async def test__feature_flags__list(
    mocked__optional_session_generator,
    mocked__feature_flag__filter_dto,
    mocked__feature_flags__by_filter_list_dto,
    mocked__instances_to_dtos,
    mocked_async_session,
):
    request_dto = FeatureFlagListRequestDtoFactory.build()
    async_session = mocked__optional_session_generator.return_value.__aenter__.return_value

    test_result = await feature_flags__list(request_dto=request_dto, session=mocked_async_session)

    assert test_result == mocked__instances_to_dtos.return_value
    mocked__optional_session_generator.assert_called_once_with(session=mocked_async_session)
    mocked__feature_flag__filter_dto.assert_called_once_with(session=async_session, request_dto=request_dto)
    mocked__feature_flags__by_filter_list_dto.assert_called_once_with(
        filter_dto=mocked__feature_flag__filter_dto.return_value, session=async_session
    )
    mocked__instances_to_dtos.assert_called_once_with(
        instances=mocked__feature_flags__by_filter_list_dto.return_value, dto_class=FeatureFlagListItemDto
    )
