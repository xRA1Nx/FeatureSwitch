from __future__ import annotations

from sqlalchemy import Select, select

from src.apps.team.models import TeamService


def team_services_q__all() -> Select[tuple[TeamService]]:
    return select(TeamService)


def team_services_q__by_pk(*, pk: int, query: Select[tuple[TeamService]] | None = None) -> Select[tuple[TeamService]]:
    if query is None:
        query = team_services_q__all()
    return query.filter(TeamService.id == pk)


def team_services_q__by_name(
    *, name: str, query: Select[tuple[TeamService]] | None = None
) -> Select[tuple[TeamService]]:
    if query is None:
        query = team_services_q__all()
    return query.filter(TeamService.name == name)


def team_services_q__by_team_id(
    *, team_id: int, query: Select[tuple[TeamService]] | None = None
) -> Select[tuple[TeamService]]:
    if query is None:
        query = team_services_q__all()
    return query.filter(TeamService.team_id == team_id)
