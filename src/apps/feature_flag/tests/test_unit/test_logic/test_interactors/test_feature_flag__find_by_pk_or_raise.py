from __future__ import annotations

import pytest

from src.apps.common.exceptions import BusinessLogicException
from src.apps.feature_flag.logic.interactors.feature_flag import feature_flag__find_by_pk_or_raise


@pytest.mark.asyncio
async def test__feature_flag__find_by_pk_or_raise__happy_path(mocked__feature_flag__find_by_pk, mocked_async_session):
    pk = 100500

    test_result = await feature_flag__find_by_pk_or_raise(session=mocked_async_session, pk=pk)

    assert test_result == mocked__feature_flag__find_by_pk.return_value
    mocked__feature_flag__find_by_pk.assert_called_with(session=mocked_async_session, pk=pk)


@pytest.mark.asyncio
async def test__feature_flag__find_by_pk_or_raise__error(mocked__feature_flag__find_by_pk, mocked_async_session):
    pk = 100500
    mocked__feature_flag__find_by_pk.return_value = None

    with pytest.raises(
        expected_exception=BusinessLogicException,
        match="Данная операция не возможна. не существует FeatureFlag с id=100500",
    ):
        await feature_flag__find_by_pk_or_raise(session=mocked_async_session, pk=pk)
    mocked__feature_flag__find_by_pk.assert_called_with(session=mocked_async_session, pk=pk)
