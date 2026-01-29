import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.feature_flag.dtos import FeatureFlagUpdateDto
from src.apps.feature_flag.logic.feature_flag import feature_flag__find_by_pk
from logging import getLogger

from src.apps.feature_flag.models import FeatureFlag
from src.utils.datetime import datetime_now_with_server_tz

logger = getLogger(__name__)

async def feature_flag__activated_at_on_change_is_active(
    *, current_feature_flag: FeatureFlag, update_dto: FeatureFlagUpdateDto
) -> datetime.datetime | None:
    if not current_feature_flag:
        logger.warning(f'Не удалось установить время начала активации флага, т.к. флаг с id={pk} не существует')
        return None

    if update_dto.is_active:
        return datetime_now_with_server_tz()
    return None


async def feature_flag__find_by_pk_or_raise(*, pk: int, session: AsyncSession | None = None):
    feature_flag = await feature_flag__find_by_pk(session=session, pk=pk)