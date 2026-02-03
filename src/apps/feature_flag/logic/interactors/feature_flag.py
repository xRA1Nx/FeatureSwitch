from __future__ import annotations

import datetime
from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.common.exceptions import BusinessLogicException
from src.apps.feature_flag.dtos import FeatureFlagUpdateDto
from src.apps.feature_flag.logic.feature_flag import feature_flag__find_by_pk
from src.apps.feature_flag.models import FeatureFlag
from src.utils.datetime import datetime_now_with_server_tz


logger = getLogger(__name__)


def feature_flag__activated_at_on_changes(
    *, current_feature_flag: FeatureFlag, update_dto: FeatureFlagUpdateDto
) -> datetime.datetime | None:
    if update_dto.is_active and current_feature_flag.is_active is False:
        return datetime_now_with_server_tz()
    return None


async def feature_flag__find_by_pk_or_raise(*, pk: int, session: AsyncSession | None = None) -> FeatureFlag:
    feature_flag = await feature_flag__find_by_pk(session=session, pk=pk)
    if not feature_flag:
        raise BusinessLogicException(f"Данная операция не возможна. не существует FeatureFlag с id={pk}")
    return feature_flag


def feature_flag__has_changes(*, current_feature_flag: FeatureFlag, update_dto: FeatureFlagUpdateDto) -> bool:
    return any(
        [current_feature_flag.is_active != update_dto.is_active, current_feature_flag.ttl_days != update_dto.ttl_days]
    )
