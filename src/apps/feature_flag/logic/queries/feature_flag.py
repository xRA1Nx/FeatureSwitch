from sqlalchemy import Select, select

from src.apps.feature_flag.models import FeatureFlag


def feature_flag_q__all() -> Select[tuple[FeatureFlag]]:
    return select(FeatureFlag)


def feature_flag_q__by_pk(
    *, pk: int, query: Select[tuple[FeatureFlag]] | None = None
) -> Select[tuple[FeatureFlag]]:
    if query is None:
        query = feature_flag_q__all()
    return query.filter(FeatureFlag.id == pk).limit(1)
