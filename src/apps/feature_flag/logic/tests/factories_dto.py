from __future__ import annotations

from src.apps.feature_flag.dtos import FeatureFlagUpdateDto
from src.utils.testing import BaseDtoFactory


class FeatureFlagUpdateDtoFactory(BaseDtoFactory[FeatureFlagUpdateDto]):
    __model__ = FeatureFlagUpdateDto
