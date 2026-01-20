from __future__ import annotations

from typing import TYPE_CHECKING

import pytest


if TYPE_CHECKING:
    from unittest.mock import Mock

MODULE_NAME = "src.apps.health.views"


@pytest.fixture
def mocked__app__is_healthy(mock_for_module) -> Mock:
    return mock_for_module(module_name=MODULE_NAME, function_name="app__is_healthy")


@pytest.fixture
def mocked__app__readiness_result(mock_for_module) -> Mock:
    return mock_for_module(module_name=MODULE_NAME, function_name="app__readiness_result")
