from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from src.apps.feature_flag.logic.tests.factories_model import FeatureFlagFactory
from src.apps.team.models import TeamService
from src.apps.team.tests.factories_model import TeamFactory, TeamServiceFactory


if TYPE_CHECKING:
    from unittest.mock import Mock

MODULE_NAME = "src.apps.feature_flag.logic.selectors.feature_flag"


@pytest.fixture
def mocked__optional_session_generator(mock_for_optional_session_generator) -> Mock:
    return mock_for_optional_session_generator(module_name=MODULE_NAME)


@pytest.fixture
async def feature_flag__factory():
    async def _feature_flag_factory(team_service: TeamService | None = None, **kwargs):
        if not team_service:
            team = await TeamFactory.create()
            team_service = await TeamServiceFactory.create(team_id=team.id)
        kwargs["team_service_id"] = team_service.id
        return await FeatureFlagFactory.create(**kwargs)

    return _feature_flag_factory
