from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.feature_flag.dtos import FeatureFlagListItemDto, FeatureFlagListRequestDto, FeatureFlagUpdateDto
from src.apps.feature_flag.logic.interactors.feature_flag import (
    feature_flag__activated_at_on_changes,
    feature_flag__find_by_pk_or_raise,
    feature_flag__has_changes,
)
from src.apps.feature_flag.models import FeatureFlag


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


async def feature_flags__list(
    *, request_dto: FeatureFlagListRequestDto, session: AsyncSession | None = None
) -> list[FeatureFlagListItemDto]:
    pass
