from __future__ import annotations

import pytest

from src.apps.feature_flag.logic.facades.feature_flag import feature_flag__prepare_for_admin_update
from src.apps.feature_flag.tests.factories_dto import FeatureFlagUpdateDtoFactory
from src.apps.feature_flag.tests.factories_model import FeatureFlagFactory


@pytest.mark.asyncio
async def test__feature_flag__prepare_for_admin_update__has_changes(
    mocked__feature_flag__find_by_pk_or_raise,
    mocked__feature_flag__has_changes,
    mocked__feature_flag__activated_at_on_changes,
):
    updated_feature_flag = FeatureFlagFactory.build()
    update_dto = FeatureFlagUpdateDtoFactory.build()
    mocked__feature_flag__has_changes.return_value = True

    test_result = await feature_flag__prepare_for_admin_update(
        update_dto=update_dto, updated_feature_flag=updated_feature_flag
    )

    assert test_result == updated_feature_flag
    assert test_result.activated_at == mocked__feature_flag__activated_at_on_changes.return_value
    mocked__feature_flag__find_by_pk_or_raise.assert_called_once_with(pk=updated_feature_flag.id)
    mocked__feature_flag__has_changes.assert_called_once_with(
        update_dto=update_dto, current_feature_flag=mocked__feature_flag__find_by_pk_or_raise.return_value
    )
    mocked__feature_flag__activated_at_on_changes.assert_called_once_with(
        current_feature_flag=mocked__feature_flag__find_by_pk_or_raise.return_value, update_dto=update_dto
    )


@pytest.mark.asyncio
async def test__feature_flag__prepare_for_admin_update__no_changes(
    mocked__feature_flag__find_by_pk_or_raise,
    mocked__feature_flag__has_changes,
    mocked__feature_flag__activated_at_on_changes,
):
    updated_feature_flag = FeatureFlagFactory.build()
    update_dto = FeatureFlagUpdateDtoFactory.build()
    mocked__feature_flag__has_changes.return_value = False

    test_result = await feature_flag__prepare_for_admin_update(
        update_dto=update_dto, updated_feature_flag=updated_feature_flag
    )

    assert test_result is None
    mocked__feature_flag__find_by_pk_or_raise.assert_called_once_with(pk=updated_feature_flag.id)
    mocked__feature_flag__has_changes.assert_called_once_with(
        update_dto=update_dto, current_feature_flag=mocked__feature_flag__find_by_pk_or_raise.return_value
    )
    mocked__feature_flag__activated_at_on_changes.assert_not_called()
