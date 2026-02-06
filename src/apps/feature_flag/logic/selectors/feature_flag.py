from __future__ import annotations

import typing
from tarfile import data_filter

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.feature_flag.dtos import FeatureFlagListRequestDto, FeatureFlagFilterDto
from src.apps.feature_flag.logic.queries.feature_flag import feature_flags_q__by_pk, feature_flags_q__all, \
    feature_flags_q__by_is_active, feature_flags__by_team_service_ids
from src.apps.feature_flag.models import FeatureFlag
from src.apps.team.models import Team, TeamService
from src.server.db import optional_session_generator


async def feature_flag__find_by_pk(*, pk: int, session: AsyncSession | None = None) -> FeatureFlag | None:
    query = feature_flags_q__by_pk(pk=pk)
    async with optional_session_generator(session=session) as async_session:
        scalars = await async_session.scalars(query)
        return scalars.one_or_none()


async def feature_flags__by_filter_list_dto(
    *,
    session: AsyncSession | None = None,
    filter_dto: FeatureFlagFilterDto
) -> typing.Sequence[FeatureFlag]:
    filter_data = filter_dto.model_dump(exclude_unset=True)
    query = feature_flags_q__all()
    if "is_active" in filter_data.keys():
        query = feature_flags_q__by_is_active(query=query, is_active=filter_data["is_active"])
    if "service_id" in filter_data.keys():
        query = feature_flags__by_team_service_ids(query=query, service_ids=[filter_dto.service_id])
    if "team_service_ids" in filter_data.keys():
        query = feature_flags__by_team_service_ids(query=query, service_ids=filter_dto.team_service_ids)

    async with optional_session_generator(session=session) as async_session:
        scalars = await async_session.scalars(query)
        return scalars.all()





