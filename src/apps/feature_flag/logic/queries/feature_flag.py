from __future__ import annotations

import datetime
import typing

from sqlalchemy import Select, select

from src.apps.feature_flag.models import FeatureFlag
from src.apps.team.models import TeamService
from src.utils.sql_alchemy import make_interval


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


def feature_flags_q__is_actual(
    *, now: datetime.datetime, query: Select[tuple[FeatureFlag]] | None = None
) -> Select[tuple[FeatureFlag]]:
    """
    - Если activated_at IS NULL → считается актуальным (TTL не начался)
    - Если activated_at IS NOT NULL → актуален пока activated_at + ttl_days > now
    """
    if query is None:
        query = feature_flags_q__all()

    expiration_date = FeatureFlag.activated_at + make_interval(days=FeatureFlag.ttl_days)

    return query.filter((FeatureFlag.activated_at.is_(None)) | (expiration_date > now))


def feature_flags_q__is_expired(
    *, now: datetime.datetime, query: Select[tuple[FeatureFlag]] | None = None
) -> Select[tuple[FeatureFlag]]:
    """
    activated_at IS NOT NULL AND activated_at + ttl_days <= now
    """
    if query is None:
        query = feature_flags_q__all()

    query = query.filter(FeatureFlag.activated_at.is_not(None))
    expiration_date = FeatureFlag.activated_at + make_interval(days=FeatureFlag.ttl_days)

    return query.filter(expiration_date <= now)


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


def feature_flags__by_team_ids(
    *, team_ids: list[int], query: Select[tuple[FeatureFlag]] | None = None
) -> Select[tuple[FeatureFlag]]:
    if query is None:
        query = feature_flags_q__all()
    return query.join(FeatureFlag.team_service).filter(TeamService.team_id.in_(team_ids))
