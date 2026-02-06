from __future__ import annotations

import datetime

import pytest

from src.apps.feature_flag.logic.interactors.feature_flag import feature_flag__activated_at_on_changes
from src.apps.feature_flag.tests.factories_dto import FeatureFlagUpdateDtoFactory
from src.apps.feature_flag.tests.factories_model import FeatureFlagFactory


def test__feature_flag__activated_at_on_changes__should_not_change(
    mocked__feature_flag__should_change_activated_at_on_update, mocked__datetime_now_with_server_tz
):
    activated_at = datetime.datetime(year=2020, month=1, day=2, hour=3, minute=4)
    mocked__feature_flag__should_change_activated_at_on_update.return_value = False
    current_feature_flag = FeatureFlagFactory.build(activated_at=activated_at)
    update_dto = FeatureFlagUpdateDtoFactory.build()

    test_result = feature_flag__activated_at_on_changes(
        current_feature_flag=current_feature_flag, update_dto=update_dto
    )

    assert test_result == activated_at
    mocked__feature_flag__should_change_activated_at_on_update.assert_called_once_with(
        current_feature_flag=current_feature_flag, update_dto=update_dto
    )
    mocked__datetime_now_with_server_tz.assert_not_called()


def test__feature_flag__activated_at_on_changes__set_new_value(
    mocked__feature_flag__should_change_activated_at_on_update, mocked__datetime_now_with_server_tz
):
    activated_at = datetime.datetime(year=2020, month=1, day=2, hour=3, minute=4)
    mocked__feature_flag__should_change_activated_at_on_update.return_value = True
    current_feature_flag = FeatureFlagFactory.build(activated_at=activated_at, is_active=False)
    update_dto = FeatureFlagUpdateDtoFactory.build(is_active=True)

    test_result = feature_flag__activated_at_on_changes(
        current_feature_flag=current_feature_flag, update_dto=update_dto
    )

    assert test_result == mocked__datetime_now_with_server_tz.return_value
    mocked__feature_flag__should_change_activated_at_on_update.assert_called_once_with(
        current_feature_flag=current_feature_flag, update_dto=update_dto
    )
    mocked__datetime_now_with_server_tz.assert_called_with()


@pytest.mark.parametrize(("updated_is_active", "current_is_active"), [(False, True), (True, True), (False, False)])
def test__feature_flag__activated_at_on_changes__reset_to_none(
    mocked__feature_flag__should_change_activated_at_on_update,
    mocked__datetime_now_with_server_tz,
    updated_is_active,
    current_is_active,
):
    activated_at = datetime.datetime(year=2020, month=1, day=2, hour=3, minute=4)
    mocked__feature_flag__should_change_activated_at_on_update.return_value = True
    current_feature_flag = FeatureFlagFactory.build(activated_at=activated_at, is_active=current_is_active)
    update_dto = FeatureFlagUpdateDtoFactory.build(is_active=updated_is_active)

    test_result = feature_flag__activated_at_on_changes(
        current_feature_flag=current_feature_flag, update_dto=update_dto
    )

    assert test_result is None
    mocked__feature_flag__should_change_activated_at_on_update.assert_called_once_with(
        current_feature_flag=current_feature_flag, update_dto=update_dto
    )
    mocked__datetime_now_with_server_tz.assert_not_called()
