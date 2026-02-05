from __future__ import annotations

from src.apps.team.models import Team, TeamService
from src.utils.testing import BaseSqlAlchemyFactory, FactoryBuilderMixin


class TeamFactory(BaseSqlAlchemyFactory, FactoryBuilderMixin):
    __model__ = Team


class TeamServiceFactory(BaseSqlAlchemyFactory, FactoryBuilderMixin):
    __model__ = TeamService
