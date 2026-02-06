from __future__ import annotations

from typing import TYPE_CHECKING

import pytest


if TYPE_CHECKING:
    from unittest.mock import Mock


MODULE_NAME = "src.apps.feature_flag.logic.interactors.feature_flag"


@pytest.fixture
def mocked__feature_flag__should_change_activated_at_on_update(mock_for_module) -> Mock:
    return mock_for_module(module_name=MODULE_NAME, function_name="feature_flag__should_change_activated_at_on_update")


@pytest.fixture
def mocked__datetime_now_with_server_tz(mock_for_module) -> Mock:
    return mock_for_module(module_name=MODULE_NAME, function_name="datetime_now_with_server_tz")


@pytest.fixture
def mocked__feature_flag__find_by_pk(mock_for_module) -> Mock:
    return mock_for_module(module_name=MODULE_NAME, function_name="feature_flag__find_by_pk")
