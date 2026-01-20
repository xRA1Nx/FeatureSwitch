from __future__ import annotations

import typing

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from src.apps.common.custom_types import BaseDtoType, BaseModelType
from src.apps.common.dto import KafkaDto
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


def _instance__prepare_for_update(*, instance: BaseModelType, dto: BaseDtoType) -> BaseModelType:
    for field, value in dto.model_dump(exclude_unset=True).items():
        if hasattr(instance, field):
            setattr(instance, field, value)
    return instance


async def save_model_instance(*, instance: BaseModelType, session: AsyncSession | None = None) -> None:
    return await save_model_instances(instances=[instance], session=session)


async def save_model_instances(*, instances: list[BaseModelType], session: AsyncSession | None = None) -> None:
    async with optional_session_generator(session=session) as generator_session:
        await _add_all_to_session_and_commit(session=generator_session, instances=instances)


async def update_model_instance(*, instance: BaseModelType, dto: BaseDtoType, session: AsyncSession) -> BaseModelType:
    instance = _instance__prepare_for_update(instance=instance, dto=dto)
    await _add_all_to_session_and_commit(session=session, instances=[instance])
    return instance


async def delete_model_instance(*, instance: BaseModelType, session: AsyncSession) -> None:
    await session.delete(instance=instance)
    await session.commit()


def if_related_instances_loaded(*, instance: BaseModelType, relationship_name: str) -> bool:
    """Проверяет, загружены ли связанные данные"""
    inspector = inspect(instance)
    return relationship_name not in inspector.unloaded
