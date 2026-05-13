from __future__ import annotations

from sqlalchemy import Select, select

from src.apps.user.models import User


def users_q__all() -> Select[tuple[User]]:
    return select(User)


def users_q__by_pk(*, pk: int, query: Select[tuple[User]] | None = None) -> Select[tuple[User]]:
    if query is None:
        query = users_q__all()
    return query.filter(User.id == pk)


def users_q__by_email(*, email: str, query: Select[tuple[User]] | None = None) -> Select[tuple[User]]:
    if query is None:
        query = users_q__all()
    return query.filter(User.email == email)
