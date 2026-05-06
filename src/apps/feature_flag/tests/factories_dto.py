from __future__ import annotations

from src.apps.feature_flag.dtos import (
    FeatureFlagDto,
    FeatureFlagFilterDto,
    FeatureFlagListRequestDto,
    FeatureFlagUpdateDto,
)
from src.utils.testing import BaseDtoFactory


class FeatureFlagUpdateDtoFactory(BaseDtoFactory[FeatureFlagUpdateDto]):
    __model__ = FeatureFlagUpdateDto


class FeatureFlagListRequestDtoFactory(BaseDtoFactory[FeatureFlagListRequestDto]):
    __model__ = FeatureFlagListRequestDto


class FeatureFlagDtoFactory(BaseDtoFactory[FeatureFlagDto]):
    __model__ = FeatureFlagDto


class FeatureFlagFilterDtoFactory(BaseDtoFactory[FeatureFlagFilterDto]):
    __model__ = FeatureFlagFilterDto
