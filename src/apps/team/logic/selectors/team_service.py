from __future__ import annotations

import typing

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.team.logic.queries.team_service import team_services_q__by_name, team_services_q__by_team_id
from src.apps.team.models import TeamService
from src.server.db import optional_session_generator


async def team_service__find_by_name(
    *, name: str | None = None, session: AsyncSession | None = None
) -> TeamService | None:
    if name is None:
        return None
    query = team_services_q__by_name(name=name)
    async with optional_session_generator(session=session) as async_session:
        scalars = await async_session.scalars(query)
        return scalars.one_or_none()


async def team_services__by_team_id(
    *, team_id: int, session: AsyncSession | None = None
) -> typing.Sequence[TeamService]:
    query = team_services_q__by_team_id(team_id=team_id)
    async with optional_session_generator(session=session) as async_session:
        scalars = await async_session.scalars(query)
        return scalars.all()
