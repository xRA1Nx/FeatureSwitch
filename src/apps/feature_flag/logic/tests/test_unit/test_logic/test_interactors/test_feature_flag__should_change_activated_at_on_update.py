from __future__ import annotations

import datetime

import pytest

from src.apps.feature_flag.logic.interactors.feature_flag import feature_flag__should_change_activated_at_on_update
from src.apps.feature_flag.logic.tests.factories_dto import FeatureFlagUpdateDtoFactory
from src.apps.feature_flag.logic.tests.factories_model import FeatureFlagFactory


@pytest.mark.parametrize(
    ("current_is_active", "updated_is_active", "activated_at", "expected_result"),
    [
        (True, True, datetime.datetime.now(), False),
        (True, False, datetime.datetime.now(), True),
        (False, True, datetime.datetime.now(), True),
        (False, False, datetime.datetime.now(), True),
        (True, True, None, True),
        (True, False, None, True),
        (False, True, None, True),
        (False, False, None, True),
    ],
)
def test__feature_flag__should_change_activated_at_on_update(
    current_is_active, updated_is_active, activated_at, expected_result
):
    current_feature_flag = FeatureFlagFactory.build(is_active=current_is_active, activated_at=activated_at)
    update_dto = FeatureFlagUpdateDtoFactory.build(is_active=updated_is_active)

    test_result = feature_flag__should_change_activated_at_on_update(
        current_feature_flag=current_feature_flag, update_dto=update_dto
    )

    assert test_result == expected_result
