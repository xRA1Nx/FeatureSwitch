from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from src.server.settings import Settings, get_settings


if TYPE_CHECKING:
    from unittest.mock import Mock


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture
def mock_for_module(mocker):
    def with_args(module_name: str, function_name: str, *args, **kwargs) -> Mock:
        return mocker.patch(f"{module_name}.{function_name}", *args, **kwargs)

    return with_args


@pytest.fixture
def api_base_url():
    return os.getenv("API_BASE_URL")
