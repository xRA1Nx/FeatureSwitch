from __future__ import annotations

from src.apps.feature_flag.models import FeatureFlag
from src.utils.testing import BaseSqlAlchemyFactory, FactoryBuilderMixin


class FeatureFlagFactory(BaseSqlAlchemyFactory, FactoryBuilderMixin):
    __model__ = FeatureFlag
