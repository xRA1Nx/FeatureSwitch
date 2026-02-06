from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.team.logic.queries.team import teams_q__by_name
from src.apps.team.models import Team
from src.server.db import optional_session_generator


async def team__find_by_name(*, name: str | None = None, session: AsyncSession | None = None) -> Team | None:
    if name is None:
        return None
    query = teams_q__by_name(name=name)
    async with optional_session_generator(session=session) as async_session:
        scalars = await async_session.scalars(query)
        return scalars.one_or_none()
