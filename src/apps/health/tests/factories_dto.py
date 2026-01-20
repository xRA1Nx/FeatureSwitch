from __future__ import annotations

from app.health.dtos import HealthCheckErrorDto

from utils.testing import BaseDtoFactory


class HealthCheckErrorDtoFactory(BaseDtoFactory[HealthCheckErrorDto]):
    __model__ = HealthCheckErrorDto
