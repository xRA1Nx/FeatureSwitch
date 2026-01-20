from __future__ import annotations

from src.apps.health.dtos import HealthCheckIsReadyResponseDto
from src.apps.health.logic.interactors import get_db_health_errors


async def app__is_healthy() -> bool:
    """Проверка работоспособности сервиса"""
    return True


async def app__readiness_result() -> HealthCheckIsReadyResponseDto:
    errors = []
    errors.extend(await get_db_health_errors())
    is_ok = True if not errors else False  # noqa: SIM210
    return HealthCheckIsReadyResponseDto(errors=errors, is_ok=is_ok)
