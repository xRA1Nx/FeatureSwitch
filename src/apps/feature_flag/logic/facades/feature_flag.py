from __future__ import annotations

from src.apps.feature_flag.dtos import FeatureFlagUpdateDto
from src.apps.feature_flag.logic.interactors.feature_flag import (
    feature_flag__activated_at_on_changes,
    feature_flag__find_by_pk_or_raise,
    feature_flag__has_changes,
)
from src.apps.feature_flag.models import FeatureFlag
from src.server.db import async_session_generator


async def feature_flag__update(*, updated_feature_flag: FeatureFlag, update_dto: FeatureFlagUpdateDto) -> None:
    async with async_session_generator() as session:
        current_feature_flag = await feature_flag__find_by_pk_or_raise(session=session, pk=updated_feature_flag.id)
        if not feature_flag__has_changes(update_dto=update_dto, current_feature_flag=current_feature_flag):
            return

        current_feature_flag.activated_at = feature_flag__activated_at_on_changes(
            current_feature_flag=current_feature_flag, update_dto=update_dto
        )

        session.add(updated_feature_flag)
        await session.commit()
