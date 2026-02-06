from __future__ import annotations

import typing

from sqlalchemy import Select, select

from src.apps.feature_flag.models import FeatureFlag


def feature_flags_q__all() -> Select[tuple[FeatureFlag]]:
    return select(FeatureFlag)


def feature_flags_q__by_pk(*, pk: int, query: Select[tuple[FeatureFlag]] | None = None) -> Select[tuple[FeatureFlag]]:
    if query is None:
        query = feature_flags_q__all()
    return query.filter(FeatureFlag.id == pk)


def feature_flags_q__by_is_active(
    *, is_active: bool, query: Select[tuple[FeatureFlag]] | None = None
) -> Select[tuple[FeatureFlag]]:
    if query is None:
        query = feature_flags_q__all()
    return query.filter(FeatureFlag.is_active == is_active)


def feature_flags_q__by_names(
    *, names: typing.Sequence[str], query: Select[tuple[FeatureFlag]] | None = None
) -> Select[tuple[FeatureFlag]]:
    if query is None:
        query = feature_flags_q__all()
    return query.filter(FeatureFlag.name.in_(names))



def feature_flags__by_team_service_ids(
    *, service_ids: list[int], query: Select[tuple[FeatureFlag]] | None = None
) -> Select[tuple[FeatureFlag]]:
    if query is None:
        query = feature_flags_q__all()
    return query.filter(FeatureFlag.team_service_id.in_(service_ids))