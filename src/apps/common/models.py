from __future__ import annotations

import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from src.apps.common.constants import UTC_TZ


class BaseModel(DeclarativeBase):
    abstract = True

    @staticmethod
    def server_current_datetime() -> datetime.datetime:
        return datetime.datetime.now(tz=UTC_TZ)

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=server_current_datetime)
    modified_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=server_current_datetime, onupdate=server_current_datetime
    )

    @declared_attr.directive
    def __tablename__(self) -> str:
        return f"{self.__name__.lower()}s"


class RemoteBaseModel(DeclarativeBase):
    pass
