from __future__ import annotations

import typing

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.functions import GenericFunction

from src.apps.common.custom_types import BaseDtoType, BaseModelType
from src.apps.common.dtos import KafkaDto
from src.apps.common.models import BaseModel
from src.server.db import optional_session_generator


def instance_to_dto(*, instance: BaseModel, dto_class: type[BaseDtoType]) -> BaseDtoType:
    return dto_class.model_validate(instance.__dict__)


def instances_to_dtos(*, instances: typing.Iterable[BaseModel], dto_class: type[BaseDtoType]) -> list[BaseDtoType]:
    return [dto_class.model_validate(instance.__dict__) for instance in instances]


def instance_to_kafka_dto(*, instance: BaseModel, dto: type[KafkaDto], key: str) -> KafkaDto:
    instance_dict = instance.__dict__
    instance_dict["key"] = key
    return dto.model_validate(instance_dict)


async def check_db_exists(*, async_connection: AsyncConnection, dbname: str) -> bool:
    result = await async_connection.execute(
        text("SELECT 1 FROM pg_database WHERE datname = :dbname"), {"dbname": dbname}
    )
    return bool(result.scalar())


async def _add_all_to_session_and_commit(*, session: AsyncSession, instances: list[BaseModelType]) -> None:
    session.add_all(instances)
    await session.commit()


def _instance__prepare_for_update(*, instance: BaseModelType, dto: BaseDtoType) -> BaseModelType | None:
    have_changes = False
    for field, value in dto.model_dump(exclude_unset=True).items():
        if hasattr(instance, field) and getattr(instance, field) != value:
            setattr(instance, field, value)
            have_changes = True
    if not have_changes:
        return None
    return instance


async def save_model_instance[T: BaseModel](*, instance: T, session: AsyncSession | None = None) -> T:
    await save_model_instances(instances=[instance], session=session)
    return instance


async def save_model_instances[T: BaseModel](*, instances: list[T], session: AsyncSession | None = None) -> list[T]:
    should_commit = True
    if session:
        should_commit = False

    async with optional_session_generator(session=session) as async_session:
        async_session.add_all(instances)
        if should_commit:
            await async_session.commit()
        else:
            await async_session.flush()
    return instances


async def update_model_instance(
    *, instance: BaseModelType, dto: BaseDtoType, session: AsyncSession | None = None
) -> BaseModelType:
    should_commit = True
    if session:
        should_commit = False

    async with optional_session_generator(session=session) as async_session:
        updated_instance = _instance__prepare_for_update(instance=instance, dto=dto)
        if updated_instance is None:
            return instance

        async_session.add(updated_instance)
        if should_commit:
            await async_session.commit()
        else:
            await async_session.flush()
    return updated_instance


async def delete_model_instance(*, instance: BaseModelType, session: AsyncSession) -> None:
    await session.delete(instance=instance)
    await session.commit()


def is_related_instances_loaded(*, instance: BaseModelType, relationship_name: str) -> bool:
    """Проверяет, загружены ли связанные данные"""
    inspector = inspect(instance)
    return relationship_name not in inspector.unloaded


class make_interval(GenericFunction):  # noqa: N801
    """Генерирует SQL-выражение PostgreSQL функции make_interval().

    Пример:
        FeatureFlag.activated_at + make_interval(days=FeatureFlag.ttl_days)
    """

    inherit_cache = True  # Enables caching of SQL queries (the function is deterministic)

    def __init__(  # noqa: PLR0913
        self,
        years: int | InstrumentedAttribute[int] = 0,
        months: int | InstrumentedAttribute[int] = 0,
        weeks: int | InstrumentedAttribute[int] = 0,
        days: int | InstrumentedAttribute[int] = 0,
        hours: int | InstrumentedAttribute[int] = 0,
        mins: int | InstrumentedAttribute[int] = 0,
        secs: int | InstrumentedAttribute[int] = 0,
    ) -> None:
        super().__init__(years, months, weeks, days, hours, mins, secs)
