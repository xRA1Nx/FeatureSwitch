from __future__ import annotations

from typing import TYPE_CHECKING

import pytest


if TYPE_CHECKING:
    from unittest.mock import Mock

MODULE_NAME = "src.apps.feature_flag.views"


@pytest.fixture
def mocked__feature_flags__list(mock_for_module) -> Mock:
    return mock_for_module(module_name=MODULE_NAME, function_name="feature_flags__list")
