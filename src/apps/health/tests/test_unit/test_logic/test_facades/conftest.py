from __future__ import annotations

import typing
from unittest.mock import Mock

import pytest


MODULE_NAME = "src.apps.health.logic.facades"

if typing.TYPE_CHECKING:
    from unittest.mock import Mock


@pytest.fixture
def mocked__get_db_health_errors(mock_for_module) -> Mock:
    return mock_for_module(module_name=MODULE_NAME, function_name="get_db_health_errors")
