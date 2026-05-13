from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.user.logic.queries.user import users_q__by_email
from src.apps.user.models import User
from src.server.db import optional_session_generator


async def user__find_by_email(*, email: str, session: AsyncSession | None = None) -> User | None:
    query = users_q__by_email(email=email)
    async with optional_session_generator(session=session) as async_session:
        scalars = await async_session.scalars(query)
        return scalars.one_or_none()
