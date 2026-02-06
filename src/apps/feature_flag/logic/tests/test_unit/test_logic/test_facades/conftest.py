from __future__ import annotations

from typing import TYPE_CHECKING

import pytest


if TYPE_CHECKING:
    from unittest.mock import Mock


MODULE_NAME = "src.apps.feature_flag.logic.facades.feature_flag"


@pytest.fixture
def mocked__feature_flag__find_by_pk_or_raise(mock_for_module) -> Mock:
    return mock_for_module(module_name=MODULE_NAME, function_name="feature_flag__find_by_pk_or_raise")


@pytest.fixture
def mocked__feature_flag__has_changes(mock_for_module) -> Mock:
    return mock_for_module(module_name=MODULE_NAME, function_name="feature_flag__has_changes")


@pytest.fixture
def mocked__feature_flag__activated_at_on_changes(mock_for_module) -> Mock:
    return mock_for_module(module_name=MODULE_NAME, function_name="feature_flag__activated_at_on_changes")
