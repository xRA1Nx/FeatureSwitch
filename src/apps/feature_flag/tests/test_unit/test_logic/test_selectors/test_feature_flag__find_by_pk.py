from __future__ import annotations

import pytest

from src.apps.feature_flag.logic.selectors.feature_flag import feature_flag__find_by_pk


@pytest.mark.asyncio
async def test__feature_flag__find_by_pk(mocked__optional_session_generator, feature_flag__factory):
    expected_instance = await feature_flag__factory()
    await feature_flag__factory()

    test_result = await feature_flag__find_by_pk(pk=expected_instance.id)

    assert test_result == expected_instance
    mocked__optional_session_generator.assert_called_once_with(session=None)
