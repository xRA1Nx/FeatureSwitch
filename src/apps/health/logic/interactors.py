from __future__ import annotations

import asyncpg
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.apps.health.dtos import HealthCheckErrorDto
from src.apps.health.enums import HealthCheckReason
from src.server.db import get_async_engine


async def get_db_health_errors() -> list[HealthCheckErrorDto]:
    """Проверка доступности PostgreSQL"""
    try:
        engine = get_async_engine()
        print(engine)
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.fetchone()

    except asyncpg.exceptions.PostgresConnectionError as e:
        return [
            HealthCheckErrorDto(reason=HealthCheckReason.DATABASE, message=f"Ошибка подключения к PostgreSQL: {e!s}")
        ]

    except SQLAlchemyError as e:
        return [HealthCheckErrorDto(reason=HealthCheckReason.DATABASE, message=f"Ошибка SQLAlchemy: {e!s}")]

    except Exception as e:
        return [
            HealthCheckErrorDto(
                reason=HealthCheckReason.DATABASE,
                message=f"Неизвестная ошибка при проверке подключения к Postgres: {e!s}",
            )
        ]
    else:
        return []
