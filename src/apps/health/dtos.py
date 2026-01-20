from __future__ import annotations

from pydantic import Field

from src.apps.common.dto import BaseDto
from src.apps.health.enums import HealthCheckReason


class HealthCheckErrorDto(BaseDto):
    reason: HealthCheckReason
    message: str


class HealthCheckIsReadyResponseDto(BaseDto):
    is_ok: bool
    errors: list[HealthCheckErrorDto] = Field(default_factory=list)
