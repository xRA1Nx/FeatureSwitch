from __future__ import annotations

from src.apps.feature_flag.dtos import FeatureFlagListItemDto, FeatureFlagListRequestDto, FeatureFlagUpdateDto
from src.utils.testing import BaseDtoFactory


class FeatureFlagUpdateDtoFactory(BaseDtoFactory[FeatureFlagUpdateDto]):
    __model__ = FeatureFlagUpdateDto


class FeatureFlagListRequestDtoFactory(BaseDtoFactory[FeatureFlagListRequestDto]):
    __model__ = FeatureFlagListRequestDto


class FeatureFlagListItemDtoFactory(BaseDtoFactory[FeatureFlagListItemDto]):
    __model__ = FeatureFlagListItemDto
