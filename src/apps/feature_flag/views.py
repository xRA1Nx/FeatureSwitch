from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.feature_flag.dtos import FeatureFlagListItemDto, FeatureFlagListRequestDto
from src.apps.feature_flag.logic.facades.feature_flag import feature_flags__list
from src.server.db import get_async_session


feature_flag_router = APIRouter(prefix="/feature_flags")


@feature_flag_router.get("")
async def get_feature_flags(
    request_dto: FeatureFlagListRequestDto = Query(...), session: AsyncSession = Depends(get_async_session)
) -> list[FeatureFlagListItemDto]:
    return await feature_flags__list(request_dto=request_dto, session=session)
