from __future__ import annotations

import pytest

from src.apps.feature_flag.dtos import FeatureFlagDto
from src.apps.feature_flag.logic.facades.feature_flag import feature_flags__retrieve


@pytest.mark.asyncio
async def test__feature_flags__retrieve(
    mocked__feature_flag__find_by_pk_or_raise, mocked__instance_to_dto, mocked_async_session
):
    pk = 100500

    test_result = await feature_flags__retrieve(pk=pk, session=mocked_async_session)

    assert test_result == mocked__instance_to_dto.return_value
    mocked__feature_flag__find_by_pk_or_raise.assert_called_once_with(pk=pk, session=mocked_async_session)
    mocked__instance_to_dto.assert_called_once_with(
        instance=mocked__feature_flag__find_by_pk_or_raise.return_value, dto_class=FeatureFlagDto
    )
