from __future__ import annotations

from src.apps.health.dtos import HealthCheckErrorDto
from src.utils.testing import BaseDtoFactory


class HealthCheckErrorDtoFactory(BaseDtoFactory[HealthCheckErrorDto]):
    __model__ = HealthCheckErrorDto
