from __future__ import annotations

from logging import getLogger

from src.apps.user.logic.selectors.user import user__find_by_email
from src.apps.user.models import User
from src.server.db import async_session_generator
from src.utils.password import get_hashed_password


logger = getLogger(__name__)


async def admin_user__create(*, email: str, password: str) -> None:
    email = email.lower().strip()
    existing_user = await user__find_by_email(email=email)
    if existing_user:
        logger.warning(f"Cannot create admin user: User with email '{email}' already exists")
        return
    async with async_session_generator() as session:
        hashed_password = get_hashed_password(raw_password=password)
        user = User(hashed_password=hashed_password, email=email, is_admin=True)
        session.add(user)
        await session.commit()
        logger.info(f"Admin user successfully created: {email}")
