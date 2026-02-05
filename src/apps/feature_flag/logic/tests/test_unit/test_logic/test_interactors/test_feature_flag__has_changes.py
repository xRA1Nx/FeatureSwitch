from __future__ import annotations

import pytest

from src.apps.feature_flag.logic.interactors.feature_flag import feature_flag__has_changes
from src.apps.feature_flag.logic.tests.factories_dto import FeatureFlagUpdateDtoFactory
from src.apps.feature_flag.logic.tests.factories_model import FeatureFlagFactory


@pytest.mark.parametrize(
    ("current_is_active", "updated_is_active", "current_ttl_days", "updated_ttl_days", "expected_result"),
    [
        (True, True, 14, 14, False),
        (False, False, 30, 30, False),
        (True, False, 14, 14, True),
        (False, True, 30, 30, True),
        (True, True, 14, 30, True),
        (False, False, 30, 14, True),
        (True, False, 14, 30, True),
        (False, True, 30, 14, True),
        (True, True, None, None, False),
        (True, True, 14, None, True),
        (True, True, None, 14, True),
        (True, True, 0, 0, False),
        (True, True, 0, 1, True),
        (True, True, 1, 0, True),
    ],
)
def test__feature_flag__has_changes(
    current_is_active, updated_is_active, current_ttl_days, updated_ttl_days, expected_result
):
    current_feature_flag = FeatureFlagFactory.build(is_active=current_is_active, ttl_days=current_ttl_days)
    update_dto = FeatureFlagUpdateDtoFactory.build(is_active=updated_is_active, ttl_days=updated_ttl_days)

    test_result = feature_flag__has_changes(current_feature_flag=current_feature_flag, update_dto=update_dto)

    assert test_result == expected_result
