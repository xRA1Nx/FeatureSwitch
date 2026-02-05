from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.feature_flag.logic.queries.feature_flag import feature_flag_q__by_pk
from src.apps.feature_flag.models import FeatureFlag
from src.server.db import optional_session_generator


async def feature_flag__find_by_pk(*, pk: int, session: AsyncSession | None = None) -> FeatureFlag | None:
    query = feature_flag_q__by_pk(pk=pk)
    async with optional_session_generator(session=session) as async_session:
        scalars = await async_session.scalars(query)
        return scalars.one_or_none()
