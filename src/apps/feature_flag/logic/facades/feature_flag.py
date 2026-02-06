from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.feature_flag.dtos import FeatureFlagListItemDto, FeatureFlagListRequestDto, FeatureFlagUpdateDto, \
    FeatureFlagFilterDto
from src.apps.feature_flag.logic.interactors.feature_flag import (
    feature_flag__activated_at_on_changes,
    feature_flag__find_by_pk_or_raise,
    feature_flag__has_changes,
)
from src.apps.feature_flag.logic.selectors.feature_flag import feature_flags__by_filter_list_dto
from src.apps.feature_flag.models import FeatureFlag
from src.apps.team.logic.interactors.team import team__find_by_name_or_raise
from src.apps.team.logic.interactors.team_service import team_service__find_by_name_or_raise
from src.apps.team.logic.selectors.team_service import team_services__by_team_id
from src.server.db import optional_session_generator
from src.utils.sql_alchemy import instances_to_dtos


async def feature_flag__prepare_for_admin_update(
    *, updated_feature_flag: FeatureFlag, update_dto: FeatureFlagUpdateDto
) -> FeatureFlag | None:
    current_feature_flag = await feature_flag__find_by_pk_or_raise(pk=updated_feature_flag.id)
    if not feature_flag__has_changes(update_dto=update_dto, current_feature_flag=current_feature_flag):
        return None

    updated_feature_flag.activated_at = feature_flag__activated_at_on_changes(
        current_feature_flag=current_feature_flag, update_dto=update_dto
    )
    return updated_feature_flag


async def feature_flag__filter_list_dto(
    *, request_dto: FeatureFlagListRequestDto, session: AsyncSession
) -> FeatureFlagFilterDto:
    filter_data = {}
    request_data = request_dto.model_dump(exclude_unset=True)
    if 'is_active' in request_data.keys():
        filter_data['is_active'] = request_data['is_active']

    if 'team_name' in request_data.keys():
        service = await team_service__find_by_name_or_raise(name=request_dto.team_name, session=session)
        filter_data['service_id'] = service.id

    if 'service_name' in request_data.keys():
        team = await team__find_by_name_or_raise(name=request_dto.team_name, session=session)
        filter_data['team_service_ids'] = await team_services__by_team_id(team_id=team.id, session=session)

    return FeatureFlagFilterDto.model_validate(filter_data)


async def feature_flags__list(
    *, request_dto: FeatureFlagListRequestDto, session: AsyncSession | None = None
) -> list[FeatureFlagListItemDto]:
    async with optional_session_generator(session=session) as async_session:
        filter_dto = await feature_flag__filter_list_dto(session=async_session, request_dto=request_dto)
        feature_flags = await feature_flags__by_filter_list_dto(filter_dto=filter_dto, session=async_session)
        return instances_to_dtos(instances=feature_flags, dto_class=FeatureFlagListItemDto)
