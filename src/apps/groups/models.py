from __future__ import annotations

import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.common.models import BaseModel


if typing.TYPE_CHECKING:
    from src.apps.feature_flags.models import FeatureFlag


class Group(BaseModel):
    name: Mapped[str] = mapped_column(unique=True)

    feature_flags: Mapped[list[FeatureFlag]] = relationship(back_populates="group")
