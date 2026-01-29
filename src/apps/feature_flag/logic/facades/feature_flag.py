from src.apps.feature_flag.dtos import FeatureFlagUpdateDto
from src.apps.feature_flag.logic.feature_flag import feature_flag__find_by_pk
from src.apps.feature_flag.models import FeatureFlag
from src.server.db import async_session_generator


async def feature_flag__update(*, updated_feature_flag: FeatureFlag, update_dto: FeatureFlagUpdateDto):
    async with async_session_generator() as session:
        current_feature_flag = await feature_flag__find_by_pk(session=session, pk=updated_feature_flag.id)

        session.add(updated_feature_flag)
        await session.commit()
