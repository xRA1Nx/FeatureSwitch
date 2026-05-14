from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.common.exceptions import BusinessLogicException
from src.apps.user.logic.selectors.user import user__find_by_email
from src.apps.user.models import User


async def user__find_by_email_or_raise(*, email: str, session: AsyncSession | None = None) -> User:
    user = await user__find_by_email(email=email, session=session)
    if not user:
        raise BusinessLogicException(f'Не существует пользователя с данным email="{email}"')
    return user
