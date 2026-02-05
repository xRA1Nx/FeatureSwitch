from __future__ import annotations

from sqlalchemy import Select, select

from src.apps.team.models import Team


def teams_q__all() -> Select[tuple[Team]]:
    return select(Team)


def teams_q__by_pk(*, pk: int, query: Select[tuple[Team]] | None = None) -> Select[tuple[Team]]:
    if query is None:
        query = teams_q__all()
    return query.filter(Team.id == pk)


def teams_q__by_name(*, name: str, query: Select[tuple[Team]] | None = None) -> Select[tuple[Team]]:
    if query is None:
        query = teams_q__all()
    return query.filter(Team.name == name)
